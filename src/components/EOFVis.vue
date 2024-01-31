<template>
    <div id="eofvis-parent" class="w-full h-full">
        <canvas id="deck-canvas" class="absolute bottom-0 left-0 w-full h-full"/>
        <div id="minimap-background" ></div>

        <div class="fixed bottom-10 left-1/2 transform -translate-x-1/2 bg-gray-800 p-4 text-white">
            {{  bottomText }}
        </div>
        
        <div id="tooltip" class="absolute bg-gray-800 text-white p-2 rounded shadow" style="display: none;"></div>
        


    </div>
</template>

<script setup lang="ts">
import { Ref, onMounted, watch, useAttrs, toRaw, ref, nextTick, inject } from 'vue'
import { Deck, OrthographicView, OrthographicViewport, MapView } from '@deck.gl/core'

import { ScatterplotLayer, PathLayer } from 'deck.gl/typed';

import { LayersList, OrthographicViewState, Layer } from '@deck.gl/core/typed'

import { AxisLayer } from './utils/AxisLayer'

import API from '../api/api'

const bottomText = ref("MPI-GE Ensemble Surface Temperature RCPs 2.6, 4.5, and 8.5")


const orthoView = new OrthographicView({
    id: 'main',
    controller: true
});
const miniorthoView = new OrthographicView({
    id: 'minimap',
    zoom: 2,
    x: 20,
    y: 20,
    width: '20%',
    height: '20%',
    clear: true
});

let layerList: LayersList = []


// import { onMounted } from 'vue';
let deck: any = null;

const DECKGL_SETTINGS = {
    canvas: "deck-canvas",
    width: "100%",
    height: "100%",
    controller: true,

    initialViewState: {
        main: {
            target: [0, 0, 0],
            zoom: 7
        },
        minimap: {
            target: [0, 0, 0],
            zoom: 2
        }
    }
}


onMounted(() => {

    deck = new Deck({
        onViewStateChange: ({ viewState }) => { handleViewStateChange(viewState) },
        ...DECKGL_SETTINGS,
        views: [orthoView, miniorthoView],
        layerFilter: layerFilter,
        getTooltip: ({object}) => {
            console.log('sdfsdf')
            object && object.message
        }
    })

    initalLayerProps().then((layers: any) => {
        layerList = layers
        setLayerProps()
    })
})

async function initalLayerProps(){
    const point_data = await API.fetchData('spatial', true, null)
    let scatterplotLayer = new ScatterplotLayer({
        id: 'scatterplot-layer',
        data: point_data['points'],
        pickable: true,
        getPosition: (d: any) => d.coords,
        getRadius: 0.05,
        getFillColor: d => {
            if (d.text.includes('rcp26')) {
                return [0, 0, 255]
            } else if (d.text.includes('rcp45')) {
                return [0, 255, 0]
            } else if (d.text.includes('rcp85')) {
                return [255, 0, 0]
            } else {
                return [255, 255, 255]
            }
            
        }
            ,
        autoHighlight: true,
        // onHover: (info, event) => console.log('Hovered:', info, event),
        // onClick: (info, event) => console.log('Clicked:', info, event)
        onClick: ({object, x, y}) => {
            // console.log('sdfsdf')
            const el = document.getElementById('tooltip');
            if (object) {
                el.innerHTML = `${object.text}`;
                el.style.display = 'block';
                el.style.opacity = 0.9;
                el.style.left = x + 'px';
                el.style.top = y + 'px';
            } else {
                el.style.opacity = 0.0;
            }
        },
    })
    let axis = new AxisLayer(-20, 20, -20, 20, 5)
    
    return [ 
        ...axis.getLayers(),
        scatterplotLayer
    ]
}

function setLayerProps() {
    deck.setProps({ layers: layerList })
}

function handleViewStateChange(viewstate: OrthographicViewState) {

    const viewport = new OrthographicViewport(viewstate);

    const topLeft = viewport.unproject([0, 0]);
    const topRight = viewport.unproject([viewstate.width, 0]);
    const bottomLeft = viewport.unproject([0, viewstate.height]);
    const bottomRight = viewport.unproject([viewstate.width, viewstate.height]);

    let bounds_layer = new PathLayer({
        id: 'viewport-bounds',
        data: [[topLeft, topRight, bottomRight, bottomLeft, topLeft]],
        getPath: d => d,
        getColor: [255, 0, 0],
        getWidth: 2,
        widthUnits: 'pixels'
    })

    deck.setProps({
        layers: [
            bounds_layer, ...layerList
        ],
        viewState: {
            main: viewstate,
            // minimap: {
            //     ...viewstate,
            //     zoom: 2
            // }
        }
    })
}

function layerFilter({ layer, viewport }) {
    if (layer.id != 'viewport-bounds') {
        return true;
    } 
    return viewport.id == 'minimap';
}

</script>

<style scoped>
#minimap-background{ 
    position: absolute; 
    top: 20px; 
    left: 20px;
    z-index: -1; 
    width: 20%; 
    height: 20%; 
    background: #D3D3D3; 
    box-shadow: 0 0 8px 2px rgba(0,0,0,0.15);

} 
</style>
