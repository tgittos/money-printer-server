import Symbol from "../../../models/Symbol";
import IChartDimensions from "./IChartDimensions";
import {MutableRefObject} from "react";
import BaseChart from "../lib/BaseChart";

export default interface IChartProps {
    chart: typeof BaseChart;
    svgRef: MutableRefObject<null>;
    data: Symbol[],
    dimensions: IChartDimensions;
}
