import IFigureDataPoint from "./IFigureDataPoint";
import ITimeBasedDataPoint from "./ITimeBasedDataPoint";

interface ILineDataPoint extends IFigureDataPoint, ITimeBasedDataPoint {
    x: Date
    y: number | undefined | null
}

export default ILineDataPoint;
