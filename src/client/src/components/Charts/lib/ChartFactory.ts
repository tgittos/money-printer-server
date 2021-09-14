import IChartProps from "../interfaces/IChartProps";
import IChart from '../interfaces/IChart';

export interface IChartFactory {
    new(props: IChartProps<any>): IChart;
}

export const createChart = (chartFactory: IChartFactory, props: IChartProps<any>): IChart => {
    return new chartFactory(props);
}

export default createChart;
