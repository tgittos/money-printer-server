import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';

import Login from '../../components/Login/Login';

export default {
    title: 'Components/Login',
    component: Login,
} as ComponentMeta<typeof Login>;

const Template: ComponentStory<typeof Login> = (args) => <Login {...args} />;

export const LoggedIn = Template.bind({});
LoggedIn.args = {
};

export const LoggedOut = Template.bind({});
LoggedOut.args = {
};
