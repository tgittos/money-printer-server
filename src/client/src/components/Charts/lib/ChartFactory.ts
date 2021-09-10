import IChartProps from "../interfaces/IChartProps";
import IChart from '../interfaces/IChart';

export interface IChartFactory {
    new(props: IChartProps): IChart;
}

export const createChart = (chartFactory: IChartFactory, props: IChartProps): IChart => {
    return new chartFactory(props);
}

export default createChart;
