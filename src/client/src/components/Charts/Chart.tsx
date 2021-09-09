import IChartProps from "./interfaces/IChartProps";
import React from "react";
import ChartFactory from "./lib/ChartFactory";

const Chart = (props: IChartProps) => {
    const { data, dimensions, chart } = props;
    const svgWidth = dimensions.margin.left + dimensions.margin.right + dimensions.width;
    const svgHeight = dimensions.margin.top + dimensions.margin.bottom + dimensions.height;
    const svgRef = React.useRef(null);

    React.useEffect(() => {
        const c = ChartFactory(chart, ({
            ...props,
            svgRef: svgRef
        }));
    }, [data]);

    return <svg ref={svgRef} width={svgWidth} height={svgHeight} />;
}

export default Chart;
