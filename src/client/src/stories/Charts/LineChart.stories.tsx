import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import BasicLineChart from "../../components/Charts/lib/charts/BasicLineChart";
import StaticChart from "../../components/Charts/StaticChart";
import IChartDimensions from "../../components/Charts/interfaces/IChartDimensions";
import ILineDataPoint from "../../components/Charts/interfaces/ILineDataPoint";
import moment from "moment";
import IChartMargin from "../../components/Charts/interfaces/IChartMargin";

export default {
    title: 'Components/Charts/LineChart',
    component: StaticChart,
} as ComponentMeta<typeof StaticChart>;

const Template: ComponentStory<typeof StaticChart> = (args) => <StaticChart
    chart={BasicLineChart}
    dimensions={{
        width: 1200,
        height: 800,
        margin: {
            top: 5,
            left: 35,
            right: 5,
            bottom: 45,
            left: 45
        } as IChartMargin
    } as IChartDimensions}
    {...args} />;

export const EmptyState = Template.bind({});
EmptyState.args = {
    data: []
};

function genData(gaps: boolean = false): ILineDataPoint[] {
    const fakeData: ILineDataPoint[] = [];
    const pointCount = 500;
    const basePrice = 50.0;
    const walkPct = 0.05;

    for (let i = pointCount; i >= 0; i--) {
        const lastDataPoint = fakeData[pointCount - i - 1];
        fakeData.push({
            x: moment().subtract(i, 'days').toDate(),
            y: lastDataPoint === undefined
                    ? basePrice
                    : Math.random() * 2 > 1
                        ? lastDataPoint.y + lastDataPoint.y * walkPct
                        : lastDataPoint.y - lastDataPoint.y * walkPct
        } as ILineDataPoint);
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
