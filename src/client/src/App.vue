<template>
  <div class="container">
    <div class="row" id="app">
      <div class="col-lg-1">
        <Tracker @graphsModified="onGraphsModified"></Tracker>
      </div>
      <div class="col-lg" id="graph">
        <Graph :graphSymbols="graphSymbols"></Graph>
      </div>
    </div>
  </div>
</template>

<script>
import Graph from './components/Graph.vue'
// import Scheduler from './components/Scheduler.vue'
import Tracker from './components/Tracker.vue'

import "@/assets/css/reset.css";
import "@/assets/css/app.css";
import "@/assets/css/tracker-list.css";
import "@/assets/css/chart.css";

export default {
  name: 'App',
  components: {
    Graph,
    // Scheduler,
    Tracker
  },
  data() {
    return {
      graphSymbols: []
    }
  },
  methods: {
    onGraphsModified(charts) {
      this.graphSymbols = charts;
    }
  }
}
</script>

<style></style>
