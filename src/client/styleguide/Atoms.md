## Buttons

### Basic Button

Your basic, run of the mill button with a variety of styled states:

```jsx padded noeditor
import Button from './../src/components/shared/Button/Button';

<>
    <Button>Click me</Button>
    <Button disabled>Disabled</Button>
    <Button active>Active</Button>
</>
```

### Icon Button

Sometimes a picture is worth 1,000 words. Icon buttons are probably worth a handful.

```jsx padded noeditor
import IconButton from './../src/components/shared/Button/IconButton';
import {BiBarChartAlt, BiBarChart, BiBarChartAlt2} from "react-icons/all";

<>
    <IconButton primary icon={BiBarChart} />
    <IconButton disabled icon={BiBarChartAlt} />
    <IconButton active icon={BiBarChartAlt2} />
</>
```

## Toolbars

Toolbars are so extensively used in Money Printer that they're considered an atomic entity in the design.

The `Toolbar` component is designed to work with `Grid` and sub-class components, and will render an underlying `Row`
or `Col` component. You can use `Toolbar` components with `Grid` components as `Row`s and `Col`s, which should simplify
the placement of toolbars and keep the design consistent.


```jsx noeditor
import IconButton from './../src/components/shared/Button/IconButton';
import {BiBarChartAlt, BiBarChart, BiBarChartAlt2, BiX} from "react-icons/all";
import Grid from './../src/components/shared/Grid/Grid';
import Toolbar from './../src/components/shared/Toolbar/Toolbar';

<Grid>
  <Toolbar>
    <IconButton icon={BiBarChart}/>
    <IconButton icon={BiBarChartAlt}/>
    <IconButton icon={BiBarChartAlt2}/>
  </Toolbar>
</Grid>
```

### Horizontal Toolbar

```jsx noeditor
import Button from './../src/components/shared/Button/Button';
import IconButton from './../src/components/shared/Button/IconButton';
import {BiBarChartAlt, BiBarChart, BiBarChartAlt2, BiX} from "react-icons/all";
import Grid from './../src/components/shared/Grid/Grid';
import Panel from './../src/components/shared/Panel/Panel';
import Toolbar from './../src/components/shared/Toolbar/Toolbar';
import {CloseButton} from "react-bootstrap";

<Panel>
  <Panel.Header>
    <span>Tool panel header</span>
    <CloseButton />
  </Panel.Header>
  <Panel.Body>
    <Grid>
      <Toolbar>
        <IconButton icon={BiBarChart}/>
        <IconButton icon={BiBarChartAlt}/>
        <IconButton icon={BiBarChartAlt2}/>
      </Toolbar>
      <Grid.Row>
        <Grid.Col>
          Tool contents in here, which respond to buttons in the toolbar
        </Grid.Col>
      </Grid.Row>
    </Grid>
  </Panel.Body>
  <Panel.Footer>
    <Button primary>Ok</Button>
    <Button secondary>Cancel</Button>
  </Panel.Footer>
</Panel>
```

### Vertical Toolbar

```jsx noeditor
import Button from './../src/components/shared/Button/Button';
import IconButton from './../src/components/shared/Button/IconButton';
import {BiBarChartAlt, BiBarChart, BiBarChartAlt2, BiX} from "react-icons/all";
import Grid from './../src/components/shared/Grid/Grid';
import Panel from './../src/components/shared/Panel/Panel';
import Toolbar from './../src/components/shared/Toolbar/Toolbar';
import {CloseButton} from "react-bootstrap";

<Panel>
  <Panel.Header>
    <span>Tool panel header</span>
    <CloseButton />
  </Panel.Header>
  <Panel.Body>
    <Grid>
      <Grid.Row>
          <Toolbar orientation="vertical">
            <IconButton icon={BiBarChart}/>
            <IconButton icon={BiBarChartAlt}/>
            <IconButton icon={BiBarChartAlt2}/>
          </Toolbar>
        <Grid.Col>
          Tool contents in here, which respond to buttons in the toolbar
        </Grid.Col>
      </Grid.Row>
    </Grid>
  </Panel.Body>
  <Panel.Footer>
    <Button primary>Ok</Button>
    <Button secondary>Cancel</Button>
  </Panel.Footer>
</Panel>
```
