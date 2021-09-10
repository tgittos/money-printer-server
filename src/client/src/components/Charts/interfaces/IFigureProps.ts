import IChartDimensions from "./IChartDimensions";
import Symbol from "../../../models/Symbol";

interface IFigureProps {
    data: Symbol[];
    xScale: any;
    yScale: any;
    dimensions: IChartDimensions
}

export default IFigureProps;
