import React  from 'react';
import * as d3 from 'd3';
import IChartProps from "../interfaces/IChartProps";
import { zoom } from 'd3-zoom';

// TODO - rename this, or change it to a mapped fn or something
const months = {
    0 : 'Jan',
    1 : 'Feb',
    2 : 'Mar',
    3 : 'Apr',
    4 : 'May',
    5 : 'Jun',
    6 : 'Jul',
    7 : 'Aug',
    8 : 'Sep',
    9 : 'Oct',
    10 : 'Nov',
    11 : 'Dec'
};

const ZoomableChart = (props: IChartProps) => {

    const svgRef = React.useRef(null);
    const { data, dimensions } = props;
    const { width, height, margin } = dimensions;
    const svgWidth = dimensions.margin.left + dimensions.margin.right + dimensions.width;
    const svgHeight = dimensions.margin.top + dimensions.margin.bottom + dimensions.height;
    const timer = null;

    console.log('got data:', data);

    React.useEffect(() => {

    const dateFormat = d3.timeParse("%Y-%m-%d");

    for (let i = 0; i < data.length; i++) {
        data[i].date = dateFormat(data[i].date?.toString() ?? '')
    }
    let dates = data.map(d => d.date);

    function zoomed({ transform }: any) {

        const xScale = d3.scaleLinear().domain([-1, dates.length])
            .range([0, width])
        let xScaleZ = transform.rescaleX(xScale);

        let hideTicksWithoutLabel = function() {
            d3.selectAll('.xAxis .tick text').each(function(d){
                if(this.innerHTML === '') {
                    this.parentNode.style.display = 'none'
                }
            })
        }

        gX.call(
            d3.axisBottom(xScaleZ).tickFormat((d, e, target) => {
                if (d >= 0 && d <= dates.length-1) {
                    const d = dates[d]
                    const hours = d.getHours()
                    const minutes = (d.getMinutes()<10?'0':'') + d.getMinutes()
                    const amPM = hours < 13 ? 'am' : 'pm'
                    return hours + ':' + minutes + amPM + ' ' + d.getDate() + ' ' + months[d.getMonth()] + ' ' + d.getFullYear()
                }
            })
        )

        candles.attr("x", (d, i) => xScaleZ(i) - (xBand.bandwidth()*t.k)/2)
            .attr("width", xBand.bandwidth()*t.k);
        stems.attr("x1", (d, i) => xScaleZ(i) - xBand.bandwidth()/2 + xBand.bandwidth()*0.5);
        stems.attr("x2", (d, i) => xScaleZ(i) - xBand.bandwidth()/2 + xBand.bandwidth()*0.5);

        hideTicksWithoutLabel();

        gX.selectAll(".tick text")
            .call(wrap, xBand.bandwidth())

    }

    function zoomend({ transform }: any) {
        const xScale = d3.scaleLinear().domain([-1, dates.length])
            .range([0, width])
        let xScaleZ = transform.rescaleX(xScale);
        clearTimeout(timer)
        timer = setTimeout(function() {

            const xDateScale = d3.scaleQuantize().domain([0, dates.length]).range(dates)
            let xMin = new Date(xDateScale(Math.floor(xScaleZ.domain()[0])))
            let xMax = new Date(xDateScale(Math.floor(xScaleZ.domain()[1])))
            let filtered = data.filter(d => ((d.date >= xMin) && (d.date <= xMax)))
            let minP = +d3.min(filtered, d => d.low)
            let maxP = +d3.max(filtered, d => d.high)
            let buffer = Math.floor((maxP - minP) * 0.1)

            yScale.domain([minP - buffer, maxP + buffer]);
            candles.transition()
                .duration(800)
                .attr("y", (d) => yScale(Math.max(d.open, d.close)))
                .attr("height",  d => (d.open === d.close)
                    ? 1
                    : yScale(Math.min(d.open, d.close)) - yScale(Math.max(d.open, d.close)));

            stems.transition().duration(800)
                .attr("y1", (d) => yScale(d.high))
                .attr("y2", (d) => yScale(d.low))

            gY.transition().duration(800).call(d3.axisLeft().scale(yScale));

        }, 500);
    }

    function wrap(text, width) {
        text.each(function() {
            const text = d3.select(this),
                words = text.text().split(/\s+/).reverse(),
                lineHeight = 1.1, // ems
                y = text.attr("y"),
                dy = parseFloat(text.attr("dy"));
            let line = [],
                word,
                lineNumber = 0,
                tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
            while (word = words.pop()) {
                line.push(word);
                tspan.text(line.join(" "));
                if (tspan.node().getComputedTextLength() ?? 0 > width) {
                    line.pop();
                    tspan.text(line.join(" "));
                    line = [word];
                    tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
                }
            }
        });
    }


        const svg = d3.select(svgRef.current)
            .attr("width", svgWidth)
            .attr("height", svgHeight)
            .append("g")
            .attr("transform", "translate(" +margin.left+ "," +margin.top+ ")");

        console.log('dates:', dates);

        const xScale = d3.scaleLinear().domain([-1, dates.length])
            .range([0, width])
        const xBand = d3.scaleBand().domain(
            d3.range(-1, dates.length)
                .map(r => r.toString())
        ).range([0, width]).padding(0.3)
        const xAxis = d3.axisBottom()
            .scale(xScale)
            .tickFormat(function(d) {
                let date = dates[d];
                let hours = date.getHours()
                let minutes = (date.getMinutes() <10 ? '0' : '') + date.getMinutes()
                let amPM = hours < 13 ? 'am' : 'pm'
                return hours + ':' + minutes + amPM + ' ' + date.getDate() + ' ' + months[date.getMonth()] + ' ' + date.getFullYear()
            });


        svg.append("rect")
            .attr("id","rect")
            .attr("width", width)
            .attr("height", height)
            .style("fill", "none")
            .style("pointer-events", "all")
            .attr("clip-path", "url(#clip)")

        const gX = svg.append("g")
            .attr("class", "axis x-axis") //Assign "axis" class
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)

        gX.selectAll(".tick text")
            .call(wrap, xBand.bandwidth())

        const yMin = d3.min(data.map(r => r.low));
        const yMax = d3.max(data.map(r => r.high));
        const yScale = d3.scaleLinear().domain([yMin, yMax]).range([height, 0]).nice();
        const yAxis = d3.axisLeft().scale(yScale);

        const gY = svg.append("g")
            .attr("class", "axis y-axis")
            .call(yAxis);

        const chartBody = svg.append("g")
            .attr("class", "chartBody")
            .attr("clip-path", "url(#clip)");

        // draw rectangles
        const candles = chartBody.selectAll(".candle")
            .data(data)
            .enter()
            .append("rect")
            .attr('x', (d, i) => xScale(i) - xBand.bandwidth())
            .attr("class", "candle")
            .attr('y', d => yScale(Math.max(d.open, d.close)))
            .attr('width', xBand.bandwidth())
            .attr('height', d => (d.open === d.close) ? 1 : yScale(Math.min(d.open, d.close))-yScale(Math.max(d.open, d.close)))
            .attr("fill", d => (d.open === d.close) ? "silver" : (d.open > d.close) ? "red" : "green")

        // draw high and low
        const stems = chartBody.selectAll("g.line")
            .data(data)
            .enter()
            .append("line")
            .attr("class", "stem")
            .attr("x1", (d, i) => xScale(i) - xBand.bandwidth()/2)
            .attr("x2", (d, i) => xScale(i) - xBand.bandwidth()/2)
            .attr("y1", d => yScale(d.high))
            .attr("y2", d => yScale(d.low))
            .attr("stroke", d => (d.open === d.close) ? "white" : (d.open > d.close) ? "red" : "green");

        svg.append("defs")
            .append("clipPath")
            .attr("id", "clip")
            .append("rect")
            .attr("width", width)
            .attr("height", height)

        const extent = [[0, 0], [width, height]];

        const zoom = d3.zoom()
            .scaleExtent([1, 100])
            .translateExtent(extent)
            .extent(extent)
            .on("zoom", zoomed)
            .on('zoom.end', zoomend);

        svg.call(zoom)
    }, [data]);

    return <svg ref={svgRef} width={svgWidth} height={svgHeight} />;
}

export default ZoomableChart;
