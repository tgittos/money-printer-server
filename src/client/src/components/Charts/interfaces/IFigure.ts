import * as d3 from 'd3';
import IFigureProps from "./IFigureProps";
import Symbol from "../../../models/Symbol";

export default interface IFigure {
    new(props: IFigureProps): IFigure;
    draw: (svg: d3.Selection<SVGElement, Symbol[], HTMLElement, undefined>) => void;
}