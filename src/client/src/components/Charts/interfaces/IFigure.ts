import * as d3 from 'd3';
import IFigureProps from "./IFigureProps";
import ISymbol from "../../../interfaces/ISymbol";

export default interface IFigure {
    new(props: IFigureProps): IFigure;
    draw: (svg: d3.Selection<SVGElement, ISymbol[], HTMLElement, undefined>) => void;
}