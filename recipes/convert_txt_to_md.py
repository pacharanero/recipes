#!/usr/bin/env python3
"""Heuristic conversion of plaintext recipe notes in text-versions/ to Markdown in draft-md/.

Rules (aligned loosely with spec):
- First non-empty line -> Title (# ...)
- Lines after title until a blank: possible subtitle ignored.
- Detect an ingredients block: consecutive lines containing quantities (digits, fractions, measures) before an empty line.
- Remaining lines -> instructions, split by blank lines; enumerate.
- Files whose title suggests non-recipe (labels, flyer, sticker, template, whitewash, dye, shellac, toothpaste, wood finishes) are skipped.
- Output filename slugified from title.
"""
from __future__ import annotations
import re, unicodedata, pathlib, sys

SRC = pathlib.Path('text-versions')
OUT = pathlib.Path('draft-md')
OUT.mkdir(exist_ok=True)

SKIP_KEYWORDS = {
    'sticker','label','flyer','template','whitewash','dye','shellac','toothpaste','wood finishes','ink ('
}

MEASURE_TOKENS = re.compile(r"(\b\d+[\/\d]*\b|\b\d+\.\d+\b|\bhalf\b|\bquarter\b)")

slugify_map = {
    ord(' '):'-', ord('/'): '-', ord('&'):'and', ord(','):'', ord("'"):'', ord('('):'', ord(')'):'', ord(':'):'', ord(';'):'', ord('–'):'-', ord('—'):'-' }

def slugify(title:str)->str:
    t = unicodedata.normalize('NFKD', title).encode('ascii','ignore').decode('ascii')
    t = t.lower().translate(slugify_map)
    t = re.sub(r'[^a-z0-9-]+','-', t)
    t = re.sub(r'-+','-', t).strip('-')
    return t or 'recipe'

converted = []
skipped = []

for path in sorted(SRC.glob('*.txt')):
    raw = path.read_text(errors='ignore').strip()
    if not raw:
        skipped.append((path.name,'empty'))
        continue
    lines = [l.rstrip() for l in raw.splitlines()]
    # title is first non-empty line
    title = next((l for l in lines if l.strip()), 'Untitled').strip()
    tlow = title.lower()
    if any(k in tlow for k in SKIP_KEYWORDS):
        skipped.append((path.name,'keyword'))
        continue
    # collect potential ingredient lines until a blank after we pass the title line index
    title_index = lines.index(title)
    body = lines[title_index+1:]
    # remove leading blanks
    while body and not body[0].strip(): body.pop(0)

    ingredient_lines = []
    instruction_lines = []

    i = 0
    # gather ingredient-like lines: stop when a blank line after at least one ingredient collected OR a line looks like a heading (ALL CAPS words >3) or contains sentence punctuation.
    while i < len(body):
        line = body[i].strip()
        if not line:
            if ingredient_lines:
                i += 1
                break
            else:
                i += 1
                continue
        if MEASURE_TOKENS.search(line):
            ingredient_lines.append(line)
            i += 1
            continue
        # heuristics: lines with 'cup','tsp','tbsp','kg','g','ml' even without number
        if re.search(r"\b(cup|cups|tsp|tbsp|gram|g|kg|ml|l|oz|teaspoon|tablespoon|pound|lb)\b", line, re.I):
            ingredient_lines.append(line)
            i += 1
            continue
        # otherwise break if we already have some ingredients
        if ingredient_lines:
            break
        else:
            i += 1
            continue
    # remaining lines -> instructions
    remainder = body[i:]
    # collapse multiple blanks and split into paragraphs
    paras = []
    buf = []
    for l in remainder:
        if l.strip():
            buf.append(l.strip())
        else:
            if buf:
                paras.append(' '.join(buf))
                buf = []
    if buf:
        paras.append(' '.join(buf))

    # form instructions
    instructions = [p.rstrip('.')+'.' if not p.endswith('.') else p for p in paras if p]
    # fallback: if no ingredients detected treat first paragraph as ingredients? skip for now
    if not ingredient_lines:
        skipped.append((path.name,'no-ingredients-detected'))
        continue

    slug = slugify(title)
    out_path = OUT / f"{slug}.md"
    with out_path.open('w') as f:
        f.write(f"# {title}\n\n")
        f.write("## Ingredients\n\n")
        for ing in ingredient_lines:
            f.write(f"- {ing}\n")
        f.write("\n## Instructions\n\n")
        for idx, step in enumerate(instructions, 1):
            f.write(f"{idx}. {step}\n")
    converted.append(out_path.name)

# write summary
summary_path = OUT / '_conversion_summary.txt'
with summary_path.open('w') as sf:
    sf.write('Converted files:\n')
    for n in converted:
        sf.write(f"  - {n}\n")
    sf.write('\nSkipped files:\n')
    for name, reason in skipped:
        sf.write(f"  - {name}: {reason}\n")

print(f"Done. Converted {len(converted)}; Skipped {len(skipped)}. See {summary_path}.")
