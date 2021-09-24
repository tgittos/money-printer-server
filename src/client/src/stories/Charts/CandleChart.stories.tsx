import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import StaticChart from "../../components/Charts/StaticChart";
import IChartDimensions from "../../components/Charts/interfaces/IChartDimensions";
import ILineDataPoint from "../../components/Charts/interfaces/ILineDataPoint";
import moment from "moment";
import IChartMargin from "../../components/Charts/interfaces/IChartMargin";
import BasicCandleChart from "../../components/Charts/lib/charts/BasicCandleChart";
import ICandleDataPoint from "../../components/Charts/interfaces/ICandleDataPoint";
import IFigureDataPoint from "../../components/Charts/interfaces/IFigureDataPoint";

export default {
    title: 'Components/Charts/CandleChart',
    component: StaticChart,
} as ComponentMeta<typeof StaticChart>;

const Template: ComponentStory<typeof StaticChart> = (args) => <StaticChart
    chart={BasicCandleChart}
    dimensions={{
        width: 1200,
        height: 800,
        margin: {
            top: 5,
            left: 45,
            right: 5,
            bottom: 45,
        } as IChartMargin
    } as IChartDimensions}
    {...args} />;

export const EmptyState = Template.bind({});
EmptyState.args = {
    data: []
};

const pointCount = 500;
const basePrice = 50.0;
const walkPct = 0.05;

function randomStep(arr: ICandleDataPoint[], valuator: (obj: ICandleDataPoint) => number) {
    const lastDataPoint = arr[arr.length-1];
    let lastValue = valuator(lastDataPoint);
    if (Math.random() * 2 > 1) {
        lastValue = lastValue + lastValue * walkPct
    } else {
        lastValue = lastValue - lastValue * walkPct
    }
    return lastValue;
}

function genData(gaps: boolean = false): ICandleDataPoint[] {
    const fakeData: ICandleDataPoint[] = [{
        date: moment().subtract(pointCount, 'days').toDate(),
        x: moment().subtract(pointCount, 'days').toDate(),
        open: 50,
        close: 50,
        high: 50,
        low: 50
    } as ICandleDataPoint];

    for (let i = pointCount; i > 0; i--) {
        fakeData.push({
            date: moment().subtract(i, 'days').toDate(),
            x: moment().subtract(i, 'days').toDate(),
            open: randomStep(fakeData, point => point.open),
            high: randomStep(fakeData, point => point.high),
            low: randomStep(fakeData, point => point.low),
            close: randomStep(fakeData, point => point.close)
        } as ICandleDataPoint);
    }

    if (gaps) {
        // randomly nuke some data points
        for (let i = 0; i < pointCount; i++){
            if (Math.random() * 20 < 1) {
                fakeData[i] = undefined;
            }
        }
    }

    return fakeData;
}

export const PopulatedState = Template.bind({});
PopulatedState.args = {
    data: genData()
};

export const PartialDataState = Template.bind({});
PartialDataState.args = {
    data: genData(true)
}
