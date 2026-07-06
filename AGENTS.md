# Repository Guidelines

## Project

This repository is a Markdown-driven recipe book built with Zensical and published to GitHub Pages.

## Recipe Editing

- Put recipes under the matching `recipes/<category-folder>/` directory.
- Use lowercase, hyphenated filenames.
- New recipe files must start with YAML frontmatter containing `slug`, `title`, `tags`, and `category`.
- Keep recipe Markdown plain and practical: H1 title, `## Ingredients`, `## Instructions`, optional storage/notes, and `## Source` for web-derived recipes.
- Use British English and metric-first measurements.
- Update `README.md` when adding a recipe so the top-level index stays current.
- Follow `spec/spec.md` for the full recipe conversion rules.

## Build And Test

- Do not create local virtualenvs or install packages globally for this project.
- Use the Docker setup for local site testing:
  - `s/up`
  - `s/down`
- The production site build command is `zensical build --clean`.

## GitHub Actions

- Keep workflow actions pinned to commit SHAs.
- Preserve the original tag as a `# pin@<ref>` comment so `pin-github-action` can update the pins later.
- To refresh pins, run `pin-github-action .github/workflows/` from a suitable environment with network access.

## Generated Files

- Do not commit local build output, caches, virtualenvs, editor state, or secrets.
- The root `.gitignore` is the source of truth for local generated files.
