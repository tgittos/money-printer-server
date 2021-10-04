import IChartProps from "./interfaces/IChartProps";
import React from "react";
import ChartFactory from "./lib/ChartFactory";
import {Dropdown} from "react-bootstrap";

const StaticChart = (props: IChartProps<any>) => {
    const { data, chart, className, dimensions } = props;
    const svgRef = React.useRef(null);

    let s = ['mp-chart'];
    if (className) { s = s.concat(Array.of(className)) }

    React.useEffect(() => {
        const svgBounding = svgRef.current.getBoundingClientRect();
        const realDims = Object.assign({}, dimensions, {
            width: svgBounding.width,
            height: svgBounding.height
        })
        const c = ChartFactory(chart, ({
            ...{
                ...props,
                dimensions: realDims
            },
            svgRef: svgRef
        }));
    }, [data, chart]);

    return <svg className={s.join(' ')} ref={svgRef} />;
}

export default StaticChart;
