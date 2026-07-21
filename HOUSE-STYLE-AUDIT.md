# House-Style Audit

Audit date: 2026-07-21

Audited against: `~/code/house-style` as of this date, especially `agents.md`, `ci.md`, `docs.md`, `licensing.md`, `new-repos.md`, `scripts.md`, `security.md`, and `specs.md`.

Scope: static audit plus the compliance fixes recorded below. The site build and content policy check were also run through the repository's documented local workflow.

## Summary

This is a public, Markdown-driven recipe collection built with Zensical and deployed to GitHub Pages. It already follows important house-style patterns: a useful local `AGENTS.md`, a specification index, Docker-backed repeatable scripts, a content policy check, SHA-pinned Actions, artifact-based Pages deployment, a split content/code licence, a security policy, and a clean Zensical build.

Main improvements completed during this audit:

- Hardened GitHub Actions permissions and checkout credentials, added pull-request validation and Zizmor workflow security scanning, and normalised action version comments.
- Updated Dependabot grouping and cooldown policy for both GitHub Actions and Python dependencies.
- Removed unsupported Material-style theme options and the unsupported `tags` plugin from the active Zensical configuration.
- Added `.editorconfig` and `REUSE.toml`, and aligned the code licence with the house-style AGPL-3.0-or-later default.
- Strengthened agent instructions and content-policy validation without invalidating established legacy slugs.

## Priority Findings

### P1 - Workflow jobs had broader permissions than required

Status: fixed in this audit.

Evidence:

- `.github/workflows/docs.yml` granted `pages: write` and `id-token: write` at workflow scope, so the build job inherited deployment permissions.
- The checkout step did not set `persist-credentials: false`.
- No blocking Zizmor workflow-security check was present.

House style:

- `ci.md` requires workflow-level `contents: read`, write permissions only on the smallest possible job, non-persisted checkout credentials, SHA-pinned Actions, and a blocking Zizmor job.

Suggested change:

- Keep the implemented least-privilege job permissions and workflow-security job current through Dependabot review.

### P2 - Zensical configuration retained unsupported MkDocs Material features

Status: fixed in this audit.

Evidence:

- `mkdocs.yml` actively configured Material-style `theme.features`, `palette`, and the unsupported `tags` plugin.
- The Docker build happened to succeed, but unsupported configuration can be silently ignored and makes the migration ambiguous.

House style:

- `docs.md` says not to carry unsupported Material-only theme options and says active unsupported plugins should be removed or suspended.

Suggested change:

- Keep `mkdocs.yml` limited to configuration proved to work with Zensical. Restore tags or theme controls only when current Zensical documentation confirms support and the rendered site is verified.

### P2 - Licensing metadata did not match the house-style default

Status: fixed in this audit.

Evidence:

- `LICENSE` and `README.md` previously placed code, scripts, workflows, and site configuration under MIT.
- No `REUSE.toml` covered Markdown, assets, configuration, and other files that cannot carry inline SPDX headers.

House style:

- `licensing.md` sets AGPL-3.0-or-later as the code default, CC-BY-SA-4.0 for written content, and REUSE metadata for files without inline headers.

Suggested change:

- Run `reuse lint` when REUSE is available and add inline SPDX headers to newly created non-trivial source or shell files.

### P2 - Content validation covered only part of the documented contract

Status: partially fixed in this audit.

Evidence:

- `s/check-recipes` checked filename shape, frontmatter key presence, categories, and inline tag-list syntax.
- It did not reject empty frontmatter values, malformed tag lists, out-of-range or non-lowercase tags, or missing H1 headings.
- Existing recipes contain historical slugs that do not always match filenames, despite `spec/spec.md` saying they normally match.

House style:

- `specs.md` recommends policy enforcement for repeated content contracts and requires intentional divergences between implementation and specification to be documented.

Suggested change:

- The checker now enforces safe invariants on the existing collection. Treat exact slug-to-filename migration and stricter section enforcement as a separate reviewed content change because applying either indiscriminately would alter many established pages and non-recipe guides.

### P3 - Agent and repository scaffolding omitted several operational details

Status: fixed in this audit.

Evidence:

- `AGENTS.md` did not link to `~/code/house-style/AGENTS.md`, state core invariants, list the complete pre-commit validation sequence, or identify externally visible actions requiring approval.
- The repository had no `.editorconfig`.

House style:

- `agents.md` requires read-first material, invariants, exact validation commands, assurance, and approval boundaries.
- `new-repos.md` includes `.editorconfig` in the baseline scaffold.

Suggested change:

- Keep agent guidance concise and update its validation commands whenever CI changes.

## Compliant / Good Patterns

- `spec/README.md` provides a clear reading order and `spec/spec.md` records the content contract.
- `s/` exposes the repository's repeatable operations, scripts are executable, and each script changes to the Git root.
- `s/check-recipes` is enforced before the production site build.
- `.github/workflows/docs.yml` uses artifact-based GitHub Pages deployment rather than a `gh-pages` branch.
- All GitHub Actions are pinned to full commit SHAs.
- `requirements.txt` pins the direct Zensical dependency.
- `SECURITY.md` gives a private reporting route and distinguishes software security from ordinary food-safety corrections.
- `.gitignore` excludes build output, caches, virtual environments, editor state, Playwright artefacts, and local secrets.
- `docker compose run --rm zensical zensical build --clean` completed successfully during the audit.

## Not Applicable

- Rust CLI architecture, Cargo testing, cargo audit, release automation, package distribution, and library extraction are not applicable to this content site.
- Clinical software safety documentation is not applicable. Recipes can carry food-safety risks, but this repository is not a clinical tool and `SECURITY.md` already routes food-safety corrections appropriately.
- Tauri and application UI architecture standards are not applicable. Responsive visual review remains relevant when templates or brand CSS change.
- Conformance fixtures and a reference implementation are unnecessary for the current single-site content model.

## Suggested First PR

1. Land the CI, Dependabot, Zensical configuration, agent guidance, editor configuration, licensing metadata, and policy-checker changes from this audit.
2. Confirm the repository's GitHub Pages source is set to GitHub Actions and make the pull-request validation job a required branch-protection check if branch protection is used.

## Suggested Second PR

1. Audit historical recipe slugs, category placement, README coverage, and `mkdocs.yml` navigation together, then migrate inconsistencies only where URLs and redirects have been considered.
2. Add focused Markdown link or navigation validation if index drift continues to recur.
