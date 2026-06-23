> Source: https://tailwindcss.com/docs/styling-with-utility-classes — Tailwind CSS official docs (curriculum extract, fetched 2026-06-17)

# Styling with utility classes

## Overview

You style things with Tailwind by combining many single-purpose presentational classes _(utility classes)_ directly in your markup:

```html
<div class="mx-auto flex max-w-sm items-center gap-x-4 rounded-xl bg-white p-6 shadow-lg outline outline-black/5 dark:bg-slate-800 dark:shadow-none dark:-outline-offset-1 dark:outline-white/10">
  <img class="size-12 shrink-0" src="/img/logo.svg" alt="ChitChat Logo" />
  <div>
    <div class="text-xl font-medium text-black dark:text-white">ChitChat</div>
    <p class="text-gray-500 dark:text-gray-400">You have a new message!</p>
  </div>
</div>
```

For example, in the UI above we've used:

- The display and padding utilities (`flex`, `shrink-0`, and `p-6`) to control the overall layout
- The max-width and margin utilities (`max-w-sm` and `mx-auto`) to constrain the card width and center it horizontally
- The background-color, border-radius, and box-shadow utilities (`bg-white`, `rounded-xl`, and `shadow-lg`) to style the card's appearance
- The width and height utilities (`size-12`) to set the width and height of the logo image
- The gap utilities (`gap-x-4`) to handle the spacing between the logo and the text
- The font-size, color, and font-weight utilities (`text-xl`, `text-black`, `font-medium`, etc.) to style the card text

Styling things this way contradicts a lot of traditional best practices, but once you try it you'll quickly notice some really important benefits:

- **You get things done faster** — you don't spend any time coming up with class names, making decisions about selectors, or switching between HTML and CSS files, so your designs come together very fast.
- **Making changes feels safer** — adding or removing a utility class to an element only ever affects that element, so you never have to worry about accidentally breaking something another page that's using the same CSS.
- **Maintaining old projects is easier** — changing something just means finding that element in your project and changing the classes, not trying to remember how all of that custom CSS works that you haven't touched in six months.
- **Your code is more portable** — since both the structure and styling live in the same place, you can easily copy and paste entire chunks of UI around, even between different projects.
- **Your CSS stops growing** — since utility classes are so reusable, your CSS doesn't continue to grow linearly with every new feature you add to a project.

## Why not just use inline styles?

A common reaction to this approach is wondering, "isn't this just inline styles?" and in some ways it is — you're applying styles directly to elements instead of assigning them a class name and then styling that class.

But using utility classes has many important advantages over inline styles, for example:

- **Designing with constraints** — using inline styles, every value is a magic number. With utilities, you're choosing styles from a [predefined design system](/docs/theme), which makes it much easier to build visually consistent UIs.
- **Hover, focus, and other states** — inline styles can't target states like hover or focus, but Tailwind's state variants make it easy to style those states with utility classes.
- **Media queries** — you can't use media queries in inline styles, but you can use Tailwind's responsive variants to build fully responsive interfaces easily.

```html
<div class="flex flex-col gap-2 p-8 sm:flex-row sm:items-center sm:gap-6 sm:py-4 ...">
  <img class="mx-auto block h-24 rounded-full sm:mx-0 sm:shrink-0" src="/img/erin-lindford.jpg" alt="" />
  <div class="space-y-2 text-center sm:text-left">
    <div class="space-y-0.5">
      <p class="text-lg font-semibold text-black">Erin Lindford</p>
      <p class="font-medium text-gray-500">Product Engineer</p>
    </div>
    <button class="border-purple-200 text-purple-600 hover:border-transparent hover:bg-purple-600 hover:text-white active:bg-purple-700 ...">
      Message
    </button>
  </div>
</div>
```

## Thinking in utility classes

### Styling hover and focus states

To style an element on states like hover or focus, prefix any utility with the state you want to target, for example `hover:bg-sky-700`:

```html
<button class="bg-sky-500 hover:bg-sky-700 ...">Save changes</button>
```

These prefixes are called [variants](/docs/hover-focus-and-other-states) in Tailwind, and they only apply the styles from a utility class when the condition for that variant matches.

Here's what the generated CSS looks like for the `hover:bg-sky-700` class:

```css
.hover\:bg-sky-700 {
  &:hover {
    background-color: var(--color-sky-700);
  }
}
```

You can even stack variants in Tailwind to apply a utility when multiple conditions match, like combining `hover:` and `disabled:`

```html
<button class="bg-sky-500 disabled:hover:bg-sky-500 ...">Save changes</button>
```

### Media queries and breakpoints

Just like hover and focus states, you can style elements at different breakpoints by prefixing any utility with the breakpoint where you want that style to apply:

```html
<div class="grid grid-cols-2 sm:grid-cols-3">
  <!-- ... -->
</div>
```

```css
.sm\:grid-cols-3 {
  @media (width >= 40rem) {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
```

### Targeting dark mode

Styling an element in dark mode is just a matter of adding the `dark:` prefix to any utility you want to apply when dark mode is active:

```html
<div class="bg-white dark:bg-gray-800 rounded-lg px-6 py-8 ring shadow-xl ring-gray-900/5">
  <h3 class="text-gray-900 dark:text-white mt-5 text-base font-medium tracking-tight">Writes upside-down</h3>
  <p class="text-gray-500 dark:text-gray-400 mt-2 text-sm">
    The Zero Gravity Pen can be used to write in any orientation, including upside-down. It even works in outer space.
  </p>
</div>
```

A single utility class will never include _both_ the light and dark styles — you style things in dark mode by using multiple classes, one for the light mode styles and another for the dark mode styles.

### Using class composition

A lot of the time with Tailwind you'll even use multiple classes to build up the value for a single CSS property, for example adding multiple filters to an element:

```html
<div class="blur-sm grayscale">
  <!-- ... -->
</div>
```

```css
.blur-sm {
  --tw-blur: blur(var(--blur-sm));
  filter: var(--tw-blur,) var(--tw-brightness,) var(--tw-grayscale,);
}
.grayscale {
  --tw-grayscale: grayscale(100%);
  filter: var(--tw-blur,) var(--tw-brightness,) var(--tw-grayscale,);
}
```

### Using arbitrary values

When you need to use a one-off value outside of your theme, use the special square bracket syntax for specifying arbitrary values:

```html
<button class="bg-[#316ff6] ...">Sign in with Facebook</button>
```

```html
<div class="grid grid-cols-[24rem_2.5rem_minmax(0,1fr)]"><!-- ... --></div>
```

```html
<div class="max-h-[calc(100dvh-(--spacing(6)))]"><!-- ... --></div>
```

```html
<div class="[--gutter-width:1rem] lg:[--gutter-width:2rem]"><!-- ... --></div>
```

#### How does this even work?

Tailwind CSS isn't one big static stylesheet — it generates the CSS needed based on the classes you're actually using when you compile your CSS. It scans all of the files in your project looking for any symbol that looks like it could be a class name:

```jsx
export default function Button({ size, children }) {
  let sizeClasses = {
    md: "px-4 py-2 rounded-md text-base",
    lg: "px-5 py-3 rounded-lg text-lg",
  }[size];
  return (
    <button type="button" className={`font-bold ${sizeClasses}`}>
      {children}
    </button>
  );
}
```

### Complex selectors

```html
<button class="dark:lg:data-current:hover:bg-indigo-600 ...">
  <!-- ... -->
</button>
```

```css
@media (prefers-color-scheme: dark) and (width >= 64rem) {
  button[data-current]:hover {
    background-color: var(--color-indigo-600);
  }
}
```

`group-*` lets you style an element when a specific parent is hovered:

```html
<a href="#" class="group rounded-lg p-8">
  <span class="group-hover:underline">Read more…</span>
</a>
```

Arbitrary variants let you write any selector directly in a class name:

```html
<div class="[&>[data-active]+span]:text-blue-600 ...">
  <span data-active><!-- ... --></span>
  <span>This text will be blue</span>
</div>
```

### When to use inline styles

Inline styles are still useful, particularly when a value is coming from a dynamic source like a database or API:

```jsx
export function BrandedButton({ buttonColor, textColor, children }) {
  return (
    <button style={{ backgroundColor: buttonColor, color: textColor }} className="rounded-md px-3 py-1.5 font-medium">
      {children}
    </button>
  );
}
```

## Managing duplication

When you build entire projects with just utility classes, you'll inevitably find yourself repeating certain patterns. Strategies:

### Using loops

A design element that shows up more than once is often only authored once because the markup is rendered in a loop:

```html
<div class="mt-3 flex -space-x-2 overflow-hidden">
  {#each contributors as user}
    <img class="inline-block h-12 w-12 rounded-full ring-2 ring-white" src={user.avatarUrl} alt={user.handle} />
  {/each}
</div>
```

### Using multi-cursor editing

When duplication is localized to a group of elements in a single file, use multi-cursor editing to quickly select and edit each class list at once.

### Using components

If you need to reuse styles across multiple files, create a _component_ (React/Svelte/Vue) or a _template partial_ (Blade, ERB, Twig, Nunjucks):

```jsx
export function VacationCard({ img, imgAlt, eyebrow, title, pricing, url }) {
  return (
    <div>
      <img className="rounded-lg" src={img} alt={imgAlt} />
      <div className="mt-4">
        <div className="text-xs font-bold text-sky-500">{eyebrow}</div>
        <div className="mt-1 font-bold text-gray-700">
          <a href={url} className="hover:underline">{title}</a>
        </div>
        <div className="mt-2 text-sm text-gray-600">{pricing}</div>
      </div>
    </div>
  );
}
```

### Using custom CSS

When a template partial feels heavy-handed, writing some custom CSS is totally fine, using [theme variables](/docs/theme#with-custom-css) to keep the design consistent:

```css
@import "tailwindcss";

@layer components {
  .btn-primary {
    border-radius: calc(infinity * 1px);
    background-color: var(--color-violet-500);
    padding-inline: --spacing(5);
    padding-block: --spacing(2);
    font-weight: var(--font-weight-semibold);
    color: var(--color-white);
    box-shadow: var(--shadow-md);
    &:hover {
      @media (hover: hover) {
        background-color: var(--color-violet-700);
      }
    }
  }
}
```

## Managing style conflicts

### Conflicting utility classes

When you add two classes that target the same CSS property, the class that appears later in the stylesheet wins (not the order in the `class` attribute). In general, never add two conflicting classes to the same element.

### Using the important modifier

Add `!` to the end of the class name to make all of the declarations `!important`:

```html
<div class="bg-teal-500 bg-red-500!"><!-- ... --></div>
```

### Using the important flag

Use the `important` flag when importing Tailwind to mark _all_ utilities as `!important`:

```css
@import "tailwindcss" important;
```

### Using the prefix option

If your project has class names that conflict with Tailwind utilities, prefix all Tailwind-generated classes and CSS variables:

```css
@import "tailwindcss" prefix(tw);
```
