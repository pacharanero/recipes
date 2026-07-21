# Repository Guidelines

## Project

This repository is a Markdown-driven recipe book built with Zensical and published to GitHub Pages.

## Read First

Before changing recipes, site structure, or build configuration, check:

- `README.md` for the repository overview and top-level recipe index.
- `recipes/index.md` for the published site landing page.
- `spec/README.md` and `spec/spec.md` for recipe conversion rules, categories, frontmatter, source attribution, and local testing expectations.
- `mkdocs.yml` for Zensical site configuration and navigation.
- `~/code/house-style/AGENTS.md` for cross-repository engineering standards.

## Core Invariants

- Keep the recipe collection Markdown-driven and buildable with Zensical.
- Keep content, `README.md`, and `mkdocs.yml` navigation consistent when adding or moving recipes.
- Do not hand-edit generated site output or commit local caches and secrets.
- Preserve source attribution for web-derived recipes and the repository's split content/code licensing.

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

## Before Every Commit

```sh
s/check-recipes
docker compose config --quiet
docker compose run --rm zensical zensical build --clean
git diff --check
```

Review the diff as well as the command output. A successful build does not prove recipe accuracy, attribution, or food safety.

## GitHub Actions

- Keep workflow actions pinned to commit SHAs.
- Preserve the exact release tag as a `# vX.Y.Z` comment.
- To refresh pins, run `pin-github-action .github/workflows/` from a suitable environment with network access.

## Approval Required

- Ask before deploying manually, changing repository settings or secrets, publishing externally, deleting branches, force-pushing, or taking other externally visible actions.

## Generated Files

- Do not commit local build output, caches, virtualenvs, editor state, Playwright MCP artefacts, or secrets.
- The root `.gitignore` is the source of truth for local generated files.
