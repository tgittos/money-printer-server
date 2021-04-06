<template>
  <svg id="singleChart" />
</template>

<script>
import * as d3 from "d3";

const f = d3.format("+.2%");
const formatChange = (y0, y1) => f((y1 - y0) / y0);
const formatValue = d3.format(".2f");
const formatDate = d3.utcFormat("%B %-d, %Y");

const margin = ({top: 20, right: 30, bottom: 30, left: 40});
const height = 600;
const width = 1200;

function formatData(data) {
  const formattedData = [];
  const candles = JSON.parse(data[0].candles);
  const candleLen = Object.entries(candles["t"]).length;
  for (let i = 0; i < candleLen; i++) {
    formattedData.push({
      'date': new Date(candles["t"][i]),
      // 'date': Number(candles["t"][i]),
      'open': Number(candles["o"][i] ?? 0),
      'close': Number(candles["c"][i] ?? 0),
      'low': Number(candles["l"][i] ?? 0),
      'high': Number(candles["h"][i] ?? 0)
    });
  }
  formattedData.sort((a, b) => a['date'] > b['date'] ? 1 : a['date'] < b['date'] ? -1 : 0);
  return formattedData;
}

function render(data) {
  console.log('start:', data[0].date);
  console.log('end:', data[data.length-1].date);

  const yAxis = g => g
      .attr("transform", `translate(${margin.left},0)`)
      .call(d3.axisLeft(y)
          .tickFormat(d3.format("$~f"))
          .tickValues(d3.scaleLinear().domain(y.domain()).ticks())
          .tickSize(0))
      .call(g => g.selectAll(".tick line").clone()
          .attr("stroke-opacity", 0.2)
          .attr("x2", width - margin.left - margin.right))
      .call(g => g.select(".domain").remove());

  const xAxis = g => g
      .attr("transform", `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x)
          .tickValues(d3.utcMonday
              .every(4)
              .range(data[0].date, data[data.length - 1].date))
          .tickFormat(d3.utcFormat("%-m/%-d/%-y"))
          .tickSize(0))
      .call(g => g.select(".domain").remove());

  const y = d3.scaleLog()
      .domain([d3.min(data, d => d.low), d3.max(data, d => d.high)])
      .rangeRound([height - margin.bottom, margin.top]);

  const x = //d3.scaleBand()
      //.domain(d3.utcDay
      //    .range(data[0].date, +data[data.length - 1].date + 1)
      //    .filter(d => d.getUTCDay() !== 0 && d.getUTCDay() !== 6))
      d3.scaleLinear()
      .domain([d3.min(data, d => d.date), d3.max(data, d => d.date)])
      .range([margin.left, width - margin.right])
      //.padding(0.2);

  d3.select("#singleChart").selectAll('*').remove();

  const svg = d3
      .select("#singleChart")
      .attr("viewBox", [0, 0, width, height]);

  const g = svg.append("g")
      .attr("stroke-linecap", "round")
      .attr("stroke", "black")
      .selectAll("g")
      .data(data)
      .join("g")
      .attr("transform", d => {
        return `translate(${x(d.date) ?? 0},0)`;
      });

  svg.append("g")
      .call(xAxis);

  svg.append("g")
      .call(yAxis);

    g.append("line")
        .attr("y1", d => y(d.low))
        .attr("y2", d => y(d.high));

    g.append("line")
        .attr("y1", d => y(d.open))
        .attr("y2", d => y(d.close))
        //.attr("stroke-width", x.bandwidth())
        .attr("stroke", d => d.open > d.close ? d3.schemeSet1[0]
            : d.close > d.open ? d3.schemeSet1[2]
                : d3.schemeSet1[8]);

    g.append("title")
        .text(d => `${formatDate(d.date)}
          Open: ${formatValue(d.open)}
          Close: ${formatValue(d.close)} (${formatChange(d.open, d.close)})
          Low: ${formatValue(d.low)}
          High: ${formatValue(d.high)}`);
}

export default {
  name: "Single",
  props: {
    data: []
  },
  updated() {
    const formattedData = formatData(this.data);
    render(formattedData);
  }
}
</script>

<style scoped></style>