## Containers

### Panel
The `Panel` is one of the structural building blocks of Money Printer. Almost all UI elements are wrapped in panels.

They help give a consistent "wireframe" style across the application.

A panel can be used as anything from a simple container:

```js
import Panel from '../src/components/shared/Panel/Panel';

<Panel>
  <p>A simple panel that can hold any child elements.</p>
</Panel>
```

All the way up to a full complex dashboard-like panel with control hooks:

```js
import Panel from '../src/components/shared/Panel/Panel';
import Button from "../src/components/shared/Button/Button";

<Panel>
  <Panel.Header>
    Nested Panel with a Title
    <Button>Click me</Button>
  </Panel.Header>
  <Panel.Body>
    <p>A panel with complex content wrapped in a `Panel.Body`</p>
    <Panel>
      <Panel.Header>
        Nested Panel with a Title
        <Button>Click me</Button>
      </Panel.Header>
      <Panel.Body>
        <p>The nested panel's complex content wrapped in a `Panel.Body`</p>
      </Panel.Body>
      <Panel.Footer>
        <Button>Click me</Button>
      </Panel.Footer>
    </Panel>
  </Panel.Body>
  <Panel.Footer>
    <Button>Click me</Button>
  </Panel.Footer>
</Panel>
```

Check the full documentation for the `Panel` component for details on full usage.