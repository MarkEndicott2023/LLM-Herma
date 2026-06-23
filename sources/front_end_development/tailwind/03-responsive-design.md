> Source: https://tailwindcss.com/docs/responsive-design — Tailwind CSS official docs (curriculum extract, fetched 2026-06-17)

# Responsive Design

Using responsive utility variants to build adaptive user interfaces.

## Overview

Every utility class in Tailwind can be applied conditionally at different breakpoints.

First, make sure you've added the [viewport meta tag](https://developer.mozilla.org/en-US/docs/Web/HTML/Viewport_meta_tag) to the `<head>`:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
```

To make a utility take effect only at a certain breakpoint, prefix it with the breakpoint name + `:`:

```html
<!-- Width of 16 by default, 32 on medium screens, and 48 on large screens -->
<img class="w-16 md:w-32 lg:w-48" src="..." />
```

There are five breakpoints by default:

| Breakpoint prefix | Minimum width | CSS |
|---|---|---|
| `sm` | 40rem _(640px)_ | `@media (width >= 40rem) { ... }` |
| `md` | 48rem _(768px)_ | `@media (width >= 48rem) { ... }` |
| `lg` | 64rem _(1024px)_ | `@media (width >= 64rem) { ... }` |
| `xl` | 80rem _(1280px)_ | `@media (width >= 80rem) { ... }` |
| `2xl` | 96rem _(1536px)_ | `@media (width >= 96rem) { ... }` |

Example component (stacked on small screens, side-by-side on larger):

```html
<div class="mx-auto max-w-md overflow-hidden rounded-xl bg-white shadow-md md:max-w-2xl">
  <div class="md:flex">
    <div class="md:shrink-0">
      <img class="h-48 w-full object-cover md:h-full md:w-48" src="/img/building.jpg" alt="Modern building architecture" />
    </div>
    <div class="p-8">
      <div class="text-sm font-semibold tracking-wide text-indigo-500 uppercase">Company retreats</div>
      <a href="#" class="mt-1 block text-lg leading-tight font-medium text-black hover:underline">Incredible accommodation for your team</a>
      <p class="mt-2 text-gray-500">Looking to take your team away on a retreat...</p>
    </div>
  </div>
</div>
```

## Working mobile-first

Tailwind uses a mobile-first breakpoint system. Unprefixed utilities (like `uppercase`) take effect on **all** screen sizes; prefixed utilities (like `md:uppercase`) take effect at the specified breakpoint _and above_.

### Targeting mobile screens

To style something for mobile, use the **unprefixed** version of a utility, not `sm:`. Don't think of `sm:` as "on small screens" — think of it as "at the small _breakpoint_".

```html
<!-- WRONG: only centers on screens 640px and wider -->
<div class="sm:text-center"></div>

<!-- RIGHT: center on mobile, left-align at 640px and up -->
<div class="text-center sm:text-left"></div>
```

Implement the mobile layout first, then layer on `sm`, `md`, etc.

### Targeting a breakpoint range

Stack a responsive variant with a `max-*` variant to limit a style to a range:

```html
<div class="md:max-xl:flex"><!-- ... --></div>
```

| Variant | Media query |
|---|---|
| `max-sm` | `@media (width < 40rem)` |
| `max-md` | `@media (width < 48rem)` |
| `max-lg` | `@media (width < 64rem)` |
| `max-xl` | `@media (width < 80rem)` |
| `max-2xl` | `@media (width < 96rem)` |

### Targeting a single breakpoint

Stack a responsive variant with the `max-*` variant for the next breakpoint: `md:max-lg:flex`.

## Using custom breakpoints

Use the `--breakpoint-*` theme variables:

```css
@import "tailwindcss";

@theme {
  --breakpoint-xs: 30rem;
  --breakpoint-2xl: 100rem;
  --breakpoint-3xl: 120rem;
}
```

Always use the **same unit** (Tailwind uses `rem`) so generated utilities sort correctly. Reset a breakpoint with `--breakpoint-2xl: initial;`, or reset all with `--breakpoint-*: initial;`. Use arbitrary one-offs with `min`/`max`: `max-[600px]:bg-sky-300 min-[320px]:text-center`.

## Container queries

[Container queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries) let you style something based on the size of a **parent element** instead of the viewport.

Mark an element as a container with `@container`, then use `@sm`, `@md`, etc. on children:

```html
<div class="@container">
  <div class="flex flex-col @md:flex-row"><!-- ... --></div>
</div>
```

- **Max-width container queries** — `@max-md:flex-col`
- **Ranges** — `@sm:@max-md:flex-col`
- **Named containers** — `@container/main` … `@sm/main:flex-col`
- **Size containers** — `@container-size` (for `cqb`/`cqh` units)
- **Custom sizes** — `--container-8xl: 96rem;` → `@8xl:flex-row`
- **Arbitrary** — `@min-[475px]:flex-row`
- **Container query units** — `w-[50cqw]`

Default container sizes range from `@3xs` (16rem) to `@7xl` (80rem).
