import IChartProps from "../interfaces/IChartProps";

export interface IChartFactory {
    new(props: IChartProps): IChart;
}

export interface IChart {
}

export const createChart = (chartFactory: IChartFactory, props: IChartProps): IChart => {
    return new chartFactory(props);
}

export default createChart;
