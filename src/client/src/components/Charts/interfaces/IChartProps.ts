import Symbol from "../../../models/Symbol";
import IChartDimensions from "./IChartDimensions";

export default interface IChartProps {
    data: Symbol[],
    dimensions: IChartDimensions;
}
