The `Panel` is one of the structural building blocks of Money Printer. Almost all UI elements are wrapped in panels.

They help give a consistent "wireframe" style across the application.

```js
import Panel from './Panel';

<Panel>
  <p>A simple panel that can hold any child elements.</p>
</Panel>
```

```js
import Panel from './Panel';

<Panel>
  <Panel.PanelHeader>
    A Panel with a Title
  </Panel.PanelHeader>
  <p>A simple panel with a title that can hold any child elements.</p>
</Panel>
```

```js
import Panel from './Panel';

<Panel>
  <p>A simple panel with a nested panel inside</p>
  <Panel>
    The nested panel content
  </Panel>
</Panel>
```

```js
import Panel from './Panel';

<Panel>
  <Panel.PanelHeader>
    Nested Panel with a Title
  </Panel.PanelHeader>
  <p>A simple panel with a title and a nested panel inside</p>
  <Panel>
    The nested panel content
  </Panel>
</Panel>
```

```js
import Panel from './Panel';

<Panel>
  <p>A simple panel with a title and a nested panel inside</p>
  <Panel>
    <Panel.PanelHeader>
      Nested Panel with Title
    </Panel.PanelHeader>
    The nested panel content
  </Panel>
</Panel>
```

```js
import Panel from './Panel';

<Panel>
  <Panel.PanelHeader>
    Nested Panel with a Title
  </Panel.PanelHeader>
  <p>A simple panel with a title and a nested panel inside</p>
  <Panel>
    <Panel.PanelHeader>
      Nested Panel with a Title
    </Panel.PanelHeader>
    The nested panel content
  </Panel>
</Panel>
```