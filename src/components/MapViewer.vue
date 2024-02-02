<template>
    <div class="relative h-full w-full">
        <canvas id="deck-canvas-map-viewer" class="h-full w-full" />
        <MapboxMap
            style="height: 400px"
            :access-token="token"
            map-style="mapbox://styles/mapbox/light-v11"
            :center="computedMapCenter"
            :zoom="zoom"
        />
    </div>
</template>

<script setup lang="ts">
import { MapboxMap } from "@studiometa/vue-mapbox-gl";
import { useStore } from "@/store/main";
import { reactive, ref, watch, onMounted, computed } from "vue";
import API from "@/api/api";

import { Deck, MapView, MapViewport } from "@deck.gl/core";
import { ScatterplotLayer, PathLayer } from "deck.gl/typed";

let deck: any = null;
const token: string =
    "pk.eyJ1IjoieXV5YTczNyIsImEiOiJjbGY0ZmMzbG4wcjNvM3hxbTVqaWpqaDQ3In0.wkIMGbAn6HaRVqPs2CJSnA";

let latitudes: number[] = [];
let longitudes: number[] = [];

const mapCenter = reactive([0, 0]);
const computedMapCenter = computed(() => [mapCenter[0], mapCenter[1]]);
const zoom = ref(1);

const DECKGL_SETTINGS = {
    canvas: "deck-canvas-map-viewer",
    width: "100%",
    height: "100%",
    controller: true,
    initialViewState: {
        latitude: 0,
        longitude: 0,
        zoom: 1,
    },
};

onMounted(() => {
    fetchMapDimensions();

    deck = new Deck({
        onViewStateChange: ({ viewState }) => {
            mapCenter[0] = viewState.longitude;
            mapCenter[1] = viewState.latitude;
            zoom.value = viewState.zoom;
        },
        ...DECKGL_SETTINGS,
    });
});

const store = useStore();

watch(
    () => store.getID,
    (newVal) => {
        console.log("SFSDF");
        fetchMapData(newVal.model_id, newVal.ensemble_id);
    },
);

async function fetchMapData(model_id: string, ensemble_id: string) {
    console.log(model_id, ensemble_id);
    const data = await API.fetchData(
        `spatial/${model_id}/${ensemble_id}`,
        true,
        null,
    );
    const mapData = data[0].data.map((d, index) => {
        return {
            val: d,
            lat: latitudes[index % latitudes.length],
            lon: longitudes[Math.floor(index / latitudes.length)],
        };
    });
    console.log(mapData);

    let scatterplotlayer = new ScatterplotLayer({
        id: "scatterplot-layer",
        data: mapData,
        pickable: true,
        opacity: 0.8,
        stroked: true,
        filled: true,
        radiusScale: 6,
        radiusMinPixels: 1,
        radiusMaxPixels: 100,
        lineWidthMinPixels: 1,
        getPosition: (d: any) => [d.lon, d.lat],
        getRadius: (d: any) => 100,
        getFillColor: [255, 140, 0],
        getLineColor: [0, 0, 0],
    });

    deck.setProps({
        layers: [scatterplotlayer],
    });
}

async function fetchMapDimensions() {
    console.log("Fetching map dimensions");
    const mapDimensions = await API.fetchData("spatial_grid", true, null);
    console.log(mapDimensions);
    latitudes = mapDimensions.lat;
    longitudes = mapDimensions.lon;
}
</script>
