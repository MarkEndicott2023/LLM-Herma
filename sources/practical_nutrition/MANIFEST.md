# Source Manifest — Practical Nutrition

Last verified: 2026-07-29. Every PDF was opened and confirmed to be the document
its filename claims; the CSV datasets were parsed and row-counted.

## Files

All filenames are year-tagged. The suffix is the **publication year**, except
`usda_dga_2025_2030` (edition span — its published title; released 2026-01-07) and
`cochrane_citation_export_2026` / `food_data_central_2026` (snapshot/export year,
since their contents span multiple years).

| File | Document | Authority | Status |
|---|---|---|---|
| `cochrane_citation_export_2026.csv` | 20 rows / **18 unique** CDSR reviews (published 2019–2026), structured abstracts w/ per-outcome GRADE, effect sizes, CIs, funding | Cochrane | ⚠️ 3 duplicate DASH rows |
| `food_data_central_2026/` | FoodData Central **Foundation Foods** relational dump, 24 CSVs + field-description XLSX | USDA ARS | ✅ profiled below |
| `nasem_dri_summary_tables_2019.pdf` | Appendix J, *DRI for Sodium and Potassium* (2019), 18 pp | NASEM Food & Nutrition Board | ✅ verified |
| `usda_dga_2025_2030.pdf` | Dietary Guidelines for Americans 2025–2030 (released 2026-01-07) | USDA / HHS | ✅ verified |
| `who_sfa_tfa_2023.pdf` | *Saturated fatty acid and trans-fatty acid intake for adults and children* | WHO | ✅ verified |
| `who_carbohydrate_intake_2023.pdf` | *Carbohydrate intake for adults and children* | WHO | ✅ verified |
| `who_sugars_2015.pdf` | *Guideline: Sugars intake for adults and children* | WHO | ✅ verified |
| `who_healthy_diet_2026.pdf` | *Healthy diet* fact sheet, dated 2026-01-26 | WHO | ✅ verified |
| `issn_protein_exercise_2017.pdf` | Jäger et al. 2017, JISSN 14:20, `10.1186/s12970-017-0177-8` | ISSN | ✅ verified |
| `issn_body_composition_2017.pdf` | Aragon et al. 2017, JISSN 14:16, `10.1186/s12970-017-0174-y` | ISSN | ✅ verified |
| `issn_nutrient_timing_2017.pdf` | Kerksick et al. 2017, JISSN 14:33, `10.1186/s12970-017-0189-4` | ISSN | ✅ verified |
| `fda_dv_micro_2016.pdf` | Nutrition Facts labeling FAQ + **RDIs – Nutrients** table (27 micronutrients + protein) | FDA | ✅ verified |
| `fda_dv_macro_2016.pdf` | Nutrition Facts labeling FAQ + **DRVs – Food Components** table (8 macros) | FDA | ✅ verified |

The `issn_nutient_timing` → `issn_nutrient_timing` typo was corrected during the
year-tagging rename.

### ⚠️ Daily Values are not DRIs

The two `fda_dv_*_2016.pdf` files are Nutrition Facts label reference values from
FDA's 2016 final rule, sourced from Federal Register document `2016-11867`
(micro: pp. 903–904; macro: p. 905). Daily Values comprise RDIs (nutrients) and
DRVs (food components), computed against a 2,000 kcal reference intake.

**They are not requirement estimates.** No EAR, no RDA, no Tolerable Upper Intake
Level, no life-stage stratification. A %DV is a legal labeling definition, not a
scientific finding — FDA is the authority for US labels specifically, and has no
standing on what a person actually needs. For requirements, use
`nasem_dri_summary_tables_2019.pdf`.

**Teach from these:** Nutrition Facts / Supplement Facts label reading, %DV
arithmetic, the complete current nutrient roster. Micro RDIs include vitamin A
900 µg RAE, vitamin D 20 µg, calcium 1,300 mg, iron 18 mg, zinc 11 mg, iodine
150 µg, potassium 4,700 mg, choline 550 mg. Macro DRVs: fat 78 g, saturated fat
20 g, total carbohydrate 275 g, fibre 28 g, sodium 2,300 mg, added sugars 50 g,
protein 50 g.

**Do not teach from these:** individual requirements, EAR/RDA/AI distinctions,
upper limits, or life-stage variation.

### Freshness watch

| File | Age | Note |
|---|---|---|
| `who_sugars_2015.pdf` | 11 yrs | Oldest guideline here. Free-sugars recommendation is still current WHO policy, but check for a successor before teaching as live guidance |
| `issn_*_2017.pdf` | 9 yrs | ISSN has issued newer stands on other topics; these three have not been superseded as of this check |
| `nasem_dri_summary_tables_2019.pdf` | 7 yrs | Most recent comprehensive DRI compilation. **Energy DRIs were revised in 2023 and are not in this file** |
| `fda_dv_*_2016.pdf` | 10 yrs | Still the operative US labeling rule, so age is not a defect here — a DV changes only when FDA amends the regulation |
| `cochrane_citation_export_2026.csv` | current | CDSR reviews are updated in place; re-export periodically |

## FoodData Central profile

This is the **Foundation Foods** download — lab-analyzed whole foods with full
sample provenance. It is *not* the complete FDC: no SR Legacy, no FNDDS survey
foods, no Branded Foods. (`food_category.csv` lists a "Branded Food Products
Database" category, but that is only the lookup table — no branded rows are present.)

| Table | Rows | Use |
|---|---|---|
| `food.csv` | 87,991 | master food records; see data_type split below |
| `foundation_food.csv` | 395 | the actual Foundation food list (fdc_id, NDB_number, footnote) |
| `food_nutrient.csv` | 170,469 | nutrient amount per food — the core join |
| `nutrient.csv` | 477 | nutrient definitions + units |
| `food_portion.csv` | 10,951 | household measure → gram weight |
| `measure_unit.csv` | 123 | unit lookup |
| `food_category.csv` | 28 | category lookup |
| `sub_sample_result.csv` | 134,267 | individual lab assay results |
| `lab_method.csv` / `lab_method_nutrient.csv` | 305 / 671 | analytical method per nutrient |

`food.csv` by `data_type`: `sub_sample_food` 75,055 · `market_acquisition` 7,577 ·
`sample_food` 4,079 · `agricultural_acquisition` 810 · **`foundation_food` 469**.

So the teachable food count is roughly 400–470 — the other ~87,500 rows are the
sampling and assay chain behind those foods. Examples: *Hummus, commercial*;
*Tomatoes, grape, raw*; *Nuts, almonds, dry roasted, with salt added*;
*Frankfurter, beef, unheated*.

**Good for:** nutrient density comparisons across whole foods, portion arithmetic,
protein/energy per 100 g, and — unusually — teaching measurement provenance, since
the assay method and sample chain are queryable.

**Not good for:** packaged/branded product lookup, restaurant items, or composite
dishes. Add SR Legacy or FNDDS if those are in scope.

**Teaching artifact worth keeping:** `nutrient.csv` id 1006 is literally named
`Fiber, crude (DO NOT USE - Archived)`. A real lesson in reading a schema before
trusting a column.

### DRI file contents

`nasem_dri_summary_tables.pdf` carries the complete DRI set — Estimated Average
Requirements; RDAs and AIs for vitamins, elements, and total water +
macronutrients; Acceptable Macronutrient Distribution Ranges; Additional
Macronutrient Recommendations; Chronic Disease Risk Reduction Intakes; and
Tolerable Upper Intake Levels for vitamins and elements.

2019 vintage, so post-2011-revision: calcium and vitamin D EARs are present
(800 mg/d and 10 µg/d for adults 19–50). Protein EAR 0.66 g/kg/d, carbohydrate
EAR 100 g/d. Energy DRIs were revised separately in 2023 and are not in this file.

**Rendering caveat:** the print-to-PDF mangled Greek characters — µg/d appears as
"Rg/d", α-tocopherol as "F-tocopherol", β-carotene as "G-carotene". Numeric
content is intact; read units contextually, not literally.

## Cochrane review inventory

CSV columns: `Cochrane Review ID, Author(s), Title, Source, Year, Abstract, Issue,
Publisher, ISSN, Keywords, DOI, URL, Cochrane Review Group Code`

The `Abstract` field is a full structured abstract — Rationale, Objectives, Search
methods, Eligibility, Outcomes, Risk of bias, Synthesis methods, Included studies,
Synthesis of results, Authors' conclusions, Funding, Registration, Plain language
summary. Per-outcome GRADE ratings and effect sizes are inline in "Synthesis of
results". This is the richest artifact source in the directory.

### Tier A — directly relevant (adult, practical)

| ID | Title | Year | Certainty profile | Teaching value |
|---|---|---|---|---|
| CD015610.PUB2 | Intermittent fasting for adults with overweight or obesity | 2026 | 1 mod / 2 low / 4 v.low | **Null result** vs. regular dietary advice |
| CD015092.PUB2 | Semaglutide for adults living with obesity | 2025 | 2 high / 9 mod / 3 low / 2 v.low | High-certainty benefit + 17/18 trials industry-funded |
| CD016018 | Tirzepatide for adults living with obesity | 2025 | 8 mod / 6 low / 2 v.low | All trials manufacturer-funded |
| CD016017 | Liraglutide for adults living with obesity | 2025 | 5 mod / 5 low / 8 v.low | Weaker profile than semaglutide; 22 industry-funded |
| CD013617.PUB2 | HIIT for cardiometabolic syndrome in sedentary adults | 2026 | 1 high / 4 mod / 4 low / 1 v.low | High-certainty waist circumference −3.56 cm |
| CD007654.PUB6 | Long-term effects of weight-reducing drugs in hypertension | 2026 | 4 mod / 6 v.low | Evidence insufficient despite many trials |

### Tier B — adjacent

| ID | Title | Year | Certainty profile |
|---|---|---|---|
| CD004366.PUB7 | Exercise for depression | 2026 | 1 mod / 3 low |
| CD014794.PUB2 | School feeding programs (socioeconomic disadvantage) | 2025 | 2 high / 2 mod / 2 low |

### Tier C — pediatric (off-target topically, useful methodologically)

| ID | Title | Year | Certainty profile |
|---|---|---|---|
| CD015988 | Physical activity for obesity in children ≤9y | 2026 | **16 v.low, nothing else** |
| CD015986 | Pharmacological interventions, children/adolescents | 2026 | 2 mod / 3 low |
| CD016063 | Multimodal behaviour interventions, children + parents | 2025 | 7 mod / 8 low / 3 v.low |
| CD016062 | Multimodal behaviour interventions, adolescents | 2025 | 1 mod / 12 low / 2 v.low |

### Tier D — clinical, low relevance

| ID | Title | Year |
|---|---|---|
| CD012161.PUB2 | (Ultra-)short-acting insulin analogues, T1D | 2026 |
| CD015906.PUB2 | DPP-4 inhibitors, CKD + diabetes | 2025 |

### Tier A — dietary patterns and fats

Four reviews sharing one outcome framework (primary + secondary CVD prevention),
which makes their certainty ratings directly comparable. That comparability is the
teaching asset — same question, same method, four different answers.

| ID | Title | Year | Group | Certainty profile |
|---|---|---|---|---|
| CD003177.PUB5 | Omega-3 fatty acids for primary and secondary prevention of CVD | 2020 | Heart | **5 high / 7 mod / 8 low** |
| CD013729.PUB2 | Dietary Approaches to Stop Hypertension (DASH) for primary and secondary prevention of CVD | 2025 | Central Editorial | see note |
| CD009825.PUB3 | Mediterranean-style diet for primary and secondary prevention of CVD | 2019 | Heart | see note |
| CD013501.PUB2 | Vegan dietary pattern for primary and secondary prevention of CVD | 2021 | Heart | 3 mod / 2 low / 2 v.low |

**CD003177.PUB5 (omega-3)** is the strongest evidence base in the entire export —
five high-certainty outcomes, and self-described as "the most extensive systematic
assessment of effects of omega-3 fats on cardiovascular health to date." Increasing
LCn3 slightly reduces CHD mortality and events and lowers serum triglycerides;
ALA slightly reduces cardiovascular events and arrhythmia. Use this as the
contrast case against the very-low-certainty reviews.

**CD013729.PUB2 (DASH)** — cardiovascular endpoints (MI, stroke, CV mortality,
all-cause mortality) remain **inconclusive** for lack of long-term evidence, and
no trials assessed heart failure or revascularisation. DASH may reduce blood
pressure, total cholesterol and triglycerides and raise HDL, but has little to no
effect on LDL. A useful corrective: DASH is widely recommended, yet its hard-outcome
evidence is thin.

**CD013501.PUB2 (vegan)** — no included study reported CVD clinical events at all;
"insufficient information to draw conclusions." Eight ongoing studies.

**Certainty-tally caveat:** CD009825 (2019), CD013729 (2025) and CD013501 use
wording that the automated tally misses or undercounts — CD009825 uses
pre-standardisation "low or moderate *quality* evidence" phrasing. Read the
certainty ratings for these three from the abstract text directly, not from a
keyword count.

### ⚠️ Duplicate rows in the CSV

`CD013729.PUB2` (DASH) appears **three times** — rows 16, 17 and 19 of 20. Unique
review count is **18**, not 20. Dedup by `Cochrane Review ID` before treating row
count as review count.

## Coverage by concept area

| Area | Status | Source |
|---|---|---|
| Evidence appraisal / GRADE | ✅ strong | Cochrane CSV (spans high → very-low certainty) |
| Micronutrient requirements (EAR/RDA/AI/UL) | ✅ strong | `nasem_dri_summary_tables_2019` |
| Macronutrient distribution (AMDR) | ✅ strong | `nasem_dri_summary_tables_2019` |
| Energy balance, deficit/surplus | ✅ strong | `issn_body_composition_2017` |
| Protein: amount, source, distribution | ✅ strong | `issn_protein_exercise_2017`, `issn_nutrient_timing_2017` |
| Dietary archetypes (LCD, KD, HPD, IF) | ✅ strong | `issn_body_composition_2017`, CD015610 |
| Carbohydrate quality + performance | ✅ strong | `who_carbohydrate_intake_2023`, `issn_nutrient_timing_2017` |
| Sodium / potassium | ✅ good | DRI Chronic Disease Risk Reduction Intakes |
| Fibre | ✅ good | `who_carbohydrate_intake_2023` (≥25 g/d) |
| Saturated / trans fat | ✅ good | `who_sfa_tfa_2023`, `usda_dga_2025_2030` |
| Obesity pharmacotherapy (GLP-1s) | ✅ good | CD015092 / CD016018 / CD016017 |
| Body composition assessment | ✅ adequate | `issn_body_composition_2017` |
| Added sugars | ✅ good | `who_sugars_2015`, `usda_dga_2025_2030` |
| Dietary patterns (Mediterranean, DASH, vegan) | ✅ strong | CD009825.PUB3, CD013729.PUB2, CD013501.PUB2 |
| Omega-3 / fish oil | ✅ strong | CD003177.PUB5 — highest-certainty review in the set |
| Food composition, nutrient density | ✅ good | `food_data_central_2026` (whole foods only) |
| Portion arithmetic | ✅ good | `food_portion.csv`, `measure_unit.csv` |
| Measurement provenance / data hygiene | ✅ good | FDC lab_method + sub_sample tables |
| General healthy-diet framing | ✅ good | `who_healthy_diet_2026` |
| DASH pattern specifically | 🟡 partial | `usda_dga_2025_2030` only; no dedicated review |
| Nutrition Facts label reading / %DV | ✅ good | `fda_dv_micro_2016`, `fda_dv_macro_2016` |
| Nutrient roster + label targets | ✅ good | `fda_dv_micro_2016` |
| Packaged / branded / restaurant foods | 🔴 missing | Foundation Foods excludes them |
| Energy availability / RED-S | 🔴 missing | — |

## Outstanding

| Priority | Item | Where |
|---|---|---|
| 1 | **Dedup the CSV** — 3 identical `CD013729.PUB2` rows | local edit |
| 2 | *(optional)* SR Legacy or FNDDS from FDC — adds packaged and composite foods | [fdc.nal.usda.gov](https://fdc.nal.usda.gov/download-datasets) |
| 3 | *(optional)* AND/DC/ACSM 2016 — paywalled; energy availability / RED-S | [jandonline](https://www.jandonline.org/article/S2212-2672(15)01802-X/abstract) |
| 4 | *(optional)* WHO sodium 2012 — DRI CDRR already covers sodium | [9789241504836](https://www.who.int/publications/i/item/9789241504836) |

No blockers. Dietary patterns went from the weakest area to one of the strongest.
Every core concept area for a 30–40 concept broad-literacy graph is sourced;
remaining items only widen coverage at the edges.
