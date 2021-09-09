import IChartDimensions from "./IChartDimensions";

interface IFigureProps {
    data: Symbol[];
    xScale: any;
    yScale: any;
    dimensions: IChartDimensions
}

export default IFigureProps;
