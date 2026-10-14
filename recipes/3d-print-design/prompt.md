# 3D Print Design

Goal: produce ONE original, 3D-printable product design worth modeling, printing, and potentially
selling — grounded in real evidence of what sells — as a **build-ready design package**: a written
spec, a machine-readable design spec, cited sources, and the description of a product mockup.

⚠️ **This package will later go to a 3D modeler** — a person in CAD or an automated modeling agent.
Every dimension, part, fit and construction step must be explicit enough to model the object from the
files alone. "Sized to taste", "appropriate thickness" or "the modeler will decide" is a defect —
pick the number.

Target date: **{{DATE_LONG}}** (`{{DATE}}`).

{{RUN_CONTRACT}}

--------------------------------------------------
## THIS RUN

**Subcategory: `{{SUBCATEGORY}}`** — chosen by the runner to keep the catalogue balanced. Do not pick
another. {{SUBCATEGORY_GUIDE}}

**Designs already published** (date · slug · title — pitch). Yours must be clearly different — not the
same object with a new name:

{{EXISTING}}

--------------------------------------------------
## WORKFLOW

1. **Research the market** with **WebSearch** (and **WebFetch**): maker and seller communities
   (r/3Dprinting, r/functionalprint, r/3DprintingBusiness, r/EtsySellers; Printables / MakerWorld /
   Thingiverse / Cults3D trending and most-downloaded pages; printer-maker community forums), articles
   on best-selling prints and profitable print farms, and marketplace listings with volume signals
   (review counts, bestseller badges, many sellers of one item type). Use `after:` qualifiers for
   some searches and **record exact URLs**. Use the research to choose a product category and demand
   signal — never copy an existing design. Yours is an original take that could stand next to the
   proven sellers.
2. **Choose the idea.** It must be:
   - **printable on a common consumer FDM printer**: every part fits **220 × 220 × 220 mm** (split
     larger objects into parts that assemble), PLA / PETG / TPU, no supports or minimal easy-to-remove
     ones, ideally one or two print sessions;
   - **commercially clean**: no team, league, brand or character names or logos, no licensed IP, no
     weapons or weapon parts, nothing for medical or safety-critical use, nothing that holds food
     long-term unless you say "use a food-safe coating". Sports ideas stay generic.
3. **Load the writing skills** (below) and write `README.md`, `design-spec.json` and `sources.csv`.
4. **Load `image-prompt-craft`** and write the mockup description into `cover_prompt`.
5. Check your own work before finishing: the JSON parses, the CSV has the right header, every part in
   the JSON appears in the README's parts table with the same dimensions, and every bounding box fits
   220 mm. The runner re-checks these and rejects the run if they fail.
6. End with the FINAL MESSAGE JSON.

--------------------------------------------------
## SKILLS (BINDING)

{{SKILLS}}

**Load `llm-writing` and `humanizer` before you write `README.md`, and run `humanizer`'s final pass
on it.** Carve-outs: ignore their workflow and output instructions (no audit, no report, no
questions); the OUTPUT FORMAT wins on structure; and **unsupported claims go or get sourced** —
"best-selling", "huge demand", "people love these" need a cited link or they come out. Numbers you
estimate (print time, grams, price) are labelled as estimates.

--------------------------------------------------
## OUTPUT FILES

{{OUTPUT_FILES}}

### `README.md`

No frontmatter. These headings, in this order:

```markdown
# <Product Title>

> <one sentence: what it is and why someone buys it>

**Date**: {{DATE}}
**Category**: {{SUBCATEGORY_LABEL}}
**Modeling difficulty**: Beginner | Intermediate | Advanced
**Estimated print**: ~<N> h total · ~<G> g <material> (estimate)
**Suggested price**: $<low>–$<high> printed · $<n> digital file (estimate)
**Status**: Concept

## Description
<2–3 short paragraphs: what it is, how it's used, what it looks like.>

## Why it sells
<The market evidence — comparable products, where they sell, the signals you found. Every claim
links a source. Then one sentence on the gap this design fills.>

## Who buys it
<The buyer, the occasion (gift, desk upgrade, display…), where they shop.>

## Design overview
<4–8 bullets on form and key features. Name the one feature that beats what's listed today.>

## Dimensions
| Measurement | Value (mm) | Notes |
|:--|--:|:--|
| Overall width (X) | … | |
| Overall depth (Y) | … | |
| Overall height (Z) | … | |
| Wall thickness | … | |
| <every other load-bearing dimension> | … | |

## Parts list
| Part | Qty | Material | Size X×Y×Z (mm) | Print orientation | Supports |
|:--|--:|:--|:--|:--|:--|

## Hardware and non-printed parts
<Exact specs — "6 × 3 mm N52 disc magnet ×4", "M3 × 8 mm button-head screw ×2", "M3 heat-set insert,
4.2 mm OD × 5.7 mm". "None — fully printed" if none.>

## Fits and tolerances
<Every mating interface: the parts, the fit type (press / sliding / snap / print-in-place /
threaded), and the clearance in mm. Default 0.2 mm per side sliding, 0.1–0.15 mm press, 0.3–0.4 mm
print-in-place gaps — and say why if you deviate.>

## Modeling guide
<Numbered steps per part for Fusion 360 / Onshape / FreeCAD / OpenSCAD: origin and axes named once,
then base sketch with dimensions → extrudes/revolves with depths → pockets and holes with diameters
and positions → fillets/chamfers with radii. Every step carries its numbers.>

## Print settings
| Setting | Value |
|:--|:--|
| Material | … |
| Nozzle | 0.4 mm |
| Layer height | … |
| Walls / perimeters | … |
| Infill | …% <pattern> |
| Supports | … |
| Brim / adhesion | … |
| Notes | <pause-at-height for magnets, colour changes…> |

## Assembly
<Numbered steps, or "No assembly — prints ready to use".>

## Variants and upsells
<Parametric variants, bundles, and for collectible series, the next pieces.>

## Selling and distribution
<Channels and which suits this product; pricing logic (material + machine time + margin); file vs
print vs both; file licence choice; 8–12 listing keywords.>

## Risks and IP notes
- <3–5 design / market / IP risks, each with a one-line mitigation>

## Resource links
- [<title>](<url>) — <what it shows>   (4–8, matching sources.csv)
```

### `design-spec.json`

Strict JSON, millimetres throughout, numbers wherever a number is possible — this is what a
modeling agent consumes:

```json
{
  "schema": "print-design/v1",
  "title": "<Product Title>",
  "slug": "<slug>",
  "date": "{{DATE}}",
  "subcategory": "{{SUBCATEGORY}}",
  "units": "mm",
  "summary": "<one sentence>",
  "overall_dimensions": { "x": 0, "y": 0, "z": 0 },
  "coordinate_system": "<origin and +X/+Y/+Z directions>",
  "target_printer": { "process": "FDM", "build_volume": { "x": 220, "y": 220, "z": 220 }, "nozzle": 0.4 },
  "parts": [
    {
      "id": "<kebab-id>",
      "name": "<Part name, exactly as in the README parts table>",
      "quantity": 1,
      "material": "PLA | PETG | TPU",
      "bounding_box": { "x": 0, "y": 0, "z": 0 },
      "base_shape": "<e.g. rounded rectangle 80 x 60, corner radius 6>",
      "construction_steps": ["<ordered CAD operations, each with its numbers>"],
      "features": [
        { "type": "hole | pocket | slot | boss | fillet | chamfer | thread | text | snap | hinge",
          "description": "<what>", "dimensions": {}, "position": { "x": 0, "y": 0, "z": 0 } }
      ],
      "print_orientation": "<which face down>",
      "supports": "none | minimal: <where>",
      "estimated_print_time_h": 0,
      "estimated_filament_g": 0
    }
  ],
  "fits": [{ "between": ["<part-id>", "<part-id>"], "type": "press | sliding | snap | print-in-place | threaded", "clearance_per_side": 0.2 }],
  "hardware": [{ "item": "<exact spec>", "quantity": 0, "notes": "<pocket size / install>" }],
  "assembly_steps": ["<step>"],
  "print_settings": { "layer_height": 0.2, "walls": 3, "infill_percent": 15, "infill_pattern": "gyroid", "supports": "none", "adhesion": "none" },
  "parametric_variables": [{ "name": "<snake_case>", "default": 0, "min": 0, "max": 0, "affects": ["<part-id>"] }],
  "pricing": { "printed_usd": [0, 0], "digital_file_usd": 0, "estimate": true },
  "sources": ["<url>"]
}
```

`parts`, `fits`, `hardware` and `parametric_variables` may be empty arrays when genuinely not
applicable — never omit a key. No zeros left over from the template.

### `sources.csv`

Strict CSV, header `title,url,note`, 4–8 rows, quoting any field with a comma.

Rules: 4–8 real sources, cited in the README, the JSON `sources`, and the CSV. Never fabricate
sources, sales figures, review counts, sellers or products — if you can't verify a number, don't
state it. README and JSON agree on parts, dimensions and hardware. Exact dates.

--------------------------------------------------
## COVER IMAGE (the product mockup)

`cover_prompt` describes **a studio product photograph of the finished, 3D-printed object** — not a
CAD screenshot, blueprint or exploded diagram. Follow `image-prompt-craft`; these rules win:

- Describe the object's real shape, proportions and features from your spec, the material (matte
  PLA, satin PETG, flexible TPU), and faint horizontal layer lines that read as FDM-printed.
- Name a **2–3 colour filament palette** (e.g. "charcoal grey and signal orange matte PLA").
- Show it in use or in context where that helps, three-quarter view, soft diffused studio light,
  shallow depth of field, clean background, the object filling about 60% of the frame (the runner
  renders it square — don't write the ratio).
- ⚠️ Never call it a "listing photo", "product page", "advertisement", "catalog page" or
  "infographic" — those carry text.
- **No text, logos, brand marks, team insignia or recognisable people.** Personalised text on the
  object is shown blank.
- End with the skill's constraint block, verbatim.

--------------------------------------------------
## FINAL MESSAGE

```json
{
  "title": "<Product Title>",
  "slug": "<kebab-case-slug>",
  "summary": "<the one-sentence pitch>",
  "subcategory": "{{SUBCATEGORY}}",
  "modeling_difficulty": "<Beginner | Intermediate | Advanced>",
  "cover_prompt": "<the full mockup description>",
  "error": null
}
```
