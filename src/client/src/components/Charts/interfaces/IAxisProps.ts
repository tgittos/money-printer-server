import IChartDimensions from "./IChartDimensions";
import IFigureDataPoint from "./IFigureDataPoint";

interface IAxisProps<T extends IFigureDataPoint, U> {
    data: T[];
    dimensions: IChartDimensions;
    mapper?: (data: T, index: number, arr: Iterable<T>) => U;
}

export interface IAxisPropsNoMapper<T extends IFigureDataPoint> {
    data: T[];
    dimensions: IChartDimensions;
}


export default IAxisProps;