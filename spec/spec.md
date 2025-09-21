# Recipe Markdown Conversion Instructions

To ensure consistency when converting recipes to Markdown, follow these persistent prompt instructions:

## 1. Title

- Use a single H1 heading for the recipe name at the top of the file.

## 2. Ingredients

- Use an H2 heading (`## Ingredients`).
- List all ingredients as bullet points, one per line, with clear measurements and preparation notes.
- Exclude any non-essential commentary or tips.

## 3. Instructions

- Use an H2 heading (`## Instructions`).
- Write the method as a numbered list, with each step as a single, clear instruction.
- Only include essential steps for making the recipe. Omit tips, serving suggestions, and non-essential commentary.

## 4. Formatting

- Do not include images, links, or promotional content (except a final source URL per Section 9).
- Use plain Markdown only.
- Use metric and imperial units if both are provided; otherwise, preserve the original units.

## 5. Exclusions

- Exclude all non-recipe content: introductions, stories, nutrition, comments, reviews, and advertisements.
- Only include ingredients and method required to make the recipe.

## 6. File Naming

- Save each recipe in the root of the repository
- Save each recipe as a Markdown file with a slugified name (lowercase, hyphens for spaces, no special characters).

## 7. Update the README.md which serves as an index of all recipes.

- Add a link for the new recipe to the index
- Follow the style of existing links
- For now simple alphabetical order is fine

## 8. Update spec.md

- If new recipes require deviation from the guidelines in this document, update this spec.md file to reflect those changes.

## 9. Source Attribution (Web-Derived Recipes)

- If a recipe is adapted or transcribed from a publicly available webpage, append a `## Source` section at the end of the file.
- Use one bare URL on a single line (no markdown link) prefixed by one of: `Source:`, `Adapted from:`, or `Inspired by:` depending on the level of change.
- Do not include tracking parameters if avoidable; keep the canonical URL only.
- Omit the section entirely for original or fully self-authored recipes.

---

These instructions should be referenced for all future recipe conversions to Markdown in this project.
