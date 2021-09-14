import IChartDimensions from "./IChartDimensions";
import {MutableRefObject} from "react";
import {IChartFactory} from "../lib/ChartFactory";

export default interface IChartProps<T> {
    chart: IChartFactory;
    svgRef?: MutableRefObject<null>;
    dimensions: IChartDimensions;
    data: T[];
}
