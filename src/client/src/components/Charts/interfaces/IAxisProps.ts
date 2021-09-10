import IChartDimensions from "./IChartDimensions";
import ISymbol from "../../../interfaces/ISymbol";

interface IAxisProps {
    data: ISymbol[];
    dimensions: IChartDimensions;
}

export default IAxisProps;