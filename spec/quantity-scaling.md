# Quantity Scaling Spec (Draft)

Status: **spec only, not yet implemented**. This document defines the syntax, behaviour, and test requirements for recipe quantity scaling. The first exemplar recipe is [`recipes/cocktails/diplomat.md`](../recipes/cocktails/diplomat.md).

## Purpose

Readers should be able to scale any recipe up or down (for example, multiply a one-serving cocktail by 8 for a party, or halve a 2-litre preserve batch) without manual arithmetic and without the site storing multiple variants of the same recipe.

The feature is technically modelled on the Transpose tool in `pacharanero/charts` (`charts/styles/transpose.js`): a client-side script rewrites explicitly delimited tokens in the rendered page. The Markdown source stays the single source of truth and remains fully readable as plain Markdown.

## Design principles

1. **Markdown stays plain.** A recipe with scaling tokens must still read naturally with JavaScript disabled, in a text editor, on GitHub, and in `git diff`.
2. **Explicit opt-in per quantity.** Only quantities wrapped in delimiters scale. Undelimited text is never rewritten. This is what makes "scales only some ingredients" detectable and testable.
3. **Delimiters are reserved.** Just as `pacharanero/charts` reserves `[...]` and `{...}` for pitched content, this repo reserves `{...}` for quantity tokens and for nothing else.
4. **Deterministic scaling.** The same recipe and factor always produce the same output, verified by automated tests.

## Token syntax

A quantity token wraps the numeric quantity and its unit, and is placed where the number currently sits in the ingredient line:

```markdown
- {50 ml} dry vermouth
- {2 dashes} orange bitters
- {400 g} tomato purée (double concentrate)
- {1} whole head of garlic, cloves separated and peeled
```

### Token grammar

```
token      := "{" quantity unit? "}"
quantity   := integer | decimal | vulgar-fraction | mixed-number
unit       := one or more words from the recognised unit vocabulary
```

- Whitespace between number and unit is required when a unit is present.
- A unitless count is valid: `{3}` eggs.
- Percentages, ranges (`2-3`), and open quantities (`to taste`, `handful`) are **not** valid tokens and must not be wrapped.

### Recognised unit vocabulary (v1)

- Volume: `ml`, `l`, `tsp`, `tbsp`, `fl oz`, `cup`, `dash(es)`, `drop(s)`
- Mass: `g`, `kg`, `oz`, `lb`
- Count: none (unitless)

Units not in the vocabulary are still allowed in tokens (the scaler passes them through unchanged and only rewrites the number), but the policy checker warns about them so new units are added deliberately rather than by accident.

### Where tokens may appear

- Ingredient list bullet lines under `## Ingredients` (and equivalent H2s such as `## Dressing`) only.
- Tokens must not appear in instructions, headings, notes, or source lines in v1. Cooking times, oven temperatures, and pan sizes do not scale linearly and must stay outside tokens.

## Frontmatter

Recipes using tokens SHOULD declare a yield so the UI can label scale factors meaningfully:

```yaml
yields: 1 serving
```

`yields` is free text (`2 pizzas`, `about 2 litres`, `24 falafel`). The factor is applied to quantities only; the yield line is descriptive.

## Reserved delimiters

`{` and `}` are reserved for quantity tokens in every file under `recipes/`. They must not be used for any other purpose. The recipe policy checker (`s/check-recipes`) will be extended to:

1. Validate every `{...}` token against the grammar; a malformed token is an error.
2. Flag `{` or `}` appearing outside a valid token as an error.
3. **Completeness rule:** in a recipe containing at least one token, every bullet line under an ingredients heading must either contain a valid token or be an explicit non-quantified line (`to taste`, `handful`, `splash`, `garnish`, and similar). A quantified ingredient left undelimited is an error, because it is the exact failure mode this feature exists to prevent.

## Runtime behaviour

A single client-side script (proposed: `recipes/styles/scale.js`, registered in `mkdocs.yml` under `extra_javascript`) will:

1. On page load, find tokens in the rendered article, validate each against the grammar, and mark them (span elements with the original value in a data attribute, as the charts transposer does).
2. Show a scale control (− / value / + / reset) in the page header when the page contains tokens. Steps: 0.25, 0.5, 1, 1.5, 2, 3, 4, 6, 8, 12, plus free-text entry.
3. Rewrite each token by multiplying the quantity by the factor, keeping the unit unchanged.
4. Show unscaled text untouched when the factor is 1.
5. Persist nothing server-side; the control may remember the last factor in `localStorage` per session, but scaling is always derived from the original token values (no compounding).

### Rounding rules

- Counts and `dash(es)`: integers only (round to nearest; minimum 1).
- `tsp` / `tbsp`: round to the nearest 0.25 below 2 tbsp, otherwise nearest 0.5.
- `ml` / `g`: round to nearest 5 up to 100, otherwise nearest 10.
- `l`, `kg`: one decimal place.
- Fractions render as vulgar fractions where clean (½, ¾), otherwise decimals.

## Automated testing requirements

The tests exist to catch the two failure modes called out in the original request: incorrect scaling, and partial scaling (some ingredients scaled, some not).

A test harness (proposed: `scripts/test-scale.js` with an `s/test-scale` wrapper) must run in CI alongside the existing checks, and the scale logic must live in one module shared by the page script and the tests (the charts transposer keeps logic inside the IIFE; this repo should not - the scaler must be importable).

1. **Golden unit tests.** A table of (token, factor) → expected output pairs covering every unit in the vocabulary, fractions, decimals, unitless counts, rounding boundaries, and minimum-1 clamping.
2. **Per-recipe completeness test.** For every recipe containing tokens, run the completeness rule from the section above. A recipe with a quantified undelimited ingredient fails the build.
3. **Full-scaling matrix test.** For every tokenised recipe and every factor in the standard step list, assert that:
   - the number of tokens is unchanged;
   - every token's numeric value has changed (or is unchanged *only* where the rounded result legitimately equals the original, for example a minimum-1 clamp);
   - values are monotonically increasing with the factor;
   - no token is left at its original text when the factor is not 1.
4. **Parser regression test.** The checker and the runtime must agree on the grammar: every token accepted by one is accepted by the other (validated by running both over the corpus).
5. **CI integration.** The harness runs in the existing GitHub Actions workflow alongside `s/check-recipes` and the Zensical build, so a scaling bug cannot merge.

## Rollout plan

1. **This change:** spec plus the Diplomat exemplar.
2. Authoring-time validation in `s/check-recipes` (grammar, reserved delimiters, completeness).
3. Scaler module plus golden tests, run by `s/test-scale` and CI.
4. Client script and header control, with browser verification per the house-style UI standard.
5. Progressive conversion of existing recipes, category by category, with the completeness checker as the guardrail.

## Non-goals (v1)

- Unit conversion (no ml-to-cup rewriting; units pass through unchanged).
- Scaling instructions, timings, or temperatures.
- Server-side or build-time rewriting of page content.
- Per-ingredient independent scaling.