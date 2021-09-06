import {ISymbol} from "../../../models/Symbol";
import {ScaleContinuousNumeric, ScaleLinear, ScaleLogarithmic} from "d3";

interface IAxisProps {
    data: ISymbol[];
    chartWidth: number;
    chartHeight: number;
    scale: ScaleLinear<any, any>;
}

export default IAxisProps;