The Money Printer application is really just a wrapper around a number of smaller sub-applications, each designed to
manage a single aspect of Money Printer.

To provide a cohesive UX experience between applications, Money Printer wraps each sub-app with a chrome, similar to how
a browser has chrome around the web page.

The chrome consists of two major components:

### MainNav

The `MainNav` is the main navigation component for the application. It renders a list of `MainNavItem` components and is
used to set the active app in the chrome.

```jsx
import MainNavItem from "./MainNav/components/MainNavItem";

<MainNavItem>
  Accounts
</MainNavItem>
```

### Header

The header is designed to hold components that provide the user with context-free, or multi-contextual data that is
relevant no matter which application is currently active.

There are currently 3 components inside the header, each designed to communicate something specific to the user.

#### Market Tracker

```jsx
import MarketTracker from "./Header/components/MarketTracker";

<MarketTracker />
```

#### Notifications Badge

```jsx padded
import NotificationsBadge from "./Header/components/NotificationsBadge";

<>
    <NotificationsBadge notificationCount={0} />
    <NotificationsBadge notificationCount={1000} />
</>
```

#### Profile Badge

The profile badge accepts callbacks that will allow consumers to hook into user requests and provide an implementation
that makes sense in the context of the app the user is currently in.

These methods should be passed down from the root `App`, which can then
orchestrate communicating the request down into the `Profile` application.

```jsx padded
import ProfileBadge from "./Header/components/ProfileBadge";

<>
    <ProfileBadge profile={{ first_name: 'Anonymous' }} />
    <ProfileBadge profile={{ first_name: 'Tim'}} authenticated={true} />
</>
```