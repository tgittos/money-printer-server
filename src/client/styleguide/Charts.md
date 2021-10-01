Ahh, charts. The lifeblood of any financial application. A good chart can make or break a fintech application.

Luckily, I'm a chart geek. I love playing with D3 and visualizing data, and financial data is some of the funnest data
to visualize.

It's normally kind of painful to get D3 charts working in React, so the MP codebase abstracts most of the junk that
it can to just leave you to render great looking charts.

## Working with Charts

There are a series of basic `Chart` types that are containers that define the behavior of the chart you're rendering:

- `StaticChart`
- `LiveChart`
- `DynamicChart`
- `SparklineChart`

These components are wrappers for the actual chart that you want to render, and alter how the chart renders and the
user interactions available.

Once you've picked a chart wrapper, you get to pick an actual chart to render. The following charts are available by
default without needing to build anything new:

- `BasicLineChart`
- `BasicCandleChart`
- `PieChart`

These charts contain all the needed information to render themselves given a valid dataset.

Obviously we're not going to be able to cover all charting use cases with basic default charts, so there's also a robust
library for creating new charts that abstracts away some D3 nonsense.

### Containers

#### `StaticChart`

#### `LiveChart`

#### `DynamicChart`

#### `SparklineChart`

### Charts

#### `BasicLineChart`

#### `BasicCandleChart`

#### `PieChart`

## Developing New Charts

### Axes

### Figures

### The `ChartFactory`