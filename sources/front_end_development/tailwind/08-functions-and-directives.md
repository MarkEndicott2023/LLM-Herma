> Source: https://tailwindcss.com/docs/functions-and-directives — Tailwind CSS official docs (curriculum extract, fetched 2026-06-17)

# Functions and Directives

A reference for the custom functions and directives Tailwind exposes to your CSS.

## Directives

Directives are custom Tailwind-specific [at-rules](https://developer.mozilla.org/en-US/docs/Web/CSS/At-rule).

### @import

Inline-import CSS files, including Tailwind itself:

```css
@import "tailwindcss";
```

### @theme

Define custom design tokens (fonts, colors, breakpoints):

```css
@theme {
  --font-display: "Satoshi", "sans-serif";
  --breakpoint-3xl: 120rem;
  --color-avocado-500: oklch(0.84 0.18 117.33);
  --ease-fluid: cubic-bezier(0.3, 0, 0, 1);
}
```

### @source

Explicitly specify source files that aren't picked up by automatic content detection:

```css
@source "../node_modules/@my-company/ui-lib";
```

### @utility

Add custom utilities that work with variants like `hover`, `focus`, `lg`:

```css
@utility tab-4 {
  tab-size: 4;
}
```

### @variant

Apply a Tailwind variant to styles in your CSS:

```css
.my-element {
  background: white;
  @variant dark { background: black; }
}
```

### @custom-variant

Add a custom variant:

```css
@custom-variant theme-midnight (&:where([data-theme="midnight"] *));
```

### @apply

Inline existing utility classes into your own custom CSS — useful for overriding third-party libraries while still using your design tokens:

```css
.select2-dropdown {
  @apply rounded-b-lg shadow-md;
}
.select2-search {
  @apply rounded border border-gray-300;
}
```

### @reference

To use `@apply` or `@variant` in the `<style>` block of a Vue/Svelte component or in CSS modules, import your theme for reference _without_ duplicating CSS:

```vue
<style>
  @reference "../../app.css";
  h1 { @apply text-2xl font-bold text-red-500; }
</style>
```

If you're using the default theme with no customizations, you can `@reference "tailwindcss";` directly.

### Subpath Imports

With the CLI, Vite, or PostCSS, `@import`, `@reference`, `@plugin`, and `@config` support [subpath imports](https://nodejs.org/api/packages.html#subpath-imports):

```json
{ "imports": { "#app.css": "./src/css/app.css" } }
```

```vue
<style>
  @reference "#app.css";
  h1 { @apply text-2xl font-bold text-red-500; }
</style>
```

## Functions

Build-time functions for working with colors and the spacing scale.

### --alpha()

Adjust the opacity of a color:

```css
/* Input */
.my-element { color: --alpha(var(--color-lime-300) / 50%); }

/* Compiled */
.my-element { color: color-mix(in oklab, var(--color-lime-300) 50%, transparent); }
```

### --spacing()

Generate a spacing value based on your theme:

```css
/* Input */
.my-element { margin: --spacing(4); }

/* Compiled */
.my-element { margin: calc(var(--spacing) * 4); }
```

Useful in arbitrary values too: `py-[calc(--spacing(4)-1px)]`.

## Compatibility (Tailwind v3.x)

These exist solely for compatibility with v3.x:

### @config

Load a legacy JavaScript-based config file:

```css
@config "../../tailwind.config.js";
```

(The `corePlugins`, `safelist`, and `separator` options are not supported in v4.0.)

### @plugin

Load a legacy JavaScript-based plugin (package name or local path):

```css
@plugin "@tailwindcss/typography";
```

### theme()

Access theme values with dot notation (deprecated — prefer CSS theme variables):

```css
.my-element { margin: theme(spacing.12); }
```
