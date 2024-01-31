<template>
    <div id="eofvis-parent">
        <canvas id="deck-canvas" />
        <div id="minimap-background" ></div>

    </div>
</template>

<script setup lang="ts">
import { Ref, onMounted, watch, useAttrs, toRaw, ref, nextTick, inject } from 'vue'
import { Deck, OrthographicView, OrthographicViewport, MapView } from '@deck.gl/core'

import { ScatterplotLayer, PathLayer } from 'deck.gl/typed';

import { LayersList, OrthographicViewState, Layer } from '@deck.gl/core/typed'


const orthoView = new OrthographicView({
    id: 'main',
    controller: true
});
const miniorthoView = new OrthographicView({
    id: 'minimap',
    x: 20,
    y: 20,
    zoom: 2,
    width: '20%',
    height: '20%',
    clear: true
});

const minimapBackgroundStyle = {
    position: 'absolute',
    zIndex: -1,
    width: '100%',
    height: '100%',
    background: '#fefeff',
    boxShadow: '0 0 8px 2px rgba(0,0,0,0.15)'
};

let data: any = [
    {
        "coordinates": [0, 0]
    },
    {
        "coordinates": [1, 0]
    },
    {
        "coordinates": [2, 0]
    },
    {
        "coordinates": [2, 2.5]
    },
    {
        "coordinates": [0, 3.5]
    },
    {
        "coordinates": [0, -2]
    },
    {
        "coordinates": [1, 3]
    },
    {
        "coordinates": [2, 8]
    },
    {
        "coordinates": [2, 2.5]
    },
    {
        "coordinates": [-4, 3.5]
    },
    {
        "coordinates": [-5, -2]
    },
];

let bounds: any = []


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
            zoom: 5
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
        layerFilter: layerFilter
    })

    deck.setProps({ layers: getLayerProps()})



    // animatedProps = getAnimatedProps();

    // Setup settings object that handles the layer settings at each iteration
})

function getLayerProps(){
    let layer = new ScatterplotLayer({
        id: 'scatterplot-layer',
        data: data,
        pickable: true,
        getPosition: (d: any) => d.coordinates,
        getRadius: 0.5,
        getColor: [255, 0, 0],
    })
    return [layer]
}

function handleViewStateChange(viewstate: OrthographicViewState) {

    const viewport = new OrthographicViewport(viewstate);

    const topLeft = viewport.unproject([0, 0]);
    const topRight = viewport.unproject([viewstate.width, 0]);
    const bottomLeft = viewport.unproject([0, viewstate.height]);
    const bottomRight = viewport.unproject([viewstate.width, viewstate.height]);
    console.log(topLeft, topRight, bottomLeft, bottomRight)

    let bounds_layer = new PathLayer({
        id: 'viewport-bounds',
        data: [[topLeft, topRight, bottomRight, bottomLeft, topLeft]],
        getPath: d => d,
        getColor: [255, 0, 0],
        getWidth: 2,
        widthUnits: 'pixels'
    })

    deck.setProps({
        layers: [bounds_layer, ...getLayerProps()],
        viewState: {
            main: viewstate,
            minimap: {
                ...viewstate,
                width: 200,
                height: 200,
                x: 20,
                y: 20,
            }
        }
    })


    console.log(viewstate)
    console.log(topLeft, topRight, bottomLeft, bottomRight)

}

function layerFilter({ layer, viewport }) {
    if (layer.id != 'viewport-bounds') {
        return true;
    } 
    return viewport.id == 'minimap';
}

</script>

<style scoped>
#eofvis-parent {
    width: 100%;
    height: 100%;
}

#deck-canvas {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 100%;
}
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
