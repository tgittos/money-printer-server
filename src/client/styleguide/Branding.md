## Colors

Green is the color of money, baby! The primary design palette of Money Printer is dominated by the green spectrum, with
additional complementary shades from the violet and orange families and splashes of yellow and blue.

The design "vibe" of Money Printer is kind of "digital cyberpunk'. We're big fans of minimalist UI design that fades
away from the data, making it the star of the application.

## Primary Palette

The primary palette is where the coloring for large and important visual elements should be selected from. Most of the
colors from this palette should work well together, just don't go creating a rainbow vomit mess.

```js noeditor
```

## Secondary Palette

The secondary palette is for drawing attention to various elements in the design. These colors are used to bring attention
to elements of the design. Think button state during interactions, alert notifications, etc.

```js noeditor
```

## Grey Palette

Grey goes with everything. Here are some greys we like.

```js noeditor
import ColorChip from '../src/styleguide/components/ColorChip';
import vars from './../public/styles/_variables.module.scss';

<>
    <ColorChip name="$mp-white" value={vars.mpWhite}/>
    <ColorChip name="$mp-grey1" value={vars.mpGrey1}/>
    <ColorChip name="$mp-grey2" value={vars.mpGrey2}/>
    <ColorChip name="$mp-grey3" value={vars.mpGrey3}/>
    <ColorChip name="$mp-grey4" value={vars.mpGrey4}/>
    <ColorChip name="$mp-grey5" value={vars.mpGrey5}/>
    <ColorChip name="$mp-black" value={vars.mpBlack}/>
</>
```

## Role Variables

In order to keep the color theme consistent across the application, a number of role-specific color variables have been
defined. These include variables for primary and secondary borders, headers, highlights, etc.

## Spectrum

In the rare instances you want to use a color outside the primary, secondary or grey palettes, below is a selection of
vetted shades from the entire color spectrum. These shades are all selected to work well with each other and other
colors in the 


### Reds

```js noeditor
import ColorChip from '../src/styleguide/components/ColorChip';
import vars from './../public/styles/_variables.module.scss';

<>
</>
```

### Oranges

```js noeditor
import ColorChip from '../src/styleguide/components/ColorChip';
import vars from './../public/styles/_variables.module.scss';

<>
    <ColorChip name="$mp-blue-grey" value={vars.mpBlueGrey}/>
    <ColorChip name="$mp-blue" value={vars.mpBlue}/>
    <ColorChip name="$mp-light-blue" value={vars.mpLightBlue}/>
</>
```

### Yellows

```js noeditor
import ColorChip from '../src/styleguide/components/ColorChip';
import vars from './../public/styles/_variables.module.scss';

<>
    <ColorChip name="$mp-bright-yellow" value={vars.mpBrightYellow}/>
</>
```

### Greens

```js noeditor
import ColorChip from '../src/styleguide/components/ColorChip';
import vars from './../public/styles/_variables.module.scss';

<>
    <ColorChip name="$mp-green1" value={vars.mpGreen1}/>
    <ColorChip name="$mp-green2" value={vars.mpGreen2}/>
    <ColorChip name="$mp-green3" value={vars.mpGreen3}/>
    <ColorChip name="$mp-green4" value={vars.mpGreen4}/>
    <ColorChip name="$mp-green5" value={vars.mpGreen5}/>
    <ColorChip name="$mp-green6" value={vars.mpGreen6}/>
    <ColorChip name="$mp-green7" value={vars.mpGreen7}/>
    <ColorChip name="$mp-green8" value={vars.mpGreen8}/>
    <ColorChip name="$mp-green9" value={vars.mpGreen9}/>
    <ColorChip name="$mp-green10" value={vars.mpGreen10}/>
</>
```

### Blues

```js noeditor
import ColorChip from '../src/styleguide/components/ColorChip';
import vars from './../public/styles/_variables.module.scss';

<>
    <ColorChip name="$mp-bright-red" value={vars.mpBrightRed}/>
    <ColorChip name="$mp-red" value={vars.mpRed}/>
</>
```

### Indigos

### Violets


## Typography

## Iconography

## Pictography

## Interactions

## Theming

The design of Money Printer is intended to invoke feelings of retro-futurism and a general cyberpunk vibe. Finance is
changing, it's democratizing and digital currencies at least have a place at the table, if not dominate the future.

Using Money Printer to do something as dry as manage your financial future should feel fun, and this vibe is part of
that fun.

Not included as part of the stylesheet for this style guide are some affects that the theme applies to the body.

These are demonstrated below:

```jsx noeditor
import fx from "./../public/styles/_effects.module.scss";
import vars from "./../public/styles/_variables.module.scss";
import Panel from '../src/components/shared/Panel/Panel';

const s = { backgroundColor: vars.mpGreen1 };

<Panel className={fx.glow} style={s}>
  <p>A simple panel that can hold any child elements.</p>
  <p>Some more content to make the panel bigger.</p>
  <p>Try selecting some of the text.</p>
</Panel>
```