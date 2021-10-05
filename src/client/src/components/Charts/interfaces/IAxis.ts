import * as d3 from "d3";
import {Axis, AxisDomain, AxisScale} from "d3";
import IFigureDataPoint from "./IFigureDataPoint";

export default interface IAxis {
    scale: AxisScale<AxisDomain>;
    domain: AxisDomain[];
    axis: Axis<AxisDomain>
    draw: (svg: d3.Selection<SVGElement, IFigureDataPoint[], HTMLElement, undefined>) => void;
}