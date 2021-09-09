import Symbol from "../../../models/Symbol";
import IChartDimensions from "./IChartDimensions";

interface IAxisProps {
    data: Symbol[];
    dimensions: IChartDimensions;
}

export default IAxisProps;