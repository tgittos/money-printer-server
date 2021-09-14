import IFigureDataPoint from "./IFigureDataPoint";
import ITimeBasedDataPoint from "./ITimeBasedDataPoint";

interface ICandleDataPoint extends IFigureDataPoint, ITimeBasedDataPoint {
    high: number;
    low: number;
    open: number;
    close: number;
}

export default ICandleDataPoint;
