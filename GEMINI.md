# Bit-Dots Wiki Project Instructions

## Project Overview
- **Name**: Bit-Dots Wiki
- **Description**: A minimal personal knowledge Wiki ("点滴成海，记录万物").
- **Tech Stack**: [VitePress](https://vitepress.dev/) (Vue-powered static site generator).
- **Architecture**: Content is stored as Markdown in the `docs/` directory.

## Core Guidelines
- **Git Operations**: **NEVER** perform git commands (add, commit, push, pull) unless explicitly instructed by the user. Instead, provide a suggested commit message following the **Conventional Commits** specification (e.g., `fix(scope): description`).
- **CLAUDE.md**: Follow the behavioral guidelines in `CLAUDE.md`.
- **Style**: Maintain the minimal, clean aesthetic of the project.
- **Content**: Focus on tech exploration (Frontend, AI, Tools), life essays, and project archives.

## Development Workflow
- **Dev Server**: `npm run docs:dev`
- **Build**: `npm run docs:build`
- **Preview**: `npm run docs:preview`
- **Source Files**: Main content is in `docs/*.md`. Configuration is in `docs/.vitepress/config.mts`.

## Key Files & Directories
- `docs/`: Markdown content.
- `docs/.vitepress/`: VitePress configuration and theme.
- `docs/public/`: Static assets (logo, etc.).
- `CLAUDE.md`: AI behavior guidelines.

## Conventions
- Use Chinese for content as per existing files.
- Internal links should use relative paths or root-relative paths (e.g., `/intro`).
- Follow CC BY-NC-SA 4.0 license for content.
