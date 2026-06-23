> Source: https://tailwindcss.com/docs/hover-focus-and-other-states — Tailwind CSS official docs (curriculum extract, fetched 2026-06-17). The exhaustive per-pseudo-class example gallery and full variant reference table are trimmed here; see the source for the complete list.

# Hover, focus, and other states

Every utility class in Tailwind can be applied _conditionally_ by adding a variant to the beginning of the class name that describes the condition you want to target.

For example, to apply the `bg-sky-700` class on hover, use the `hover:bg-sky-700` class:

```html
<button class="bg-sky-500 hover:bg-sky-700 ...">Save changes</button>
```

## How does this compare to traditional CSS?

When writing CSS the traditional way, a single class name would do different things based on the current state:

```css
.btn-primary { background-color: #0ea5e9; }
.btn-primary:hover { background-color: #0369a1; }
```

In Tailwind, rather than adding the styles for a hover state to an existing class, you add another class to the element that _only_ does something on hover:

```css
.bg-sky-500 { background-color: #0ea5e9; }
.hover\:bg-sky-700:hover { background-color: #0369a1; }
```

Tailwind includes variants for just about everything, including:

- **Pseudo-classes** — `:hover`, `:focus`, `:first-child`, `:required`, etc.
- **Pseudo-elements** — `::before`, `::after`, `::placeholder`, `::selection`, etc.
- **Media and feature queries** — responsive breakpoints, dark mode, `prefers-reduced-motion`
- **Attribute selectors** — `[dir="rtl"]`, `[open]`, ARIA and data attributes
- **Child selectors** — `& > *`, `& *`

Variants can be stacked to target more specific situations, e.g. dark mode, at the medium breakpoint, on hover:

```html
<button class="dark:md:hover:bg-fuchsia-600 ...">Save changes</button>
```

## Pseudo-classes

### :hover, :focus, and :active

```html
<button class="bg-violet-500 hover:bg-violet-600 focus:outline-2 focus:outline-offset-2 focus:outline-violet-500 active:bg-violet-700 ...">
  Save changes
</button>
```

### :first, :last, :odd, and :even

```html
<li class="flex py-4 first:pt-0 last:pb-0">...</li>
<tr class="odd:bg-white even:bg-gray-50 dark:odd:bg-gray-900/50 dark:even:bg-gray-950">...</tr>
```

Use `nth-*` and `nth-last-*` for position-based styling: `nth-3:underline`, `nth-of-type-4:underline`, and arbitrary values like `nth-[2n+1_of_li]`.

### :required, :disabled, :invalid

```html
<input type="text" disabled
  class="invalid:border-pink-500 invalid:text-pink-600 focus:border-sky-500 focus:invalid:border-pink-500 disabled:border-gray-200 disabled:bg-gray-50 disabled:text-gray-500 ..." />
```

### :has()

Style an element based on the state or content of its descendants:

```html
<label class="has-checked:bg-indigo-50 has-checked:text-indigo-900 ...">
  Google Pay
  <input type="radio" class="checked:border-indigo-500 ..." />
</label>
```

Combine with `group-has-*` (descendants of a parent marked `group`) and `peer-has-*` (descendants of a sibling marked `peer`).

### :not()

```html
<button class="bg-indigo-600 hover:not-focus:bg-indigo-700">...</button>
<div class="not-supports-[display:grid]:flex">...</div>
```

### Styling based on parent state (`group`)

Mark the parent with `group`, then use `group-*` variants like `group-hover`:

```html
<a href="#" class="group ...">
  <svg class="stroke-sky-500 group-hover:stroke-white ..."></svg>
  <h3 class="text-gray-900 group-hover:text-white ...">New project</h3>
</a>
```

- **Named groups** — `group/item` … `group-hover/item:visible`
- **Arbitrary groups** — `group-[.is-published]:block`
- **Implicit groups** — `in-*` works like `group` without adding `group` to the parent: `in-focus:opacity-100`

### Styling based on sibling state (`peer`)

Mark the sibling with `peer`, then use `peer-*` variants like `peer-invalid`:

```html
<input type="email" class="peer ..." />
<p class="invisible peer-invalid:visible ...">Please provide a valid email address.</p>
```

Note: `peer` only works on _previous_ siblings (CSS subsequent-sibling combinator). Named peers (`peer/draft` … `peer-checked/draft:`) and arbitrary peers are supported.

## Pseudo-elements

- **::before / ::after** — `before:` and `after:` variants; Tailwind auto-adds `content: ''`. Example: `after:content-['*'] after:text-red-500`.
- **::placeholder** — `placeholder:text-gray-500 placeholder:italic`
- **::file** — style the file input button: `file:mr-4 file:rounded-full file:bg-violet-50 ...`
- **::marker** — list bullets/counters: `marker:text-sky-400` (inheritable)
- **::selection** — `selection:bg-fuchsia-300 selection:text-fuchsia-900` (inheritable)
- **::first-line / ::first-letter** — `first-letter:float-left first-letter:text-7xl`, `first-line:uppercase`
- **::backdrop** — `<dialog>` backdrop: `backdrop:bg-gray-50`

## Media and feature queries

- **Responsive breakpoints** — `md:`, `lg:`; container queries with `@container` + `@md:`, `@lg:`
- **prefers-color-scheme** — `dark:` variant
- **prefers-reduced-motion** — `motion-reduce:` and `motion-safe:`
- **prefers-contrast** — `contrast-more:` and `contrast-less:`
- **forced-colors** — `forced-colors:` and `not-forced-colors:`
- **pointer / any-pointer** — `pointer-fine`, `pointer-coarse`, `pointer-none` (larger touch targets, etc.)
- **orientation** — `portrait:`, `landscape:`
- **scripting** — `noscript:`
- **print** — `print:hidden`, `hidden print:block`
- **@supports** — `supports-[display:grid]:grid`, shorthand `supports-backdrop-filter:`
- **@starting-style** — `starting:` for entry transitions / `display: none` → visible

## Attribute selectors

- **ARIA states** — `aria-checked:bg-sky-700`; built-in boolean variants (`aria-busy`, `aria-checked`, `aria-disabled`, `aria-expanded`, `aria-hidden`, `aria-pressed`, `aria-readonly`, `aria-required`, `aria-selected`); arbitrary: `aria-[sort=ascending]:bg-[url(...)]`
- **Data attributes** — `data-active:border-purple-500` (presence), `data-[size=large]:p-8` (value), custom: `@custom-variant data-checked (&[data-ui~="checked"])`
- **RTL support** — `rtl:` and `ltr:` (e.g. `ltr:ml-3 rtl:mr-3`)
- **Open/closed state** — `open:` for `<details>`/`<dialog>` and `:popover-open`
- **inert** — `inert:opacity-50`

## Child selectors

- **`*`** — direct children: `*:rounded-full *:border` (children can't override styles given to them by the parent)
- **`**`** — all descendants, best combined with another variant: `**:data-avatar:size-12`

## Custom variants

### Arbitrary variants

Write custom selector variants directly in your HTML, wrapped in square brackets:

```html
<li class="[&.is-dragging]:cursor-grabbing">{item}</li>
<div class="[&_p]:mt-4">...</div>   <!-- underscore = space -->
<div class="flex [@supports(display:grid)]:grid">...</div>
```

### Registering a custom variant

```css
@custom-variant theme-midnight (&:where([data-theme="midnight"] *));
```

```html
<html data-theme="midnight">
  <button class="theme-midnight:bg-black ..."></button>
</html>
```

## Quick reference (excerpt)

| Variant | CSS |
|---------|-----|
| `hover` | `@media (hover: hover) { &:hover }` |
| `focus` | `&:focus` |
| `focus-visible` | `&:focus-visible` |
| `active` | `&:active` |
| `first` / `last` | `&:first-child` / `&:last-child` |
| `odd` / `even` | `&:nth-child(odd)` / `&:nth-child(even)` |
| `disabled` / `checked` | `&:disabled` / `&:checked` |
| `required` / `invalid` | `&:required` / `&:invalid` |
| `before` / `after` | `&::before` / `&::after` |
| `placeholder` / `selection` | `&::placeholder` / `&::selection` |
| `sm` / `md` / `lg` / `xl` / `2xl` | `@media (width >= 40/48/64/80/96rem)` |
| `dark` | `@media (prefers-color-scheme: dark)` |
| `motion-reduce` | `@media (prefers-reduced-motion: reduce)` |
| `print` | `@media print` |
| `open` | `&:is([open], :popover-open, :open)` |

(See the source page for the complete variant table, which also includes container-query variants `@3xs`–`@7xl`, every ARIA/`max-*` variant, and a full pseudo-class example gallery.)
