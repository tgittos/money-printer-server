<template>
  <ul id="tracker-list">
    <li v-for="sync in syncs" :key="sync.symbol" @click="graphSymbolToggle(sync)"
      v-bind:class="isGraphed">
      {{ sync.symbol }} [{{ formatDate(sync.last_update) }}]
    </li>
  </ul>
  <input v-if="addMode" v-model="symbolToAdd" name="symbol">
  <button id="tracker-list-add" v-if="!addMode" @click="showSymbolAdd">+</button>
  <button id="tracker-list-add" v-if="addMode" @click="submitSymbolAdd">Add</button>
</template>

<script>

import axios from "axios";
import moment from "moment";
import config from "./../config";

export default {
  name: "Tracker",
  mounted () {
    axios.get(config.apiRoot + '/symbols')
        .then(response => {
          if (response.data.success) {
            this.syncs = response.data.data
          }
        });
  },
  data() {
    return {
      symbolToAdd: '',
      addMode: false,
      syncs: [],
      graphs: []
    }
  },
  methods: {
    formatDate(date) {
      if (date) {
        return moment(date).fromNow();
      }
      return 'never';
    },
    showSymbolAdd() {
      this.addMode = true;
    },
    submitSymbolAdd() {
      this.addMode = false;
      this.symbolToAdd = '';
    },
    graphSymbolToggle(symbol) {
      if (this.graphs.includes(symbol)) {
        this.graphs = this.graphs.filter(r => r != symbol);
      } else {
        this.graphs = this.graphs.concat(symbol);
      }
      this.$emit('graphsModified', this.graphs);
    },
  },
  computed: {
    isGraphed: function(symbol) {
      return {
        'graphed': this.graphs.includes(symbol)
      };
    }
  }
}
</script>
