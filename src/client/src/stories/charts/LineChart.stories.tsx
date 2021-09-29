import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import BasicLineChart from "../../components/Charts/lib/charts/BasicLineChart";
import StaticChart from "../../components/Charts/StaticChart";
import IChartDimensions from "../../components/Charts/interfaces/IChartDimensions";
import IChartMargin from "../../components/Charts/interfaces/IChartMargin";
import { lineGenerator } from "../data";

export default {
    title: 'Components/charts/LineChart',
    component: StaticChart,
} as ComponentMeta<typeof StaticChart>;

const Template: ComponentStory<typeof StaticChart> = (args) => <StaticChart
    chart={BasicLineChart}
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
    data: lineGenerator()
};

export const PartialDataState = Template.bind({});
PartialDataState.args = {
    data: lineGenerator(500, true)
}
