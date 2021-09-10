import IChartDimensions from "./IChartDimensions";
import ISymbol from "../../../interfaces/ISymbol";

interface IFigureProps {
    data: ISymbol[];
    xScale: any;
    yScale: any;
    dimensions: IChartDimensions
}

export default IFigureProps;
