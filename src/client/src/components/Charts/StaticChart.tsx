import IChartProps from "./interfaces/IChartProps";
import React from "react";
import ChartFactory from "./lib/ChartFactory";
import {Dropdown} from "react-bootstrap";

const StaticChart = (props: IChartProps<any>) => {
    const { data, dimensions, chart, className } = props;
    const svgWidth = dimensions.margin.left + dimensions.margin.right + dimensions.width;
    const svgHeight = dimensions.margin.top + dimensions.margin.bottom + dimensions.height;
    const svgRef = React.useRef(null);

    let s = ['mp-chart'];
    if (className) { s = s.concat(Array.of(className)) }

    React.useEffect(() => {
        const c = ChartFactory(chart, ({
            ...props,
            svgRef: svgRef
        }));
    }, [data, chart]);

    return <svg className={s.join(' ')} ref={svgRef} width={svgWidth} height={svgHeight} />;
}

export default StaticChart;
