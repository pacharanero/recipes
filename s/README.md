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

## `s/gen-indexes`

Generates the section landing pages (`recipes/<section>/index.md`) and the recipe index in the root `README.md` from the files on disk, so neither has to be maintained by hand.

Section titles, blurbs and tags live in the script itself; the recipe lists come from each recipe's `title` frontmatter. A recipe with `featured: true` in its frontmatter is also listed under a Highlights heading on its section page.

Run `s/gen-indexes` after adding, renaming or removing a recipe, and commit the result. `s/gen-indexes --check` fails if any generated file is out of date, and runs in CI.

## `s/check-recipes`

Checks Markdown content policy for files under `recipes/`:

- slug-case filenames
- YAML frontmatter at the top of recipe/content files
- required frontmatter keys: `slug`, `title`, `tags`, `category`
- category values from `spec/spec.md`
- every file under `recipes/` appears in the `mkdocs.yml` nav, and every nav entry exists

The root site index (`recipes/index.md`) and generated tags page (`recipes/tags.md`) are skipped.
