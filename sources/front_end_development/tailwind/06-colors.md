> Source: https://tailwindcss.com/docs/colors — Tailwind CSS official docs (curriculum extract, fetched 2026-06-17). The full ~250-line OKLCH palette reference is summarized here; see the source for every exact value.

# Colors

Tailwind CSS includes a vast color palette out of the box.

## Color Palette Overview

Every color in the default palette includes 11 steps, with 50 being the lightest and 950 the darkest:

`50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950`

Available color families: red, orange, amber, yellow, lime, green, emerald, teal, cyan, sky, blue, indigo, violet, purple, fuchsia, pink, rose, slate, gray, zinc, neutral, stone, taupe, mauve, mist, olive (plus `black` and `white`).

```html
<div>
  <div class="bg-sky-50"></div>
  <div class="bg-sky-100"></div>
  ...
  <div class="bg-sky-900"></div>
  <div class="bg-sky-950"></div>
</div>
```

## Working with Colors

### Using Color Utilities

| Utility | Description |
|---------|-------------|
| `bg-*` | Background color |
| `text-*` | Text color |
| `decoration-*` | Text decoration color |
| `border-*` | Border color |
| `outline-*` | Outline color |
| `shadow-*` / `inset-shadow-*` | Box shadow color |
| `ring-*` / `inset-ring-*` | Ring shadow color |
| `accent-*` | Accent color of form controls |
| `caret-*` | Caret color in form controls |
| `fill-*` / `stroke-*` | SVG fill / stroke color |

### Adjusting Opacity

Use slash syntax `bg-black/75` (75% alpha):

```html
<div class="bg-sky-500/10"></div>
<div class="bg-sky-500/50"></div>
<div class="bg-sky-500/100"></div>
```

Also supports arbitrary values and CSS variable shorthand:

```html
<div class="bg-pink-500/[71.37%]"></div>
<div class="bg-cyan-400/(--my-alpha-value)"></div>
```

### Targeting Dark Mode

```html
<div class="bg-white dark:bg-gray-800 ...">...</div>
```

### Referencing in CSS

Colors are exposed as CSS variables in the `--color-*` namespace:

```css
@layer components {
  .typography {
    color: var(--color-gray-950);
    a {
      color: var(--color-blue-500);
      &:hover { color: var(--color-blue-800); }
    }
  }
}
```

Use as arbitrary values: `bg-[light-dark(var(--color-white),var(--color-gray-950))]`. Adjust opacity in CSS with the `--alpha()` function:

```css
.DocSearch-Hit--Result {
  background-color: --alpha(var(--color-gray-950) / 10%);
}
```

## Customizing Your Colors

### Adding Custom Colors

```css
@theme {
  --color-midnight: #121063;
  --color-tahiti: #3ab7bf;
  --color-bermuda: #78dcca;
}
```

Now `bg-midnight`, `text-tahiti`, `fill-bermuda` are available alongside the defaults.

### Overriding Default Colors

Redefine theme variables with the same name (e.g. all `--color-gray-*` steps).

### Disabling Default Colors

```css
@theme {
  --color-lime-*: initial;
  --color-fuchsia-*: initial;
}
```

### Using a Custom Palette

```css
@theme {
  --color-*: initial;
  --color-white: #fff;
  --color-purple: #3f3cbb;
  --color-midnight: #121063;
}
```

### Referencing Other Variables

```css
:root { --acme-canvas-color: oklch(0.967 0.003 264.542); }
[data-theme="dark"] { --acme-canvas-color: oklch(0.21 0.034 264.665); }

@theme inline {
  --color-canvas: var(--acme-canvas-color);
}
```

## Default Color Palette Reference

The default palette is defined as OKLCH values inside `@theme`. A representative excerpt (red family):

```css
@theme {
  --color-red-50:  oklch(97.1% 0.013 17.38);
  --color-red-100: oklch(93.6% 0.032 17.717);
  --color-red-500: oklch(63.7% 0.237 25.331);
  --color-red-700: oklch(50.5% 0.213 27.518);
  --color-red-950: oklch(25.8% 0.092 26.042);
  /* ...10 more families (orange, amber, yellow, lime, green, emerald, teal,
     cyan, sky, blue, indigo, violet, purple, fuchsia, pink, rose, slate, gray,
     zinc, neutral, stone, taupe, mauve, mist, olive), each with 11 steps... */
  --color-black: #000;
  --color-white: #fff;
}
```

(See the source page for every family and exact OKLCH value.)
