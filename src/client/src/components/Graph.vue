<template>
  <Single :data="singleData"></Single>
</template>

<script>
import axios from 'axios';
import config from "../config";
import Single from "./graphs/Single";

export default {
  name: "Graph",
  components: {Single},
  props: {
    graphSymbols: []
  },
  data() {
    return {
      charts: {},
      singleData: [],
    }
  },
  updated() {
    this.graphSymbols.map(sync => {
      if (!this.charts[sync.symbol]) {
        // fetch data from server to draw charts
        console.log('fetching chart data for ticker:', sync.symbol)
        axios.get(config.apiRoot + '/candles/' + sync.symbol)
            .then(response => {
              console.log(response);
              if (response.data.success) {
                this.charts[sync.symbol] = response.data.data
                this.singleData = response.data.data;
              }
            });
      }
    });
  }
}
</script>

<style scoped>

</style>