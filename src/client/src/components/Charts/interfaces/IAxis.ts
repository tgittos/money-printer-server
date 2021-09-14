import * as d3 from "d3";
import {Axis, AxisScale} from "d3";
import IFigureDataPoint from "./IFigureDataPoint";

export default interface IAxis<T extends IFigureDataPoint> {
    scale: AxisScale<any>;
    axis: Axis<any>;

    draw: (svg: d3.Selection<SVGElement, T[], HTMLElement, undefined>) => void;
}