import 'bootstrap/dist/css/bootstrap.min.css';
import '../../mp-theme.scss'

import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';

import HoldingsList from "../../components/Investments/HoldingsList/HoldingsList";
import Account, {IAccount} from "../../models/Account";
import moment from "moment";
import HoldingListItem from "../../components/Investments/HoldingsList/HoldingListItem";
import Holding, {IHolding} from "../../models/Holding";
import {IHistoricalEoDSymbol} from "../../models/symbols/HistoricalEoDSymbol";

export default {
    title: 'Components/HoldingsList',
    component: HoldingsList,
} as ComponentMeta<typeof HoldingsList>;

const fakeAccount = {
    id: 1,
    name: "Fake Account",
    balance: 100000,
    type: "investment",
    subtype: "401k",
    timestamp: moment.utc().toDate()
} as IAccount

const Template: ComponentStory<typeof HoldingsList> = (args) =>
    <HoldingsList
        account={fakeAccount}
        onActiveChanged={(holding) => {}}
        {...args} />;

const ListItemTemplate: ComponentStory<typeof HoldingListItem> = (args) =>
    <HoldingListItem
        account={fakeAccount}
        active={false}
        {...args} />;

const fakeHoldings = [{
    id: 1,
    accountId: fakeAccount.id,
    securitySymbol: 'AMZN',
    costBasis: 2500,
    quantity: 100,
    isoCurrencyCode: 'USD',
    timestamp: moment.utc().toDate()
}, {
    id: 2,
    accountId: fakeAccount.id,
    securitySymbol: 'GOOG',
    costBasis: 1000,
    quantity: 100,
    isoCurrencyCode: 'USD',
    timestamp: moment.utc().toDate()
}];

export const Unpopulated = Template.bind({});
Unpopulated.args = {
    holdings: []
};

export const LoadingListItem = ListItemTemplate.bind({});
LoadingListItem.args = {
    holding: new Holding(({
        securitySymbol: "FOO",
        accountId: fakeAccount.id,
        costBasis: 500.0,
        quantity: 10,
        _timestamp: moment.utc().toDate()
    } as unknown) as IHolding),
    latestPriceResolver: (holding: Holding) => new Promise<IHistoricalEoDSymbol>((resolver, rejector) => {
       // no-op - let the promise spin indefinitely to keep the component
       // in a loading state
    })
}

export const Populated = Template.bind({});
Populated.args = {
    holdings: fakeHoldings
};
