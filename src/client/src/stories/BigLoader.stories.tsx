import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';

import BigLoader from '../components/shared/Loaders/BigLoader';

export default {
    title: 'Components/BigLoader',
    component: BigLoader,
} as ComponentMeta<typeof BigLoader>;

const Template: ComponentStory<typeof BigLoader> = (args) => <BigLoader {...args} />;

export const Loading = Template.bind({});
Loading.args = {
};
