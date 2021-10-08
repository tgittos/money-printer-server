## Account Chip

```jsx padded
import AccountChip from './Components/AccountChip';
import Account from './../../models/Account';
import {accounts} from './../../guidebook/data';
import {Container} from "react-bootstrap";

<Container>
  {accounts.map(account =>
      <AccountChip key={account.id} account={account}/>
  )}
</Container>
```

## Account Tile

```jsx
import AccountTile from './Components/AccountTile';
import Account from './../../models/Account';
import { accounts } from './../../guidebook/data';

<AccountTile account={accounts[0]} />
```