import * as d3 from 'd3';
import IFigureProps from "./IFigureProps";
import IFigureDataPoint from "./IFigureDataPoint";

export default interface IFigure {
    new(props: IFigureProps): IFigure;
    draw: (svg: d3.Selection<SVGElement, IFigureDataPoint[], HTMLElement, undefined>) => void;
}