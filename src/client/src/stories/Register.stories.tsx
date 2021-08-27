import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';

import  Register from '../components/Register/Register';

export default {
    title: 'Components/Register',
    component: Register,
} as ComponentMeta<typeof Register>;

const Template: ComponentStory<typeof Register> = (args) => <Register {...args} />;

export const LoggedIn = Template.bind({});
LoggedIn.args = {
};

export const LoggedOut = Template.bind({});
LoggedOut.args = {
};

export const ErrorState = Template.bind({});
ErrorState.args = {

};
