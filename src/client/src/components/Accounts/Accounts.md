## Account Chip

```jsx padded
import AccountChip from './Components/AccountChip';
import Account from './../../models/Account';
import {accounts, balanceHistoryGenerator} from './../../guidebook/data';
import {Container} from "react-bootstrap";

<>
    <AccountChip account={accounts[0]} balanceHistory={balanceHistoryGenerator(accounts[0])}/>
    <AccountChip account={accounts[1]}/>
    <AccountChip account={accounts[2]} balanceHistory={balanceHistoryGenerator(accounts[2])} />
</>
```

## Account Tile

```jsx
import AccountTile from './Components/AccountTile';
import Account from './../../models/Account';
import { accounts, balanceHistoryGenerator } from './../../guidebook/data';

<AccountTile account={accounts[0]} balanceHistory={balanceHistoryGenerator(accounts[0])} />
```