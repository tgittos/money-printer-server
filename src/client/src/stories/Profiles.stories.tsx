import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';

import Profiles from '../components/Profiles/Profiles';

export default {
    title: 'Components/Profiles',
    component: Profiles,
} as ComponentMeta<typeof Profiles>;

const Template: ComponentStory<typeof Profiles> = (args) => <Profiles {...args} />;

export const LoggedIn = Template.bind({});
LoggedIn.args = {
};

export const LoggedOut = Template.bind({});
LoggedOut.args = {
};
