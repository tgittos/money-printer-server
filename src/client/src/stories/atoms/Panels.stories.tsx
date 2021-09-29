import 'bootstrap/dist/css/bootstrap.min.css';
import './../../mp-theme.scss'

import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import Panel from "../../components/shared/Panel/Panel";

export default {
    title: 'Components/atoms/Panel',
    component: Panel,
} as ComponentMeta<typeof Panel>;

const Template: ComponentStory<typeof Panel> = (args) => <Panel {...args} />;

export const Single = Template.bind({});
Single.args = {
    children: <span>Content inside a panel</span>
}

export const SingleWithTitle = Template.bind({});
SingleWithTitle.args = {
    title: "Title",
    children: <span>Content inside a panel</span>
}

export const Nested = Template.bind({});
Nested.args = {
    children: <div>
        <Panel>
            <span>Content inside a nested panel</span>
        </Panel>
        <span>Content inside a panel</span>
    </div>
};

export const NestedWithTitle = Template.bind({});
NestedWithTitle.args = {
    title: "Title",
    children: <div>
        <Panel>
            <span>Content inside a nested panel</span>
        </Panel>
        <span>Content inside a panel</span>
    </div>
};
