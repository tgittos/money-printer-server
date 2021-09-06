import Symbol from "../../../models/Symbol";
import IChartDimensions from "./IChartDimensions";
import {MutableRefObject} from "react";
import { IChart } from "../lib/BaseChart";

export default interface IChartProps {
    chart: IChart;
    svgRef: MutableRefObject<null>;
    data: Symbol[],
    dimensions: IChartDimensions;
}
