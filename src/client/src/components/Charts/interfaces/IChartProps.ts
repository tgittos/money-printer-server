import IChartDimensions from "./IChartDimensions";
import {MutableRefObject} from "react";
import {IChartFactory} from "../lib/ChartFactory";
import ISymbol from "../../../interfaces/ISymbol";

export default interface IChartProps {
    chart: IChartFactory;
    svgRef?: MutableRefObject<null>;
    dimensions: IChartDimensions;
    data: ISymbol[];
}
