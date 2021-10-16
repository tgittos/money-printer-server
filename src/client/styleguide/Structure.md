In order to enforce spacing rules across the Money Printer application, most UI elements are comprised of nested `Grid`
and `Panel` objects. `Panel`s can go inside `Grid`s, and `Grid`s can go inside `Panel`s.

This results in a pleasing and intentional 'boxy' look that goes hand in hand with the color philosphy to enforce the
design "vibe"

## Layout

The `Grid` is the basic organizational structural element, and is used to layout components and the content of components.

There are several specialized types of `Grid` to assist in common layout goals.

### Grid
```js noeditor
import Grid from '../src/components/shared/Grid/Grid';
import vars from '../public/styles/_variables.module.scss';

<Grid>
  <Grid.Row>
    <Grid.Col style={{backgroundColor: vars.mpGrey5}}>1 of 2</Grid.Col>
    <Grid.Col style={{backgroundColor: vars.mpGrey5}}>2 of 2</Grid.Col>
  </Grid.Row>
  <Grid.Row>
    <Grid.Col style={{backgroundColor: vars.mpGrey5}}>1 of 3</Grid.Col>
    <Grid.Col style={{backgroundColor: vars.mpGrey5}}>2 of 3</Grid.Col>
    <Grid.Col style={{backgroundColor: vars.mpGrey5}}>3 of 3</Grid.Col>
  </Grid.Row>
</Grid>
```

## Containers

### Panel
The `Panel` is one of the structural building blocks of Money Printer. Almost all UI elements are wrapped in panels.

They help give a consistent "wireframe" style across the application.

A panel can be used as anything from a simple container:

```js noeditor
import Panel from '../src/components/shared/Panel/Panel';

<Panel>
  <p>A simple panel that can hold any child elements.</p>
</Panel>
```

All the way up to a full complex dashboard-like panel with control hooks:

```js noeditor
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

