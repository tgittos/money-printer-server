import * as d3 from "d3";
import {Axis, AxisScale} from "d3";
import Symbol from "../../../models/Symbol";

export default interface IAxis {
    scale: AxisScale<any>;
    axis: Axis<any>;

    draw: (svg: d3.Selection<SVGElement, Symbol[], HTMLElement, undefined>) => void;
}