import IFigureDataPoint from "./IFigureDataPoint";

interface ILineDataPoint extends IFigureDataPoint {
    x: Date
    y: number | undefined | null
}

export default ILineDataPoint;
