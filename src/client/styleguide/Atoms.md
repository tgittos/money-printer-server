## Buttons

#### Variants

Button appearance is controlled through passing in variant key works as props on the buttons.
Some variants change the color/border of the buttons:

- `primary`
- `secondary`
- `disabled`
- `outline`
- `link`

While others change the size of the buttons:

- `small`
- `medium`
- `large`
- `xl`
- `full`

Variants of different types can be mixed and matched (`primary small`), but the component default to the last specified
variant if multiple types conflict.

### Basic Button

Your basic, run-of-the-mill button with a variety of styled states:

```jsx padded
import Button from './../src/components/shared/Button/Button';

<>
  <Button primary>Primary</Button>
  <Button secondary>Secondary</Button>
  <Button disabled>Disabled</Button>
  <Button outline>Outline</Button>
  <Button link>Link</Button>
</>
```

#### Size Variants

```jsx padded
import Button from './../src/components/shared/Button/Button';

<>
  <Button small primary>Small</Button>
  <Button medium primary>Medium</Button>
  <Button large primary>Large</Button>
  <Button xl primary>Extra Large</Button>
  <Button full primary>Full Width</Button>
</>
```

The `medium` variant is the standard button variant, and if no size is given will be the size used.

### Icon Button

Sometimes a picture is worth 1,000 words. Icon buttons are probably worth a handful.

```jsx padded
import IconButton from './../src/components/shared/Button/IconButton';
import {BiBarChartAlt, BiBarChart, BiBarChartAlt2} from "react-icons/all";

<>
  <IconButton primary icon={BiBarChart} />
  <IconButton secondary icon={BiBarChart} />
  <IconButton disabled icon={BiBarChartAlt} />
  <IconButton x-large icon={BiBarChartAlt} />
  <IconButton link icon={BiBarChartAlt} />
</>
```

All the variants for the regular button work with the icon button.

## Toolbars

Toolbars are so extensively used in Money Printer that they're considered an atomic entity in the design.

The `Toolbar` component is designed to work with `Grid` and sub-class components, and will render an underlying `Row`
or `Col` component. You can use `Toolbar` components with `Grid` components as `Row`s and `Col`s, which should simplify
the placement of toolbars and keep the design consistent.


```jsx
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

```jsx
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
    <Toolbar>
      <IconButton icon={BiBarChart}/>
      <IconButton icon={BiBarChartAlt}/>
      <IconButton icon={BiBarChartAlt2}/>
    </Toolbar>
    <Grid>
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

```jsx
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
