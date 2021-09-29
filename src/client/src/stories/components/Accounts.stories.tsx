import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';

import Accounts from '../../components/Accounts/Accounts';
import Account from '../../models/Account';

export default {
    title: 'Components/Accounts',
    component: Accounts,
} as ComponentMeta<typeof Accounts>;

const Template: ComponentStory<typeof Accounts> = (args) => <Accounts {...args} />;

export const EmptyState = Template.bind({});
EmptyState.args = {
    accounts: []
};

/*
{"data":[],"success":true}

 */

const accountsData = [
    { "id":1, "name":"Plaid Checking", "official_name":"Plaid Gold Standard 0% Interest Checking", "profile_id":4, "subtype":"checking","timestamp":"2021-09-13T10:28:12","balance": 110.00},
    {"id":2,"name":"Plaid Saving","official_name":"Plaid Silver Standard 0.1% Interest Saving","profile_id":4,"subtype":"savings","timestamp":"2021-09-13T10:31:54","balance": 110.00},
    {"id":3,"name":"Plaid CD","official_name":"Plaid Bronze Standard 0.2% Interest CD","profile_id":4,"subtype":"cd","timestamp":"2021-09-13T10:31:54","balance": 110.00},
    {"id":4,"name":"Plaid Credit Card","official_name":"Plaid Diamond 12.5% APR Interest Credit Card","profile_id":4,"subtype":"credit card","timestamp":"2021-09-13T10:31:54","balance": 110.00},
    {"id":5,"name":"Plaid Money Market","official_name":"Plaid Platinum Standard 1.85% Interest Money Market","profile_id":4,"subtype":"money market","timestamp":"2021-09-13T10:31:54","balance": 110.00},
    {"id":6,"name":"Plaid IRA","official_name":null,"profile_id":4,"subtype":"ira","timestamp":"2021-09-13T10:31:54","balance": 110.00},
    {"id":7,"name":"Plaid 401k","official_name":null,"profile_id":4,"subtype":"401k","timestamp":"2021-09-13T10:31:54","balance": 110.00},
    {"id":8,"name":"Plaid Student Loan","official_name":null,"profile_id":4,"subtype":"student","timestamp":"2021-09-13T10:31:54","balance": 110.00},
    {"id":9,"name":"Plaid Mortgage","official_name":null,"profile_id":4,"subtype":"mortgage","timestamp":"2021-09-13T10:31:54","balance": 110.00}
];

export const PopulatedState = Template.bind({});
PopulatedState.args = {
    accounts: accountsData.map(serverObj => new Account(serverObj))
};
