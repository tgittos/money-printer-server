import {ISymbol} from "../../../models/Symbol";
import {ScaleLinear} from "d3";

interface IFigureProps {
    data: ISymbol[];
    xScale: ScaleLinear<any, any>;
    yScale: ScaleLinear<any, any>;
}

export default IFigureProps;
