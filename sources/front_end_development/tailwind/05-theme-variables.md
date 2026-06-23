> Source: https://tailwindcss.com/docs/theme — Tailwind CSS official docs (curriculum extract, fetched 2026-06-17)

# Theme variables

## Overview

Tailwind is a framework for building custom designs. Low-level design decisions (typography, colors, shadows, breakpoints) are often called _design tokens_, and in Tailwind you store those values in _theme variables_.

### What are theme variables?

Theme variables are special CSS variables defined using the `@theme` directive that influence which utility classes exist in your project. For example, define a new color:

```css
@import "tailwindcss";

@theme {
  --color-mint-500: oklch(0.72 0.11 178);
}
```

Now you can use `bg-mint-500`, `text-mint-500`, or `fill-mint-500`. Tailwind also generates regular CSS variables so you can reference tokens in arbitrary values or inline styles: `style="background-color: var(--color-mint-500)"`.

#### Why `@theme` instead of `:root`?

Theme variables aren't _just_ CSS variables — they also instruct Tailwind to create new utility classes. Use `@theme` when you want a design token to map directly to a utility class; use `:root` for regular CSS variables that shouldn't have corresponding utilities. Theme variables must be defined top-level (not nested under selectors/media queries).

### Relationship to utility classes

Some utilities (`flex`, `object-cover`) are static. Many others are driven by theme variables. For example, `--font-*` variables determine all `font-family` utilities:

```css
@theme {
  --font-poppins: Poppins, sans-serif;
}
```

```html
<h1 class="font-poppins">This headline will use Poppins.</h1>
```

#### Relationship to variants

Some theme variables define variants rather than utilities. `--breakpoint-*` determines responsive breakpoint variants:

```css
@theme {
  --breakpoint-3xl: 120rem;
}
```

```html
<div class="3xl:grid-cols-6 grid grid-cols-2 md:grid-cols-4"><!-- ... --></div>
```

### Theme variable namespaces

| Namespace | Utility classes |
|-----------|-----------------|
| `--color-*` | Color utilities like `bg-red-500`, `text-sky-300` |
| `--font-*` | Font family utilities like `font-sans` |
| `--text-*` | Font size utilities like `text-xl` |
| `--font-weight-*` | Font weight utilities like `font-bold` |
| `--tracking-*` | Letter spacing utilities like `tracking-wide` |
| `--leading-*` | Line height utilities like `leading-tight` |
| `--breakpoint-*` | Responsive breakpoint variants like `sm:*` |
| `--container-*` | Container query variants `@sm:*` and size utilities like `max-w-md` |
| `--spacing-*` | Spacing and sizing utilities like `px-4`, `max-h-16` |
| `--radius-*` | Border radius utilities like `rounded-sm` |
| `--shadow-*` | Box shadow utilities like `shadow-md` |
| `--blur-*` | Blur filter utilities like `blur-md` |
| `--aspect-*` | Aspect ratio utilities like `aspect-video` |
| `--ease-*` | Transition timing utilities like `ease-out` |
| `--animate-*` | Animation utilities like `animate-spin` |

(Plus `--inset-shadow-*`, `--drop-shadow-*`, `--perspective-*`, `--zoom-*`, `--tab-size-*`.)

### Default theme variables

When you `@import "tailwindcss"`, you're importing:

```css
@layer theme, base, components, utilities;
@import "./theme.css" layer(theme);
@import "./preflight.css" layer(base);
@import "./utilities.css" layer(utilities);
```

`theme.css` includes the default color palette, type scale, shadows, fonts, etc. — which is why `bg-red-200`, `font-serif`, `shadow-sm` exist out of the box.

## Customizing your theme

### Extending the default theme

```css
@theme {
  --font-script: Great Vibes, cursive;
}
```

### Overriding the default theme

```css
@theme {
  --breakpoint-sm: 30rem;   /* sm:* now triggers at 30rem */
}
```

To override an entire namespace, set it to `initial` with the asterisk syntax:

```css
@theme {
  --color-*: initial;
  --color-white: #fff;
  --color-purple: #3f3cbb;
  --color-midnight: #121063;
}
```

### Using a custom theme (disable defaults)

```css
@theme {
  --*: initial;
  --spacing: 4px;
  --font-body: Inter, sans-serif;
  --color-lagoon: oklch(0.72 0.11 221.19);
}
```

### Defining animation keyframes

```css
@theme {
  --animate-fade-in-scale: fade-in-scale 0.3s ease-out;

  @keyframes fade-in-scale {
    0%   { opacity: 0; transform: scale(0.95); }
    100% { opacity: 1; transform: scale(1); }
  }
}
```

### Referencing other variables (`inline`)

```css
@theme inline {
  --font-sans: var(--font-inter);
}
```

Using `inline`, the utility uses the variable _value_ rather than referencing the variable — avoiding resolution surprises where `var()` resolves where it's defined, not where it's used.

### Generating all CSS variables (`static`)

```css
@theme static {
  --color-primary: var(--color-red-500);
  --color-secondary: var(--color-blue-500);
}
```

### Sharing across projects

Put shared theme variables in their own CSS file and `@import` it in each project (can even be published to NPM).

## Using your theme variables

All theme variables become regular CSS variables (`:root { --font-sans: ...; --color-red-50: ...; }`) when compiled.

- **With custom CSS** — `font-size: var(--text-base); color: var(--color-gray-700);`
- **With arbitrary values** — `rounded-[calc(var(--radius-xl)-1px)]`
- **In JavaScript** — use the CSS variables directly (e.g. Motion: `animate={{ backgroundColor: "var(--color-blue-500)" }}`), or `getComputedStyle(document.documentElement).getPropertyValue("--shadow-xl")` for a resolved value.
