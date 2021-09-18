import IChartDimensions from "./IChartDimensions";
import IFigureDataPoint from "./IFigureDataPoint";

interface IFigureProps {
    name?: string;
    data: IFigureDataPoint[];
    xScale?: any;
    yScale?: any;
    colorScale?: any;
    dimensions: IChartDimensions
}

export default IFigureProps;
