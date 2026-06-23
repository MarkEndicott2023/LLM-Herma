> Source: https://tailwindcss.com/docs/adding-custom-styles — Tailwind CSS official docs (curriculum extract, fetched 2026-06-17)

# Adding Custom Styles

Best practices for adding your own custom styles in Tailwind projects.

## Customizing your theme

Change your color palette, spacing scale, typography scale, or breakpoints with the `@theme` directive:

```css
@theme {
  --font-display: "Satoshi", "sans-serif";
  --breakpoint-3xl: 120rem;
  --color-avocado-500: oklch(0.84 0.18 117.33);
  --ease-fluid: cubic-bezier(0.3, 0, 0, 1);
  --ease-snappy: cubic-bezier(0.2, 0, 0, 1);
}
```

## Using arbitrary values

When you need a one-off value, use square-bracket notation to generate a class on the fly:

```html
<div class="top-[117px]"></div>
<div class="top-[117px] lg:top-[344px]"></div>
<div class="bg-[#bada55] text-[22px] before:content-['Festivus']"></div>
```

Reference a CSS variable with the custom-property shorthand (`fill-(--my-brand-color)` = `fill-[var(--my-brand-color)]`).

### Arbitrary properties

For a CSS property with no utility, use square-bracket notation:

```html
<div class="[mask-type:luminance] hover:[mask-type:alpha]"></div>
<div class="[--scroll-offset:56px] lg:[--scroll-offset:44px]"></div>
```

### Arbitrary variants

On-the-fly selector modification:

```html
<li class="lg:[&:nth-child(-n+3)]:hover:underline">{item}</li>
```

### Handling whitespace

Use an underscore (`_`) for spaces; Tailwind converts it at build time:

```html
<div class="grid grid-cols-[1fr_500px_2fr]"></div>
```

Underscores are preserved where spaces are invalid (e.g. URLs `bg-[url('/what_a_rush.png')]`). Escape a literal underscore with `\_`. In JSX use `String.raw` so the backslash survives.

### Resolving ambiguities

Tailwind usually infers the type (`text-[22px]` → font-size, `text-[#bada55]` → color). When ambiguous (e.g. CSS variables), hint the type:

```html
<div class="text-(length:--my-var)">...</div>
<div class="text-(color:--my-var)">...</div>
```

## Using custom CSS

You can always just write plain CSS:

```css
@import "tailwindcss";

.my-custom-style { /* ... */ }
```

### Adding base styles

For page defaults, add classes to `html`/`body`:

```html
<html lang="en" class="bg-gray-100 font-serif text-gray-900"><!-- ... --></html>
```

Or use the `base` layer for element defaults:

```css
@layer base {
  h1 { font-size: var(--text-2xl); }
  h2 { font-size: var(--text-xl); }
}
```

### Adding component classes

Use the `components` layer for classes you still want to be able to override with utilities (`card`, `btn`, `badge`):

```css
@layer components {
  .card {
    background-color: var(--color-white);
    border-radius: var(--radius-lg);
    padding: --spacing(6);
    box-shadow: var(--shadow-xl);
  }
}
```

```html
<!-- Looks like a card, but with square corners -->
<div class="card rounded-none"><!-- ... --></div>
```

### Using variants

Apply a Tailwind variant within custom CSS with `@variant`:

```css
.my-element {
  background: white;
  @variant dark { background: black; }
}
```

Stack (`@variant hover:focus { ... }`) or comma-separate (`@variant hover, focus { ... }`) variants.

## Adding custom utilities

### Simple utilities

```css
@utility content-auto {
  content-visibility: auto;
}
```

Works with variants (`hover:content-auto`, `lg:content-auto`).

### Complex utilities

```css
@utility scrollbar-hidden {
  &::-webkit-scrollbar { display: none; }
}
```

### Functional utilities

Register utilities that accept an argument with the `--value()` function:

```css
@utility tab-* {
  tab-size: --value(--tab-size-*);     /* match theme keys */
}
```

- **Matching theme values** — `--value(--tab-size-*)` resolves against theme keys (`tab-2`, `tab-github`).
- **Bare values** — `--value(integer)` matches `tab-1`, `tab-76`. Types: `number`, `integer`, `ratio`, `percentage`.
- **Literal values** — `--value("inherit", "initial", "unset")`.
- **Arbitrary values** — `--value([integer])` matches `tab-[76]`. Many arbitrary types (`color`, `length`, `url`, etc.).
- **Combine all three** — list multiple declarations; failed resolutions are omitted:

```css
@utility opacity-* {
  opacity: --value([percentage]);
  opacity: calc(--value(integer) * 1%);
  opacity: --value(--opacity-*);
}
```

- **Default values** — `--value(integer, --default(4))` so `tab` works without an explicit value.
- **Negative values** — register separate `-inset-*` utilities multiplying by `-1`.
- **Modifiers** — `--modifier(--leading-*, [length], [*])` operates on the `/value` modifier.
- **Fractions** — use the `ratio` data type: `aspect-ratio: --value(--aspect-ratio-*, ratio, [ratio]);`.

## Adding custom variants

```css
@custom-variant theme-midnight {
  &:where([data-theme="midnight"] *) { @slot; }
}
```

Shorthand when nesting isn't required:

```css
@custom-variant theme-midnight (&:where([data-theme="midnight"] *));
```

Multiple rules can be nested:

```css
@custom-variant any-hover {
  @media (any-hover: hover) {
    &:hover { @slot; }
  }
}
```
