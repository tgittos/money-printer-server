The `Panel` is one of the structural building blocks of Money Printer. Almost all UI elements are wrapped in panels.

Panels are nestable and composable and work well with `Grid` and `Grid` sub-components.

You can use panels as just simple containers for content:

```jsx
import Panel from './Panel';

<Panel>
  <p>A simple panel that can hold any child elements.</p>
</Panel>
```

```jsx
import Panel from './Panel';

<Panel>
  <p>A simple panel with a nested panel inside</p>
  <Panel>
    <p>The nested panel content</p>
  </Panel>
</Panel>
```

You can give your panels a title bar to make them stand out. It's recommended that when using `Panel.Header`, you also
use `Panel.Body` to ensure the spacing is consistent. But you don't have to.

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
  <Panel.Header>
    Nested Panel with a Title
  </Panel.Header>
  <Panel.Body>
      <p>A simple panel with a title and a nested panel inside</p>
      <Panel>
        <p>The nested panel content</p>
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
        <p>The nested panel content</p>
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
            <p>The nested panel content</p>
          </Panel.Body>
      </Panel>
    </Panel.Body>
</Panel>
```

`Panel.Header` components accept a configuration for control buttons that appear in the top right.

There are a few default controls available, such as `Panel.Controls.Close` and `Panel.Controls.Minimize` that will
automatically provide the respective functionality to the panel.

Default controls include:

- `Panel.Header.Controls.Close`
- `Panel.Header.Controls.Maximize`
- `Panel.Header.Controls.Minimize`

However, you aren't limited to just the controls provided, you can supply any `IconButton` to the control as long as you
give it your own hooks:

```jsx
import {MdHelpOutline} from "react-icons/all";
import IconButton from "./../Button/IconButton";
import Panel from './Panel';

<Panel>
  <Panel.Header>
    Nested Panel with a Title
    <Panel.Header.Controls>
      <IconButton icon={MdHelpOutline} />
      <Panel.Header.Controls.Close/>
    </Panel.Header.Controls>
  </Panel.Header>
  <Panel.Body>
    <p>A simple panel</p>
  </Panel.Body>
</Panel>
```

Panels can also have a `Panel.Footer` element to encapsulate actions that are contextual to the content of the entire
panel:

```jsx
import Button from '../Button/Button';
import Panel from './Panel';

<Panel>
  <Panel.Body>
    <p>A simple with a control footer</p>
  </Panel.Body>
  <Panel.Footer>
    <Button primary>Ok</Button>
    <Button outline>Cancel</Button>
  </Panel.Footer>
</Panel>
```

This combination of `Panel`s, `Panel.Header`, `Panel.Body`, and `Panel.Footer` elements enable you to build a variety
of functional and expressive components:

```jsx
import { MdOutlineWarning } from 'react-icons/all';
import Button from '../Button/Button';
import Panel from './Panel';

<Panel>
  <Panel.Header>
    Sell order - selling at a loss
  </Panel.Header>
  <Panel.Body>
    <p>The holding that you're about to sell is currently at a -5.6% gain</p>
    <p>Are you sure you want to sell?</p>
  </Panel.Body>
  <Panel.Footer>
    <Button primary>Sell</Button>
    <Button outline>Cancel</Button>
  </Panel.Footer>
</Panel>
```

```jsx
import {BiBarChartAlt, BiBarChart, BiBarChartAlt2, BiX} from "react-icons/all";
import {CloseButton} from "react-bootstrap";
import Button from './../Button/Button';
import IconButton from './../Button/IconButton';
import Grid from './../Grid/Grid';
import Panel from './../Panel/Panel';
import Toolbar from './../Toolbar/Toolbar';
import StaticChart from "../Charts/StaticChart";
import BasicLineChart from "../Charts/lib/charts/BasicLineChart";
import {lineGenerator} from "../../../styleguide/data";

<Panel>
    <Panel.Header>
        <span> Return Analysis </span>
        <Panel.Header.Controls>
            <Panel.Header.Controls.Close/>
        </Panel.Header.Controls>
    </Panel.Header>
    <Panel.Body>
        <Toolbar>
            <IconButton icon={BiBarChart}/>
            <IconButton icon={BiBarChartAlt}/>
            <IconButton icon={BiBarChartAlt2}/>
        </Toolbar>
        <p>The security XYZ has achieved 10.3% returns over the last 90 days.</p>
        <StaticChart chart={BasicLineChart}
                     dimensions={{
                         width: 400,
                         height: 300,
                         margin: {
                             top: 0,
                             left: 35,
                             right: 0,
                             bottom: 25
                         }
                     }}
                     data={lineGenerator()}
        />
    </Panel.Body>
</Panel>
```
