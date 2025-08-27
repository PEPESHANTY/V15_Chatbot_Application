cypher = """
// ===============================
// Chapter 2 (Part 2) — Seed Preparation for Mekong Delta
// Single-statement, idempotent upsert with :Searchable + search_text
// ===============================

// Ensure Chapter 2 exists and is addressable
MERGE (ch2:Chapter {entity_id: 'Cultivation Techniques - Ch2'})
SET ch2:Searchable,
    ch2.entity_type = 'chapter',
    ch2.chapter     = 'Ch2',
    ch2.file_path   = coalesce(ch2.file_path, 'book_1.pdf')

// === Seed Preparation Section ===
WITH ch2
MERGE (seed:Practice:Searchable {
  entity_id:  'Seed Preparation - Ch2',
  entity_type:'practice',
  name:       'Seed Preparation'
})
SET seed.chapter     = 'Ch2',
    seed.source_id   = 'chunk-ch2-002',
    seed.description = 'Comprehensive seed preparation protocol for Mekong Delta rice farming per Decision 73/QĐ-TT-VPPN: use certified seed; do not exceed 70 kg/ha; sunlight exposure 2–3 h pre-soak; soak 24–48 h (change water at 12 h); incubate 30–35°C for 12–24 h to nút nanh (0.5–1.0 mm radicle); if delayed, hold sprouts in cool shade; shallow sowing depth 1–3 mm; spacing: row 20–30 cm, cluster 12–20 cm; fertilizer placement 3.0–4.0 cm during sowing; adjust seed amount for non-germinated and mechanical loss.',
    seed.search_text = 'seed preparation | Decision 73/QĐ-TT-VPPN | certified seed | ≤70 kg/ha | sunlight 2–3 h | soak 24–48 h | change water 12 h | incubate 30–35°C 12–24 h | nút nanh 0.5–1.0 mm | cool shaded holding | sowing depth 1–3 mm | row 20–30 cm | cluster 12–20 cm | fertilizer 3.0–4.0 cm | mechanical loss | germination rate'
MERGE (ch2)-[:COVERS {
  description:'Chapter 2 includes seed preparation as a critical practice before sowing.',
  source_id:'chunk-ch2-002'
}]->(seed)

// === Certified Seeds
WITH seed
MERGE (cert:Concept:Searchable {
  entity_id:  'Certified Seed - Ch2',
  entity_type:'input',
  name:       'Certified Seed'
})
SET cert.chapter     = 'Ch2',
    cert.source_id   = 'chunk-ch2-002',
    cert.description = 'Government-approved, officially circulated varieties ensuring purity, vigor, and uniform stands for mechanized systems.',
    cert.search_text = 'certified seed | approved variety | varietal purity | vigor | uniform stand | mechanized sowing compatibility'
MERGE (seed)-[:REQUIRES {source_id:'chunk-ch2-002'}]->(cert)

// === Seeding Rate
WITH seed
MERGE (rate:Parameter:Searchable {
  entity_id:  'Seeding Rate - Ch2',
  entity_type:'parameter',
  name:       'Seeding Rate Limit'
})
SET rate.chapter     = 'Ch2',
    rate.source_id   = 'chunk-ch2-002',
    rate.description = 'Do not exceed 70 kg/ha to avoid overcrowding, reduce cost, and ensure uniform crop stands under mechanized sowing.',
    rate.search_text = 'seeding rate | ≤70 kg/ha | avoid overcrowding | cost optimization | uniform stand | mechanized seeding'
MERGE (seed)-[:FOLLOWS {source_id:'chunk-ch2-002'}]->(rate)

// === Germination Length (nút nanh)
WITH seed
MERGE (germ:Concept:Searchable {
  entity_id:  'Germination Length - Ch2',
  entity_type:'parameter',
  name:       'Ideal Germination Length'
})
SET germ.chapter     = 'Ch2',
    germ.source_id   = 'chunk-ch2-002',
    germ.description = 'Radicle length at sowing: 0.5–1.0 mm (nút nanh) for optimal mechanical sowing performance and reduced damage.',
    germ.search_text = 'germination length | nút nanh | 0.5–1.0 mm | mechanical sowing | reduce damage | uniform emergence'
MERGE (seed)-[:TARGETS {source_id:'chunk-ch2-002'}]->(germ)

// === Sunlight Pre-treatment
WITH seed
MERGE (sun:Step:Searchable {
  entity_id:  'Sun Exposure - Ch2',
  entity_type:'step',
  name:       'Sunlight Exposure'
})
SET sun.chapter     = 'Ch2',
    sun.source_id   = 'chunk-ch2-002',
    sun.description = 'Expose seeds to sunlight for 2–3 hours prior to soaking to prime moisture uptake and boost germination response.',
    sun.search_text = 'sunlight exposure | pre-soak | 2–3 hours | prime germination | moisture uptake'
MERGE (seed)-[:INCLUDES {source_id:'chunk-ch2-002'}]->(sun)

// === Soaking & Incubation
WITH seed
MERGE (soak:Process:Searchable {
  entity_id:  'Soaking and Incubation - Ch2',
  entity_type:'method',
  name:       'Seed Soaking and Incubation'
})
SET soak.chapter     = 'Ch2',
    soak.source_id   = 'chunk-ch2-002',
    soak.description = 'Soak 24–48 h in clean water (change after 12 h to prevent souring and remove unfilled seeds). Incubate 30–35°C for 12–24 h until radicle emerges (nút nanh).',
    soak.search_text = 'soak 24–48 h | change water 12 h | prevent souring | remove unfilled seeds | incubate 30–35°C 12–24 h | radicle emergence | nút nanh'
MERGE (seed)-[:USES {source_id:'chunk-ch2-002'}]->(soak)

// === Holding sprouted seeds (if sowing is delayed)
WITH seed
MERGE (hold:Condition:Searchable {
  entity_id:  'Sprout Holding - Ch2',
  entity_type:'condition',
  name:       'Sprout Holding Conditions'
})
SET hold.chapter     = 'Ch2',
    hold.source_id   = 'chunk-ch2-002',
    hold.description = 'If sowing is delayed, spread germinated seeds thinly in cool, shaded, ventilated areas to prevent elongation, tangling, and damage.',
    hold.search_text = 'holding sprouts | cool shaded area | prevent elongation | avoid entanglement | delay management'
MERGE (seed)-[:REQUIRES {source_id:'chunk-ch2-002'}]->(hold)

// === Sowing Depth
WITH seed
MERGE (depth:Parameter:Searchable {
  entity_id:  'Sowing Depth - Ch2',
  entity_type:'parameter',
  name:       'Sowing Depth'
})
SET depth.chapter     = 'Ch2',
    depth.source_id   = 'chunk-ch2-002',
    depth.description = 'Maintain shallow depth of 1–3 mm for good seed-to-soil contact and rapid emergence in mechanized systems.',
    depth.search_text = 'sowing depth | 1–3 mm | seed-to-soil contact | rapid emergence | mechanized sowing'
MERGE (seed)-[:USES {source_id:'chunk-ch2-002'}]->(depth)

// === Sowing Spacing
WITH seed
MERGE (space:Parameter:Searchable {
  entity_id:  'Row and Cluster Spacing - Ch2',
  entity_type:'parameter',
  name:       'Sowing Spacing'
})
SET space.chapter     = 'Ch2',
    space.source_id   = 'chunk-ch2-002',
    space.description = 'Row sowing: 20–30 cm; Cluster sowing: 12–20 cm both between rows and within clusters for uniform distribution.',
    space.search_text = 'row spacing 20–30 cm | cluster spacing 12–20 cm | uniform distribution | mechanized sowing'
MERGE (seed)-[:REQUIRES {source_id:'chunk-ch2-002'}]->(space)

// === Fertilizer Integration during sowing
WITH seed
MERGE (fert:Input:Searchable {
  entity_id:  'Fertilizer Placement - Ch2',
  entity_type:'input',
  name:       'Fertilizer Incorporation'
})
SET fert.chapter     = 'Ch2',
    fert.source_id   = 'chunk-ch2-002',
    fert.description = 'Place fertilizer at 3.0–4.0 cm depth during sowing to improve nutrient uptake and early vigor.',
    fert.search_text = 'fertilizer placement | 3.0–4.0 cm depth | nutrient uptake | early vigor | mechanized placement'
MERGE (seed)-[:INTEGRATES_WITH {source_id:'chunk-ch2-002'}]->(fert)

// === Seed Rate Formula (adjustment)
// Adjusted rate = base × (1 + %non-germinated + %mechanical loss)
WITH seed
MERGE (formula:Formula:Searchable {
  entity_id:  'Seed Rate Formula - Ch2',
  entity_type:'calculation',
  name:       'Seed Quantity Adjustment Formula'
})
SET formula.chapter     = 'Ch2',
    formula.source_id   = 'chunk-ch2-002',
    formula.description = 'Adjusted seed amount accounts for non-germinated seeds and mechanical loss. Example: at 90% germination, add 10% for non-germinated + 5% for mechanical loss → 115% of base.',
    formula.search_text = 'seed rate formula | germination rate | mechanical loss | 90% germination → 115% | calculation'
MERGE (seed)-[:CALCULATES_USING {source_id:'chunk-ch2-002'}]->(formula)

// === Seeder Equipment
WITH seed
MERGE (machine:Tool:Searchable {
  entity_id:  'Rice Seeder - Ch2',
  entity_type:'tool',
  name:       'Seeder Machine'
})
SET machine.chapter     = 'Ch2',
    machine.source_id   = 'chunk-ch2-002',
    machine.description = 'Row (sạ hàng) or cluster (sạ cụm) seeders used for consistent, mechanized seed placement compatible with fertilizer co-placement.',
    machine.search_text = 'seeder machine | row seeder | cluster seeder | mechanized sowing | fertilizer co-placement'
MERGE (seed)-[:REQUIRES_TOOL {source_id:'chunk-ch2-002'}]->(machine)
"""
