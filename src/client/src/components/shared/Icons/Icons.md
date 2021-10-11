## Account Icon

```jsx
import AccountIcon from './AccountIcon';
import Account from "./../../../models/Account";

const account = new Account({
  id: 34523,
  name: "Retirment IRA",
  balance: 224352.0,
  type: "investment",
  subtype: "ira",
  timestamp: new Date()
});

<AccountIcon account={account}/>
```