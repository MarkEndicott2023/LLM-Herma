> Source: https://tailwindcss.com/docs/dark-mode — Tailwind CSS official docs (curriculum extract, fetched 2026-06-17)

# Dark Mode

Using variants to style your site in dark mode.

## Overview

Tailwind includes a `dark` variant that lets you style your site differently when dark mode is enabled:

```html
<div class="bg-white dark:bg-gray-800 rounded-lg px-6 py-8 ring shadow-xl ring-gray-900/5">
  <div>
    <span class="inline-flex items-center justify-center rounded-md bg-indigo-500 p-2 shadow-lg">
      <svg class="h-6 w-6 stroke-white" ...><!-- ... --></svg>
    </span>
  </div>
  <h3 class="text-gray-900 dark:text-white mt-5 text-base font-medium tracking-tight">Writes upside-down</h3>
  <p class="text-gray-500 dark:text-gray-400 mt-2 text-sm">
    The Zero Gravity Pen can be used to write in any orientation, including upside-down. It even works in outer space.
  </p>
</div>
```

By default this uses the `prefers-color-scheme` CSS media feature, but you can also build sites that support toggling dark mode manually by overriding the dark variant.

## Toggling Dark Mode Manually

If you want your dark theme to be driven by a CSS selector instead of the `prefers-color-scheme` media query, override the `dark` variant to use your custom selector:

**app.css**
```css
@import "tailwindcss";

@custom-variant dark (&:where(.dark, .dark *));
```

Now `dark:*` utilities are applied whenever the `dark` class is present earlier in the HTML tree:

```html
<html class="dark">
  <body>
    <div class="bg-white dark:bg-black"><!-- ... --></div>
  </body>
</html>
```

A common approach is a bit of JavaScript that updates the `class` attribute and syncs the preference to `localStorage`.

### Using a Data Attribute

To use a data attribute instead of a class:

**app.css**
```css
@import "tailwindcss";

@custom-variant dark (&:where([data-theme=dark], [data-theme=dark] *));
```

```html
<html data-theme="dark">
  <body>
    <div class="bg-white dark:bg-black"><!-- ... --></div>
  </body>
</html>
```

### With System Theme Support

To build three-way theme toggles (light / dark / system), use a custom dark mode selector and the [`window.matchMedia()` API](https://developer.mozilla.org/en-US/docs/Web/API/Window/matchMedia):

```javascript
// On page load or when changing themes, best to add inline in `head` to avoid FOUC
document.documentElement.classList.toggle(
  "dark",
  localStorage.theme === "dark" ||
    (!("theme" in localStorage) && window.matchMedia("(prefers-color-scheme: dark)").matches),
);

// Whenever the user explicitly chooses light mode
localStorage.theme = "light";

// Whenever the user explicitly chooses dark mode
localStorage.theme = "dark";

// Whenever the user explicitly chooses to respect the OS preference
localStorage.removeItem("theme");
```
