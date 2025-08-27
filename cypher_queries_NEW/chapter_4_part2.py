cypher = """
// =======================================================
// Chapter 4 (Part 2) — In-field Straw Treatment (single statement)
// =======================================================

// --- In-field straw treatment practice ---
MERGE (treat:Practice:Searchable {
  entity_id:  'In-field Straw Treatment - Ch4',
  entity_type:'practice',
  name:       'In-field Straw Treatment'
})
SET treat.chapter     = 'Ch4',
    treat.source_id   = 'chunk-ch4-002',
    treat.description = 'Plow/chop stubble into soil under dry, non-flooded conditions; apply microbial inoculants (e.g., Trichoderma) to accelerate decomposition and reduce emissions.',
    treat.search_text = 'stubble incorporation | plow | chop | non-flooded 3+ weeks | microbial inoculant | Trichoderma | aerobic decomposition | methane reduction'

// Link to Chapter 4
WITH treat
MATCH (ch4:Chapter {entity_id:'Straw Management - Ch4'})
MERGE (ch4)-[:COVERS {source_id:'chunk-ch4-002'}]->(treat)

// --- Season-specific guidance ---
WITH treat
MERGE (winter:Season:Searchable {
  entity_id:  'Winter-Spring Crop - Ch4',
  entity_type:'season',
  name:       'Winter–Spring'
})
SET winter.chapter     = 'Ch4',
    winter.source_id   = 'chunk-ch4-002',
    winter.description = 'Immediately plow/bury stubble after harvest; keep field non-flooded for ≥3 weeks for aerobic decomposition.',
    winter.search_text = 'Winter–Spring | immediate plow | non-flooded ≥3 weeks | aerobic decomposition'
MERGE (treat)-[:APPLIES_DURING {source_id:'chunk-ch4-002'}]->(winter)

MERGE (summer:Season:Searchable {
  entity_id:  'Summer-Autumn & Autumn-Winter Crops - Ch4',
  entity_type:'season',
  name:       'Summer–Autumn & Autumn–Winter'
})
SET summer.chapter     = 'Ch4',
    summer.source_id   = 'chunk-ch4-002',
    summer.description = 'Till immediately after harvest; spray Trichoderma before plowing to speed decomposition, especially in short cycles.',
    summer.search_text = 'Summer–Autumn | Autumn–Winter | immediate till | Trichoderma spray | short cycles'
MERGE (treat)-[:APPLIES_DURING {source_id:'chunk-ch4-002'}]->(summer)

// --- Biological treatment inputs/methods ---
WITH treat
MERGE (tricho:Input:Searchable {
  entity_id:  'Trichoderma - Ch4',
  entity_type:'input',
  name:       'Trichoderma'
})
SET tricho.chapter     = 'Ch4',
    tricho.source_id   = 'chunk-ch4-002',
    tricho.description = 'Microbial agent applied before plowing to accelerate straw breakdown; recommended ~0.1% of straw volume.',
    tricho.search_text = 'Trichoderma | microbial agent | 0.1% volume | faster decomposition'
MERGE (treat)-[:USES {source_id:'chunk-ch4-002'}]->(tricho)

MERGE (bio:Method:Searchable {
  entity_id:  'Biological Decomposition - Ch4',
  entity_type:'method',
  name:       'Biological Decomposition'
})
SET bio.chapter     = 'Ch4',
    bio.source_id   = 'chunk-ch4-002',
    bio.description = 'Incorporate straw under dry (non-flooded) conditions with microbial inoculants to enhance aerobic decomposition and soil health.',
    bio.search_text = 'biological decomposition | microbial inoculant | aerobic | soil health'
MERGE (treat)-[:USES {source_id:'chunk-ch4-002'}]->(bio)

// --- Machinery for incorporation ---
WITH treat, bio
MERGE (tiller:Equipment:Searchable {
  entity_id:  'Rotary Tiller - Ch4',
  entity_type:'equipment',
  name:       'Rotary Tiller'
})
SET tiller.chapter     = 'Ch4',
    tiller.source_id   = 'chunk-ch4-002',
    tiller.description = 'Incorporates stubble at 10–15 cm depth to mix residues and promote decomposition.',
    tiller.search_text = 'rotary tiller | 10–15 cm | residue mixing | decomposition'
MERGE (treat)-[:USES {source_id:'chunk-ch4-002'}]->(tiller)

MERGE (tractor:Equipment:Searchable {
  entity_id:  'Tractor for Tillage - Ch4',
  entity_type:'equipment',
  name:       'Tractor for Tillage'
})
SET tractor.chapter     = 'Ch4',
    tractor.source_id   = 'chunk-ch4-002',
    tractor.description = 'Tractor powers rotary tiller to plow/bury stubble; readies field for next cycle.',
    tractor.search_text = 'tractor | plow | bury stubble | field prep'
MERGE (treat)-[:USES {source_id:'chunk-ch4-002'}]->(tractor)

// --- Conditions & warnings ---
WITH treat, bio
MERGE (dry_cond:Condition:Searchable {
  entity_id:  'Dry Field Condition - Ch4',
  entity_type:'condition',
  name:       'Dry Field Condition'
})
SET dry_cond.chapter     = 'Ch4',
    dry_cond.source_id   = 'chunk-ch4-002',
    dry_cond.description = 'After incorporation, keep field non-flooded ≥3 weeks to ensure aerobic decomposition and avoid methane.',
    dry_cond.search_text = 'non-flooded ≥3 weeks | aerobic | avoid methane'
MERGE (treat)-[:REQUIRES {source_id:'chunk-ch4-002'}]->(dry_cond)

MERGE (flooded_cond:Threat:Searchable {
  entity_id:  'Flooded Straw Burial - Ch4',
  entity_type:'threat',
  name:       'Flooded Straw Burial'
})
SET flooded_cond.chapter     = 'Ch4',
    flooded_cond.source_id   = 'chunk-ch4-002',
    flooded_cond.description = 'Anaerobic decomposition in flooded fields produces methane and causes nutrient loss.',
    flooded_cond.search_text = 'flooded burial | anaerobic | methane | nutrient loss'
MERGE (treat)-[:AVOIDS {source_id:'chunk-ch4-002'}]->(flooded_cond)

MERGE (burn_straw:Threat:Searchable {
  entity_id:  'Straw Burning - Ch4',
  entity_type:'threat',
  name:       'Straw Burning'
})
SET burn_straw.chapter     = 'Ch4',
    burn_straw.source_id   = 'chunk-ch4-002',
    burn_straw.description = 'Prohibited due to air pollution and complete nitrogen loss.',
    burn_straw.search_text = 'burning | air pollution | nitrogen loss'
MERGE (treat)-[:AVOIDS {source_id:'chunk-ch4-002'}]->(burn_straw)

// --- Nutrient composition & losses ---
WITH treat, bio, flooded_cond, burn_straw
MERGE (nutrients:Concept:Searchable {
  entity_id:  'Nutrient Composition in Straw - Ch4',
  entity_type:'concept',
  name:       'Nutrient Composition in Straw'
})
SET nutrients.chapter     = 'Ch4',
    nutrients.source_id   = 'chunk-ch4-002',
    nutrients.description = 'Approx. per ton of straw: 5–8 kg N, 1.6–2.7 kg P, 14–20 kg K.',
    nutrients.search_text = 'straw nutrients | 5–8 kg N | 1.6–2.7 kg P | 14–20 kg K'
MERGE (treat)-[:PRESERVES {source_id:'chunk-ch4-002'}]->(nutrients)

MERGE (loss:Concept:Searchable {
  entity_id:  'Nutrient Loss from Straw Burning - Ch4',
  entity_type:'concept',
  name:       'Nutrient Loss from Burning'
})
SET loss.chapter     = 'Ch4',
    loss.source_id   = 'chunk-ch4-002',
    loss.description = 'Burning causes ~100% N loss, ~25% P loss, ~20% K loss.',
    loss.search_text = 'burning loss | 100% N | 25% P | 20% K'
MERGE (burn_straw)-[:CAUSES {source_id:'chunk-ch4-002'}]->(loss)

// --- Environmental impact (methane) ---
WITH treat, bio, flooded_cond
MERGE (methane:Emission:Searchable {
  entity_id:  'Methane Emissions - Ch4',
  entity_type:'emission',
  name:       'Methane Emissions (CH₄)'
})
SET methane.chapter     = 'Ch4',
    methane.source_id   = 'chunk-ch4-002',
    methane.description = 'Anaerobic breakdown in flooded fields generates CH₄, a potent greenhouse gas.',
    methane.search_text = 'methane | CH4 | anaerobic | greenhouse gas'
MERGE (flooded_cond)-[:RELEASES {source_id:'chunk-ch4-002'}]->(methane)
MERGE (bio)-[:REDUCES {source_id:'chunk-ch4-002'}]->(methane)

// --- Post-treatment benefits ---
WITH treat
MERGE (fertility:Benefit:Searchable {
  entity_id:  'Soil Fertility Enhancement - Ch4',
  entity_type:'benefit',
  name:       'Soil Fertility Enhancement'
})
SET fertility.chapter     = 'Ch4',
    fertility.source_id   = 'chunk-ch4-002',
    fertility.description = 'Dry-field aerobic decomposition retains nutrients and improves soil structure and long-term productivity.',
    fertility.search_text = 'soil fertility | structure | productivity'
MERGE (treat)-[:ACHIEVES {source_id:'chunk-ch4-002'}]->(fertility)

MERGE (recycling:Benefit:Searchable {
  entity_id:  'Nutrient Recycling - Ch4',
  entity_type:'benefit',
  name:       'Nutrient Recycling'
})
SET recycling.chapter     = 'Ch4',
    recycling.source_id   = 'chunk-ch4-002',
    recycling.description = 'Recycles N, P, K back into the soil via controlled decomposition.',
    recycling.search_text = 'nutrient recycling | N | P | K | decomposition'
MERGE (treat)-[:ACHIEVES {source_id:'chunk-ch4-002'}]->(recycling)

MERGE (climate:Benefit:Searchable {
  entity_id:  'GHG Reduction - Ch4',
  entity_type:'benefit',
  name:       'GHG Reduction'
})
SET climate.chapter     = 'Ch4',
    climate.source_id   = 'chunk-ch4-002',
    climate.description = 'Avoiding flooding/burning and using biological decomposition reduces greenhouse gas emissions.',
    climate.search_text = 'GHG reduction | avoid flooding | avoid burning | biological decomposition'
MERGE (treat)-[:ACHIEVES {source_id:'chunk-ch4-002'}]->(climate)
"""
