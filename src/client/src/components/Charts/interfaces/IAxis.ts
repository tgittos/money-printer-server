import * as d3 from "d3";
import {Axis, AxisScale} from "d3";
import ISymbol from "../../../interfaces/ISymbol";

export default interface IAxis {
    scale: AxisScale<any>;
    axis: Axis<any>;

    draw: (svg: d3.Selection<SVGElement, ISymbol[], HTMLElement, undefined>) => void;
}