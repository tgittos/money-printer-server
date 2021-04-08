<template>
  <Single :data="singleData" :symbol="charts[0]?.symbol"></Single>
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
        // calculate time window
        const end = Date.now() / 1000;
        const now = new Date();
        const start = now.setDate(now.getDate()-7) / 1000;
        // fetch data from server to draw charts
        console.log('fetching chart data for ticker:', sync.symbol)
        axios.get(`${config.apiRoot}/candles/${sync.symbol}?start=${start}&end=${end}`)
            .then(response => {
              console.log(response);
              if (response.data.success) {
                this.charts[sync.symbol] = response.data.data
                this.singleData = response.data.data;
              }
            });
      } else {
        this.singleData = this.charts[sync.symbol];
      }
    });
  }
}
</script>

<style scoped>

</style>