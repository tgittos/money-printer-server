import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import StaticChart from "../../components/Charts/StaticChart";
import IChartDimensions from "../../components/Charts/interfaces/IChartDimensions";
import IChartMargin from "../../components/Charts/interfaces/IChartMargin";
import BasicCandleChart from "../../components/Charts/lib/charts/BasicCandleChart";
import { candleGenerator } from "./../data";

export default {
    title: 'Components/charts/CandleChart',
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

export const PopulatedState = Template.bind({});
PopulatedState.args = {
    data: candleGenerator()
};

export const PartialDataState = Template.bind({});
PartialDataState.args = {
    data: candleGenerator(500, true)
}
