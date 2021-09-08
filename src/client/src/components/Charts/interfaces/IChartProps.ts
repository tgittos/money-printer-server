import Symbol from "../../../models/Symbol";
import IChartDimensions from "./IChartDimensions";
import {MutableRefObject} from "react";
import {IChart, IChartFactory} from "../lib/BaseChart";

export default interface IChartProps {
    chart: IChartFactory;
    svgRef: MutableRefObject<null>;
    data: Symbol[],
    dimensions: IChartDimensions;
}
