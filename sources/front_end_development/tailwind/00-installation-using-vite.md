> Source: https://tailwindcss.com/docs/installation/using-vite — Tailwind CSS official docs (curriculum extract, fetched 2026-06-17)

# Installing Tailwind CSS with Vite

## Installation Steps

### 01. Create your project

Start by creating a new Vite project if you don't have one set up already. The most common approach is to use [Create Vite](https://vite.dev/guide/#scaffolding-your-first-vite-project).

```bash
npm create vite@latest my-project
cd my-project
```

### 02. Install Tailwind CSS

Install `tailwindcss` and `@tailwindcss/vite` via npm.

```bash
npm install tailwindcss @tailwindcss/vite
```

### 03. Configure the Vite plugin

Add the `@tailwindcss/vite` plugin to your Vite configuration.

**vite.config.ts**
```typescript
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    tailwindcss(),
  ],
})
```

### 04. Import Tailwind CSS

Add an `@import` to your CSS file that imports Tailwind CSS.

```css
@import "tailwindcss";
```

### 05. Start your build process

Run your build process with `npm run dev` or whatever command is configured in your `package.json` file.

```bash
npm run dev
```

### 06. Start using Tailwind in your HTML

Make sure your compiled CSS is included in the `<head>` _(your framework might handle this for you)_, then start using Tailwind's utility classes to style your content.

```html
<!doctype html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="/src/style.css" rel="stylesheet">
</head>
<body>
  <h1 class="text-3xl font-bold underline">
    Hello world!
  </h1>
</body>
</html>
```

---

## Related Core Documentation Pages

### Getting Started
- [Installation](/docs/installation)
- [Editor setup](/docs/editor-setup)
- [Compatibility](/docs/compatibility)
- [Upgrade guide](/docs/upgrade-guide)

### Core Concepts
- [Styling with utility classes](/docs/styling-with-utility-classes)
- [Hover, focus, and other states](/docs/hover-focus-and-other-states)
- [Responsive design](/docs/responsive-design)
- [Dark mode](/docs/dark-mode)
- [Theme variables](/docs/theme)
- [Colors](/docs/colors)
- [Adding custom styles](/docs/adding-custom-styles)
- [Detecting classes in source files](/docs/detecting-classes-in-source-files)
- [Functions and directives](/docs/functions-and-directives)
