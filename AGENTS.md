# Repository Guidelines

## Project

This repository is a Markdown-driven recipe book built with Zensical and published to GitHub Pages.

## Read First

Before changing recipes, site structure, or build configuration, check:

- `README.md` for the repository overview and top-level recipe index.
- `recipes/index.md` for the published site landing page.
- `spec/README.md` and `spec/spec.md` for recipe conversion rules, categories, frontmatter, source attribution, and local testing expectations.
- `mkdocs.yml` for Zensical site configuration and navigation.

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
- Docker Compose is the intentional local preview path for this repo.
- Use the script wrappers:
  - `s/docs` starts the local Zensical preview.
  - `s/up` is a compatibility alias for `s/docs`.
  - `s/down` stops the preview containers.
  - `s/check-recipes` runs the content policy check.
- The production site build command is `zensical build --clean`; for local validation, run it through Docker: `docker compose run --rm zensical zensical build --clean`.

## GitHub Actions

- Keep workflow actions pinned to commit SHAs.
- Preserve the original tag as a `# pin@<ref>` comment so `pin-github-action` can update the pins later.
- To refresh pins, run `pin-github-action .github/workflows/` from a suitable environment with network access.

## Generated Files

- Do not commit local build output, caches, virtualenvs, editor state, Playwright MCP artefacts, or secrets.
- The root `.gitignore` is the source of truth for local generated files.
