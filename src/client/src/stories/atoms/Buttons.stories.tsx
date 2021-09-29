import 'bootstrap/dist/css/bootstrap.min.css';
import './../../mp-theme.scss'

import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import {Button} from "react-bootstrap";

export default {
    title: 'Components/atoms/Buttons',
    component: Button,
} as ComponentMeta<typeof Button>;

const Template: ComponentStory<typeof Button> = (args) => <Button {...args} />;

export const Standard = Template.bind({});
Standard.args = {
    children: <span>Button Text</span>
}
