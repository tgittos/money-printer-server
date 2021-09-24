import 'bootstrap/dist/css/bootstrap.min.css';
import './../mp-theme.scss'

import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';

import Header from '../components/Header/Header';
import Profile, {IServerProfile} from "../models/Profile";

export default {
    title: 'Components/Header',
    component: Header,
} as ComponentMeta<typeof Header>;

const Template: ComponentStory<typeof Header> = (args) => <Header {...args} />;

export const LoggedIn = Template.bind({});
LoggedIn.args = {
    profile: new Profile({
        id: 1,
        first_name: "Gordon",
        last_name: "Gekko",
        email: "g.gecko@moneyprintergobrr.io",
        timestamp: new Date()
    } as IServerProfile),
    authenticated: true
};

export const LoggedOut = Template.bind({});
LoggedOut.args = {
    profile: new Profile({
        first_name: "Anonymous",
        last_name: "Money Printer",
        timestamp: new Date()
    } as IServerProfile),
    authenticated: false
};
