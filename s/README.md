# Scripts

Run scripts from the repository root or any subdirectory; each script changes to the Git top-level directory before running.

## `s/docs`

Starts the Docker Compose Zensical preview in the background, rebuilding the image if needed, then opens <http://localhost:8008>.

Set `ZENSICAL_PORT` if the published host port changes in `docker-compose.yml`.

## `s/up`

Compatibility alias for `s/docs`.

## `s/down`

Stops the Docker Compose preview containers without deleting images.

Additional arguments are forwarded to `docker compose down`.

## `s/remove-containers-and-images`

Stops the Compose stack and removes locally-built Compose images with `docker compose down --rmi local`.

Use this when you need a clean local Docker rebuild.

## `s/check-recipes`

Checks Markdown content policy for files under `recipes/`:

- slug-case filenames
- YAML frontmatter at the top of recipe/content files
- required frontmatter keys: `slug`, `title`, `tags`, `category`
- category values from `spec/spec.md`

The root site index (`recipes/index.md`) and generated tags page (`recipes/tags.md`) are skipped.
