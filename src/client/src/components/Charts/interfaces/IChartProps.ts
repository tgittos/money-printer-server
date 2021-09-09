import Symbol from "../../../models/Symbol";
import IChartDimensions from "./IChartDimensions";
import {MutableRefObject} from "react";
import {IChartFactory} from "../lib/ChartFactory";
import IAxis from "./IAxis";
import IFigure from "./IFigure";

export default interface IChartProps {
    chart: IChartFactory;
    svgRef: MutableRefObject<null>;
    dimensions: IChartDimensions;
    xAxis: IAxis;
    yAxis: IAxis;
    data: Symbol[];
}
