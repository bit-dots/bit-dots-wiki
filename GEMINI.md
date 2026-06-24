# Bit-Dots Wiki Project Instructions

## Project Overview
- **Name**: Bit-Dots Wiki
- **Description**: A minimal personal knowledge Wiki ("点滴成海，记录万物").
- **Tech Stack**: [Astro](https://astro.build/) (static site generator) + [Vue 3](https://vuejs.org/) (interactive components).
- **Architecture**: Content is stored as Markdown in `src/content/wiki/`, managed by Astro Content Collections.

## Core Guidelines
- **Git Operations**: **NEVER** perform git commands (add, commit, push, pull) unless explicitly instructed by the user. Instead, provide a suggested commit message following the **Conventional Commits** specification (e.g., `fix(scope): description`).
- **CLAUDE.md**: Follow the behavioral guidelines in `CLAUDE.md`.
- **Style**: Maintain the minimal, clean aesthetic of the project.
- **Content**: Focus on tech exploration (Frontend, AI, Tools), life essays, and project archives.

## Development Workflow
- **Dev Server**: `npm run dev`
- **Build**: `npm run build`
- **Postbuild**: `npm run postbuild` (runs Pagefind indexing)
- **Preview**: `npm run preview`
- **Source Files**: Content is in `src/content/wiki/`. Configuration is in `astro.config.mjs` and `src/content.config.ts`.
- **Git Commit Message**: 仅在**修改代码或内容后**提供符合 Conventional Commits 规范的中文 Git commit message；单纯咨询问题或进行技术讨论时**无需**提供。

## Key Files & Directories
- `src/content/wiki/`: Markdown content files.
- `src/layouts/`: Layout components (BaseLayout, PostLayout).
- `src/components/`: UI components (Astro + Vue).
- `src/pages/`: Route pages.
- `src/styles/`: Global CSS styles.
- `src/plugins/`: Markdown processing plugins.
- `astro.config.mjs`: Astro configuration.
- `src/content.config.ts`: Content collection schema.
- `CLAUDE.md`: AI behavior guidelines.

## Conventions
- Use Chinese for content as per existing files.
- Internal links should use relative paths or root-relative paths (e.g., `/intro`).
- Follow CC BY-NC-SA 4.0 license for content.