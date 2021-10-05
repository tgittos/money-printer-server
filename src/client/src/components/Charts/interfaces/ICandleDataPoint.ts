import IFigureDataPoint from "./IFigureDataPoint";

interface ICandleDataPoint extends IFigureDataPoint {
    date: Date;
    high: number;
    low: number;
    open: number;
    close: number;
}

export default ICandleDataPoint;
