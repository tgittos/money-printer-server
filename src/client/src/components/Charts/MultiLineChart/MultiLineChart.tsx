import React from 'react';
import * as d3 from 'd3';
import Symbol, {ISymbol} from "../../../models/Symbol";
import {randomColor} from "../lib/ChartUtils";
import IChartProps from "../interfaces/IChartProps";

const MultiLineChart = ({ data, dimensions }: IChartProps) => {
    /*
    console.log('got data:', data);
    console.log('got dimensions:', dimensions);

    const svgRef = React.useRef(null);
    const {width, height, margin} = dimensions;
    const svgWidth = width + margin.left + margin.right;
    const svgHeight = height + margin.top + margin.bottom;

    React.useEffect(() => {
        const f = d3.format("+.2%");
        const formatChange = (y0: number, y1: number) => f((y1 - y0) / y0);
        const formatValue = d3.format(".2f");
        const formatDate = d3.utcFormat("%H:%M %m/%d");

        const chartData = data;

        if (chartData.length == 0) {
            // someone called the chart with no data, lets inject a dummy data point so that
            // we can at least render the axis
            chartData.push(new Symbol({
                open: 0,
                close: 0,
                low: 0,
                high: 0,
                latestUpdate: new Date().getTime()
            } as ISymbol));
        }

        const lowerDateBound = data[0]?.date ?? new Date();
        const upperDateBound = data[data.length-1]?.date ?? new Date();

        console.log('rendering with width:', width);
        console.log('rendering with height:', height);
        console.log('rendering with margin:', margin);
        console.log('rendering with chartData:', chartData);

        const y = d3.scaleLog()
            .domain([d3.min(chartData, d => d.low) as number, d3.max(chartData, d => d.high) as number])
            .rangeRound([height - margin.bottom, margin.top]);

        const x = d3.scaleBand()
            .domain(d3.utcHour
                .range(lowerDateBound, upperDateBound)
                .filter(d => d.getUTCHours() >= 13 && d.getUTCHours() <= 22 &&
                    d.getUTCDay() !== 0 && d.getUTCDay() !== 6)
                .map(d => d.toDateString()))
            .range([margin.left, width - margin.right])
            .padding(0.2);

        console.log('raw x\'s:', chartData.map(d => d.date));
        console.log('x vals:', chartData.map(d => x(d.date.toDateString())));
        console.log('y vals:', chartData.map(d => {
            return {o: y(d.open), c: y(d.close), h: y(d.high), l: y(d.low)};
        }));

        const yAxis = (g: any) => g
            .attr("transform", `translate(${margin.left},0)`)
            .attr('class', 'axis')
            .call(d3.axisLeft(y)
                .tickFormat(d3.format("$~f"))
                .tickValues(d3.scaleLinear().domain(y.domain()).ticks())
                .tickSize(0))
            .call((g: any) => g.selectAll(".tick line").clone()
                .attr("stroke-opacity", 0.2)
                .attr("x2", width - margin.left - margin.right))
            .call((g: any) => g.select(".domain").remove());

        const xAxis = (g: any) => g
            .attr("transform", `translate(0,${height - margin.bottom})`)
            .attr('class', 'axis')
            .call(d3.axisBottom(x)
                .tickValues(d3.utcHour
                    .range(chartData[0].date, chartData[chartData.length - 1].date)
                    .map(d => d.toDateString()))
                // .tickFormat(d3.utcFormat("%H:%M"))
                )
            .call((g: any) => g.select(".domain").remove());

        d3.select("#singleChart").selectAll('*').remove();

        // create root container
        const svg = d3.select(svgRef.current);
        svg.selectAll("*").remove();
        svg.attr("viewBox", `['0', '0', ${width}, ${height}]`);

        svg.append("g")
            .call(xAxis);

        svg.append("g")
            .call(yAxis);

        const g = svg.append("g")
            .attr("stroke", "gray")
            .selectAll("g")
            .data(chartData)
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
High: ${formatValue(d.high)}`
            );
    }, [data]); // Redraw chart if data changes

    return <svg ref={svgRef} width={svgWidth} height={svgHeight} />;

     */
}

export default MultiLineChart;
