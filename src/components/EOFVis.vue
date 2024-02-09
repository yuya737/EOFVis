<template>
    <Splitter style="height: 100%" layout="horizontal">
        <SplitterPanel style="height: 100%" :size="60">
            <ProjectionViewer class="h-full" />
        </SplitterPanel>

        <SplitterPanel style="height: 100%" :size="30">
            <MapViewer />
        </SplitterPanel>
    </Splitter>
</template>

<script setup lang="ts">
import Splitter from "primevue/splitter";
import SplitterPanel from "primevue/splitterpanel";
import MapViewer from "./MapViewer.vue";
import ProjectionViewer from "./ProjectionViewer.vue";
</script>
