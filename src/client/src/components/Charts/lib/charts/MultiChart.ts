import BaseChart from "../BaseChart";
import IChartDimensions from "../../interfaces/IChartDimensions";
import {ISymbol} from "../../../../models/Symbol";
import IChartProps from "../../interfaces/IChartProps";
import { IChart} from "../BaseChart";

interface MultiChartData {
    chart: typeof BaseChart;
    data: ISymbol[];
}

interface IMultiChartProps {
    dimensions: IChartDimensions;

}

class MultiChart extends BaseChart implements IChart {

    constructor(props: IMultiChartProps) {
        const { dimensions } = props;

        const superProps = {
            dimensions: dimensions
        } as IChartProps;
        super(superProps);
    }

    protected override _renderFigures() {
    }
}

export default MultiChart;
