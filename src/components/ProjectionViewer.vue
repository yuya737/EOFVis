<template>
    <div id="eofvis-parent" class="h-full w-full">
        <div class="relative h-full w-full">
            <canvas
                id="deck-canvas-projection-viewer"
                class="z-[2] h-full w-full"
            />
            <div
                id="minimap-background"
                class="absolute left-[20px] top-[20px] z-[1] aspect-square h-1/4 w-1/4 rounded-md bg-gray-100 shadow-md"
            />

            <div
                class="relative left-[20px] top-[20px] z-[3] w-1/4 text-center text-black"
            >
                Overview
            </div>
        </div>

        <div
            class="relative bottom-10 left-1/2 z-[3] w-fit -translate-x-1/2 -translate-y-1/2 transform rounded-md bg-gray-200 p-4 text-lg font-bold text-black"
        >
            {{ bottomText }}
        </div>

        <div
            id="tooltip"
            class="absolute z-[4] rounded bg-gray-800 p-2 text-white shadow"
            style="display: none"
        ></div>
    </div>
</template>

<script setup lang="ts">
import {
    Ref,
    onMounted,
    watch,
    useAttrs,
    toRaw,
    ref,
    nextTick,
    inject,
} from "vue";
import {
    Deck,
    OrthographicView,
    OrbitView,
    OrthographicViewport,
    MapView,
    COORDINATE_SYSTEM,
} from "@deck.gl/core";
import { scaleLinear, interpolatePRGn, interpolateBlues } from "d3";
import { ScatterplotLayer, PathLayer, PointCloudLayer } from "deck.gl/typed";
import { LayersList, OrthographicViewState, Layer } from "@deck.gl/core/typed";
import { AxisLayer } from "./utils/AxisLayer";
import API from "@/api/api";
import { useStore } from "@/store/main";

const store = useStore();

const fileName =
    "/Users/yuyakawakami/Research/EOF_ensemble/eof_data/rcpall_pr_south_america_spatial_1_decadal.csv";
// "/Users/yuyakawakami/Research/EOF_ensemble/eof_data/ssp_sim_all_spatial_0.csv";
// "/Users/yuyakawakami/Research/EOF_ensemble/eof_data/pr_ssp_sim_all_spatial_1.csv";

const bottomText = ref(
    "MPI-GE Ensemble Surface Temperature RCPs 2.6, 4.5, and 8.5",
);

const orbitView = new OrbitView({
    id: "main",
    controller: true,
});

const orthoView = new OrthographicView({
    id: "main",
    controller: true,
});
const miniorthoView = new OrthographicView({
    id: "minimap",
    zoom: 2,
    x: 20,
    y: 20,
    width: "25%",
    height: "25%",
    clear: true,
});

let layerList: LayersList = [];

let data = [
    {
        coords: [0, 0],
    },
    {
        coords: [1, 1],
    },
];

let deck: any = null;

const DECKGL_SETTINGS = {
    canvas: "deck-canvas-projection-viewer",
    width: "100%",
    height: "100%",
    controller: true,

    initialViewState: {
        main: {
            target: [0, 0, 0],
            zoom: 7,
        },
        minimap: {
            target: [0, 0, 0],
            zoom: 2,
        },
    },
};

onMounted(() => {
    deck = new Deck({
        onViewStateChange: ({ viewState }) => {
            handleViewStateChange(viewState);
        },
        ...DECKGL_SETTINGS,
        views: [orthoView, miniorthoView],
        layerFilter: layerFilter,
        // getTooltip: mytooltip
    });

    initalLayerProps().then((layers: any) => {
        layerList = layers;
        setLayerProps();
    });
});

async function initalLayerProps() {
    bottomText.value = "Projections: " + fileName.split("/").pop();
    const point_data = await API.fetchData("spatial_MPI", true, {
        file: fileName,
        filter_string: "",
        temporal: false,
        three_d: false,
    });

    const colorInterp = (val) =>
        interpolateBlues(scaleLinear().domain([0, 10]).range([0, 1])(val))
            .replace(/[^\d,]/g, "")
            .split(",")
            .map((d) => Number(d));

    const color = (d) => {
        const matches = d.text.match(/RCP(\d+):E(\d+):D(\d+)/);
        return colorInterp(matches[3]);
        if (d.text.includes("RCP26")) {
            return [0, 0, 255];
        } else if (d.text.includes("RCP45")) {
            return [0, 255, 0];
        } else if (d.text.includes("RCP85")) {
            return [255, 0, 0];
        } else {
            return [0, 0, 0];
        }
    };
    let scatterplotLayer = new ScatterplotLayer({
        // let scatterplotLayer = new PointCloudLayer({
        id: "scatterplot-layer",
        data: point_data["points"],
        // data: data,
        pickable: true,
        getPosition: (d: any) => d.coords,
        getRadius: 0.06,
        // getFillColor: (d) => {
        getColor: color,
        // getColor: (d) => {
        //     if (d.text.includes("RCP26")) {
        //         return [0, 0, 255];
        //     } else if (d.text.includes("RCP45")) {
        //         return [0, 255, 0];
        //     } else if (d.text.includes("RCP85")) {
        //         return [255, 0, 0];
        //     } else {
        //         return [255, 255, 255];
        //     }
        // },
        // coordinateSystem: COORDINATE_SYSTEM.CARTESIAN,
        // radiusPixels: 4,
        autoHighlight: true,
        onHover: ({ object, x, y }) => {
            const el = document.getElementById("tooltip");
            if (!object) {
                el.style.display = "none";
                return;
            }
            console.log(object.text);
            const matches = object.text.match(/RCP(\d+):E(\d+)/);
            // console.log('sdfsdf')
            if (object) {
                el.innerHTML = `${object.text}`;
                el.style.display = "block";
                el.style.opacity = 0.9;
                el.style.left = x + "px";
                el.style.top = y + "px";
            } else {
                el.style.opacity = 0.0;
            }
        },
        onClick: ({ object, x, y }) => {
            store.updateID(fileName, object.text);
        },
    });
    // let d = [
    //     {
    //         position: [0, 0, 0],
    //         normal: [0, 0, 1],
    //         color: [255, 0, 0],
    //     },
    //     {
    //         position: [1, 1, 1],
    //         normal: [0, 0, 1],
    //         color: [0, 255, 0],
    //     },
    // ];
    // const layer = new PointCloudLayer({
    //     id: "point-cloud-layer",
    //     data: d,
    //     pickable: false,
    //     coordinateSystem: COORDINATE_SYSTEM.CARTESIAN,
    //     coordinateOrigin: [0, 0, 0],
    //     radiusPixels: 4,
    //     getPosition: (d) => d.position,
    //     getNormal: (d) => d.normal,
    //     getColor: (d) => d.color,
    // });
    let axis = new AxisLayer(-20, 20, -20, 20, 2.5);

    return [...axis.getLayers(), scatterplotLayer];
}

function setLayerProps() {
    deck.setProps({ layers: layerList });
}

function handleViewStateChange(viewstate: OrthographicViewState) {
    const viewport = new OrthographicViewport(viewstate);

    const topLeft = viewport.unproject([0, 0]);
    const topRight = viewport.unproject([viewstate.width, 0]);

    const bottomLeft = viewport.unproject([0, viewstate.height]);
    const bottomRight = viewport.unproject([viewstate.width, viewstate.height]);

    let bounds_layer = new PathLayer({
        id: "viewport-bounds",
        data: [[topLeft, topRight, bottomRight, bottomLeft, topLeft]],
        getPath: (d) => d,
        getColor: [255, 0, 0],
        getWidth: 2,
        widthUnits: "pixels",
    });

    deck.setProps({
        layers: [bounds_layer, ...layerList],
        viewState: {
            main: viewstate,
            // minimap: {
            //     ...viewstate,
            //     zoom: 2
            // }
        },
    });
}

function layerFilter({ layer, viewport }) {
    if (layer.id != "viewport-bounds") {
        return true;
    }
    return viewport.id == "minimap";
}
</script>
