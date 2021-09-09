import {Axis, AxisScale} from "d3";

export default interface IAxis {
    scale: AxisScale<any>;
    axis: Axis<any>;
}