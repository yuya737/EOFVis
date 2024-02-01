<template>
    <Splitter style="height: 100%" layout="vertical">
        <SplitterPanel style="height: 100%" :size="50" class="bg-gray-800">
            <ProjectionViewer class="h-full"/>
        </SplitterPanel>

        <SplitterPanel :size="50" class="bg-gray-800">
            <MapViewer />
        </SplitterPanel>
    </Splitter>
            <!-- <ProjectionViewer class="h-full"/> -->
</template>

<script setup lang="ts">
import Splitter from 'primevue/splitter'
import SplitterPanel from 'primevue/splitterpanel'

import MapViewer from './MapViewer.vue'
import ProjectionViewer from './ProjectionViewer.vue'

</script>