import IFigureDataPoint from "./IFigureDataPoint";

interface ITimeBasedDataPoint extends IFigureDataPoint{
    x: Date;
}

export default ITimeBasedDataPoint;
