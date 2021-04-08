<template>
  <div class="chart-summary">
    <span class="symbol">{{ this.ticker }}</span>
    <span class="bid">B --</span>
    <span class="ask">A --</span>
  </div>
  <svg id="singleChart" />
</template>

<script>
import * as d3 from "d3";

const f = d3.format("+.2%");
const formatChange = (y0, y1) => f((y1 - y0) / y0);
const formatValue = d3.format(".2f");
const formatDate = d3.utcFormat("%H:%M %m/%d");

const margin = {top: 20, right: 30, bottom: 30, left: 40};
const height = 600;
const width = 1200;

function formatData(data) {
  const formattedData = [];
  const candles = JSON.parse(data[0].candles);
  const candleLen = Object.entries(candles["t"]).length;
  for (let i = 0; i < candleLen; i++) {
    const date = new Date(candles["t"][i]);
    // filter out after/pre market candles for now
    if (date.getUTCDay() !== 0 && date.getUTCDay() !== 6 &&
        date.getUTCHours() >= 13 && date.getUTCHours() <= 22) {
      formattedData.push({
        'date': date,
        'open': Number(candles["o"][i]),
        'close': Number(candles["c"][i]),
        'low': Number(candles["l"][i]),
        'high': Number(candles["h"][i])
      });
    }
  }
  return formattedData;
}

function render(data) {
  console.log('records:', data);
  console.log('start:', data[0].date);
  console.log('end:', data[data.length-1].date);

  const y = d3.scaleLog()
      .domain([d3.min(data, d => d.low), d3.max(data, d => d.high)])
      .rangeRound([height - margin.bottom, margin.top]);

  const x = d3.scaleBand()
      .domain(d3.utcHour
          .range(data[0].date, +data[data.length - 1].date + 1)
          .filter(d => d.getUTCHours() >= 13 && d.getUTCHours() <= 22 &&
              d.getUTCDay() !== 0 && d.getUTCDay() !== 6))
      .range([margin.left, width - margin.right])
      .padding(0.2);

  console.log('x vals:', data.map(d => x(d.date)));
  console.log('y vals:', data.map(d => {
    return {o: y(d.open), c: y(d.close), h: y(d.high), l: y(d.low)};
  }));

  const yAxis = g => g
      .attr("transform", `translate(${margin.left},0)`)
      .attr('class', 'axis')
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
      .attr('class', 'axis')
      .call(d3.axisBottom(x)
          .tickValues(d3.utcHour
              .range(data[0].date, data[data.length - 1].date))
          .tickFormat(d3.utcFormat("%H:%M")))
      .call(g => g.select(".domain").remove());

  d3.select("#singleChart").selectAll('*').remove();

  const svg = d3
      .select("#singleChart")
      .attr("viewBox", [0, 0, width, height]);

  svg.append("g")
      .call(xAxis);

  svg.append("g")
      .call(yAxis);

  const g = svg.append("g")
      .attr("stroke", "gray")
      .selectAll("g")
      .data(data)
      .join("g")
      .attr("transform", d => {
        const val = Number(x(d.date));
        return `translate(${val},0)`;
      });

    g.append("line")
        .attr("y1", d => y(d.low))
        .attr("y2", d => y(d.high));

    g.append("line")
        .attr("y1", d => y(d.open))
        .attr("y2", d => y(d.close))
        .attr("stroke-width", x.bandwidth())
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
    ticker: null,
    data: []
  },
  updated() {
    const formattedData = formatData(this.data);
    render(formattedData);
  }
}
</script>

<style scoped></style>