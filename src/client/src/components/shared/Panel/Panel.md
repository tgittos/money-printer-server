The `Panel` is one of the structural building blocks of Money Printer. Almost all UI elements are wrapped in panels.

They help give a consistent "wireframe" style across the application.

```jsx
import Panel from './Panel';

<Panel>
  <p>A simple panel that can hold any child elements.</p>
</Panel>
```

```jsx
import Panel from './Panel';

<Panel>
  <Panel.Header>
    A Panel with a Title
  </Panel.Header>
  <Panel.Body>
      <p>A simple panel with a title that can hold any child elements.</p>
  </Panel.Body>
</Panel>
```

```jsx
import Panel from './Panel';

<Panel>
  <p>A simple panel with a nested panel inside</p>
  <Panel>
    The nested panel content
  </Panel>
</Panel>
```

```jsx
import Panel from './Panel';

<Panel>
  <Panel.Header>
    Nested Panel with a Title
  </Panel.Header>
  <Panel.Body>
      <p>A simple panel with a title and a nested panel inside</p>
      <Panel>
        The nested panel content
      </Panel>
  </Panel.Body>
</Panel>
```

```jsx
import Panel from './Panel';

<Panel>
  <p>A simple panel with a title and a nested panel inside</p>
  <Panel>
    <Panel.Header>
      Nested Panel with Title
    </Panel.Header>
      <Panel.Body>
        The nested panel content
      </Panel.Body>
  </Panel>
</Panel>
```

```jsx
import Panel from './Panel';

<Panel>
  <Panel.Header>
    Nested Panel with a Title
  </Panel.Header>
    <Panel.Body>
  <p>A simple panel with a title and a nested panel inside</p>
  <Panel>
    <Panel.Header>
      Nested Panel with a Title
    </Panel.Header>
      <Panel.Body>
        The nested panel content
      </Panel.Body>
  </Panel>
    </Panel.Body>
</Panel>
```