import Symbol from "../../../models/Symbol";
import IChartDimensions from "./IChartDimensions";
import {MutableRefObject} from "react";

export default interface IChartProps {
    svgRef: MutableRefObject<null>;
    data: Symbol[],
    dimensions: IChartDimensions;
}
