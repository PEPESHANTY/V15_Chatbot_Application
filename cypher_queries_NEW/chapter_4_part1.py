cypher = """
// =======================================
// Chapter 4 (Part 1) — Straw Collection & Circular Management
// Single-statement upsert with :Searchable and search_text
// =======================================

// --- Chapter 4 central node ---
MERGE (ch4:Chapter {entity_id:'Straw Management - Ch4'})
SET ch4:Searchable,
    ch4.entity_type = 'chapter',
    ch4.name        = 'Straw Management — Chapter 4',
    ch4.chapter     = 'Ch4',
    ch4.file_path   = 'book_1.pdf',
    ch4.source_id   = 'chunk-ch4-001',
    ch4.description = 'Chapter 4 focuses on circular straw management to minimize emissions, improve soil health, and utilize rice straw via mulching, composting, mushroom cultivation, feed, bioenergy, silicate, bioplastics, paper, and handicrafts.',
    ch4.created_at  = coalesce(ch4.created_at, timestamp()),
    ch4.search_text = 'straw management | circular | low emission | avoid burning | avoid flooded burial | collect within 5 days | mushroom | feed | compost | bioenergy | SRP'

// --- Part 1 main practice: Straw Collection ---
MERGE (collect:Practice:Searchable {
  entity_id:  'Straw Collection - Ch4',
  entity_type:'practice',
  name:       'Straw Collection'
})
SET collect.chapter     = 'Ch4',
    collect.source_id   = 'chunk-ch4-001',
    collect.description = 'Collect straw promptly after harvest (≤5 days; immediate in wet fields) to preserve nutritional quality and reduce methane emissions.',
    collect.search_text = 'straw collection | ≤5 days | immediate in wet fields | protein preservation | methane reduction | raking | baling'
MERGE (ch4)-[:COVERS {source_id:'chunk-ch4-001'}]->(collect)

// --- Circular management principle + policy alignment ---
WITH ch4, collect
MERGE (circular:Concept:Searchable {
  entity_id:  'Circular Straw Management - Ch4',
  entity_type:'concept',
  name:       'Circular Straw Management'
})
SET circular.chapter     = 'Ch4',
    circular.source_id   = 'chunk-ch4-001',
    circular.description = 'Discourage burning and flooded-field burial; promote collection and reuse of straw for mushroom cultivation, livestock feed, organic fertilizer, mulch, bioenergy, silicate, bioplastics, paper, and handicrafts.',
    circular.search_text = 'circular straw | reuse | mushroom | feed | compost | mulch | bioenergy | silicate | bioplastics | paper | handicrafts | low emission'
MERGE (collect)-[:ALIGNS_WITH {source_id:'chunk-ch4-001'}]->(circular)

MERGE (burning:Threat:Searchable {
  entity_id:  'Straw Burning - Ch4',
  entity_type:'threat',
  name:       'Straw Burning'
})
SET burning.chapter     = 'Ch4',
    burning.source_id   = 'chunk-ch4-001',
    burning.description = 'Burning causes air pollution, nutrient loss, and biodiversity degradation.',
    burning.search_text = 'burning | air pollution | nutrient loss | biodiversity loss'
MERGE (circular)-[:AVOIDS {source_id:'chunk-ch4-001'}]->(burning)

MERGE (burial:Threat:Searchable {
  entity_id:  'Flooded Straw Burial - Ch4',
  entity_type:'threat',
  name:       'Flooded Straw Burial'
})
SET burial.chapter     = 'Ch4',
    burial.source_id   = 'chunk-ch4-001',
    burial.description = 'Flooded burial releases methane (CH₄) due to anaerobic decomposition.',
    burial.search_text = 'flooded burial | methane | anaerobic decomposition'
MERGE (circular)-[:AVOIDS {source_id:'chunk-ch4-001'}]->(burial)

MERGE (srp:Standard:Searchable {
  entity_id:  'Sustainable Rice Platform Goals - Ch4',
  entity_type:'standard',
  name:       'SRP Goals'
})
SET srp.chapter     = 'Ch4',
    srp.source_id   = 'chunk-ch4-001',
    srp.description = 'Low-emission, resource-efficient guidelines aligned with circular straw reuse and regenerative practices.',
    srp.search_text = 'SRP | sustainable rice | low emission | resource efficiency'
MERGE (circular)-[:SUPPORTS {source_id:'chunk-ch4-001'}]->(srp)

MERGE (reg:Document:Searchable {
  entity_id:  'Decision 248/QĐ-TT-VPPN (Jul 2023)',
  entity_type:'document',
  name:       'Circular Straw Management Procedure — Decision 248/QĐ-TT-VPPN (Jul 2023)'
})
SET reg.chapter     = 'Ch4',
    reg.source_id   = 'chunk-ch4-001',
    reg.description = 'Official Vietnamese procedure for circular, low-emission straw management in the Mekong Delta.',
    reg.search_text = 'Decision 248/QĐ-TT-VPPN | circular straw | low emission | Mekong Delta'
MERGE (circular)-[:GUIDED_BY {source_id:'chunk-ch4-001'}]->(reg)

// --- Collection timing parameter ---
WITH ch4, collect, circular
MERGE (timing:Parameter:Searchable {
  entity_id:  'Straw Collection Timing - Ch4',
  entity_type:'parameter',
  name:       'Straw Collection Timing'
})
SET timing.chapter     = 'Ch4',
    timing.source_id   = 'chunk-ch4-001',
    timing.description = 'Collect within 5 days post-harvest to preserve protein and prevent microbial degradation; immediate in wet fields.',
    timing.search_text = 'timing | ≤5 days | immediate in wet fields | protein | microbial degradation'
MERGE (collect)-[:REQUIRES {source_id:'chunk-ch4-001'}]->(timing)

// --- Machinery types ---
WITH ch4, collect, circular
MERGE (tractor_baler:Equipment:Searchable {
  entity_id:  'Tractor-Mounted Baler - Ch4',
  entity_type:'equipment',
  name:       'Tractor-Mounted Baler'
})
SET tractor_baler.chapter     = 'Ch4',
    tractor_baler.source_id   = 'chunk-ch4-001',
    tractor_baler.description = 'Requires ≥25 HP tractor; effective only in dry fields; lacks onboard storage and needs extra vehicle for transport.',
    tractor_baler.search_text = 'tractor-mounted baler | ≥25 HP | dry fields only | no onboard storage'
MERGE (collect)-[:USES {source_id:'chunk-ch4-001'}]->(tractor_baler)

MERGE (self_baler:Equipment:Searchable {
  entity_id:  'Self-Propelled Baler - Ch4',
  entity_type:'equipment',
  name:       'Self-Propelled Baler'
})
SET self_baler.chapter     = 'Ch4',
    self_baler.source_id   = 'chunk-ch4-001',
    self_baler.description = '≥70 HP; onboard storage (~50 bales); crawler tracks for wet conditions; output ~70–150 bales/hour.',
    self_baler.search_text = 'self-propelled baler | ≥70 HP | onboard storage 50 bales | crawlers | wet fields | 70–150 bales/hour'
MERGE (collect)-[:USES {source_id:'chunk-ch4-001'}]->(self_baler)

// --- Features & performance params ---
WITH ch4, collect, circular, tractor_baler, self_baler
MERGE (crawler:Feature:Searchable {
  entity_id:  'Rubber Crawlers - Ch4',
  entity_type:'feature',
  name:       'Rubber Crawlers'
})
SET crawler.chapter     = 'Ch4',
    crawler.source_id   = 'chunk-ch4-001',
    crawler.description = 'Crawler tracks enable operation in wet, muddy fields without getting stuck.',
    crawler.search_text = 'rubber crawlers | wet fields | traction'
MERGE (self_baler)-[:FEATURES {source_id:'chunk-ch4-001'}]->(crawler)

MERGE (bale_output:Parameter:Searchable {
  entity_id:  'Baling Output - Ch4',
  entity_type:'parameter',
  name:       'Baling Output / Size / Weight'
})
SET bale_output.chapter     = 'Ch4',
    bale_output.source_id   = 'chunk-ch4-001',
    bale_output.description = 'Output ~70–150 bales/hour; bale size 50×70 cm; weight 12–18 kg (dry), 20–30 kg (wet).',
    bale_output.search_text = 'output 70–150 bales/hour | bale 50×70 cm | 12–18 kg dry | 20–30 kg wet'
MERGE (self_baler)-[:DELIVERS {source_id:'chunk-ch4-001'}]->(bale_output)

// --- Field condition logic ---
WITH ch4, collect, circular, tractor_baler, self_baler
MERGE (wet_fields:Condition:Searchable {
  entity_id:  'Wet Field Straw Collection - Ch4',
  entity_type:'condition',
  name:       'Wet Field Collection'
})
SET wet_fields.chapter     = 'Ch4',
    wet_fields.source_id   = 'chunk-ch4-001',
    wet_fields.description = 'Immediate collection after harvest; self-propelled baler preferred; tractor-mounted baler not recommended.',
    wet_fields.search_text = 'wet fields | immediate collection | self-propelled baler preferred | tractor-mounted not recommended'
MERGE (collect)-[:TAILORED_TO {source_id:'chunk-ch4-001'}]->(wet_fields)
MERGE (self_baler)-[:PREFERRED_IN {source_id:'chunk-ch4-001'}]->(wet_fields)

MERGE (dry_fields:Condition:Searchable {
  entity_id:  'Dry Field Straw Collection - Ch4',
  entity_type:'condition',
  name:       'Dry Field Collection'
})
SET dry_fields.chapter     = 'Ch4',
    dry_fields.source_id   = 'chunk-ch4-001',
    dry_fields.description = 'Straw may remain ≤5 days; both baler types possible; self-propelled is more efficient.',
    dry_fields.search_text = 'dry fields | ≤5 days | tractor-mounted or self-propelled | efficiency'
MERGE (collect)-[:TAILORED_TO {source_id:'chunk-ch4-001'}]->(dry_fields)
MERGE (tractor_baler)-[:SUITABLE_IN {source_id:'chunk-ch4-001'}]->(dry_fields)
MERGE (self_baler)-[:SUITABLE_IN {source_id:'chunk-ch4-001'}]->(dry_fields)

// --- Raking machine & manual fallback ---
WITH ch4, collect, circular
MERGE (rake:Equipment:Searchable {
  entity_id:  'Raking Machine - Ch4',
  entity_type:'equipment',
  name:       'Raking Machine'
})
SET rake.chapter     = 'Ch4',
    rake.source_id   = 'chunk-ch4-001',
    rake.description = 'Used before baling to aerate and gather straw, improving drying and baling efficiency.',
    rake.search_text = 'raking | aeration | gather straw | improve drying | efficiency'
MERGE (collect)-[:PRECEDED_BY {source_id:'chunk-ch4-001'}]->(rake)

MERGE (manual:Method:Searchable {
  entity_id:  'Manual Straw Collection - Ch4',
  entity_type:'method',
  name:       'Manual Straw Collection'
})
SET manual.chapter     = 'Ch4',
    manual.source_id   = 'chunk-ch4-001',
    manual.description = 'Labor-intensive fallback for areas without access to mechanized baling.',
    manual.search_text = 'manual | fallback | no baler | labor intensive'
MERGE (collect)-[:ALTERNATIVE_METHOD {source_id:'chunk-ch4-001'}]->(manual)

// --- Circular reuse use-cases ---
WITH ch4, collect, circular
UNWIND [
  ['Mushroom Cultivation', 'Straw reused as substrate for mushroom production.'],
  ['Cattle Feed',          'Straw used for ruminant feed; quality preserved via prompt collection.'],
  ['Organic Fertilizer',   'Straw composted with microbial inoculants (e.g., Trichoderma) to enrich soil organic matter.'],
  ['Mulching',             'Straw used as field/garden mulch to retain moisture and suppress weeds.'],
  ['Bioenergy',            'Straw as feedstock for energy/fuel/heat applications.'],
  ['Silicate Recovery',    'Straw ash as a silicate source for materials/soil amendments.'],
  ['Bioplastics',          'Straw-derived biomass used in producing bio-based plastics.'],
  ['Paper & Handicrafts',  'Straw used for paper pulp and traditional handicrafts.']
] AS uc
MERGE (u:UseCase:Searchable {
  entity_id:  uc[0],
  entity_type:'usecase',
  name:       uc[0]
})
SET u.chapter     = 'Ch4',
    u.source_id   = 'chunk-ch4-001',
    u.description = uc[1],
    u.search_text = uc[0] + ' | straw reuse | circular economy'
MERGE (circular)-[:PROMOTES {source_id:'chunk-ch4-001'}]->(u)
MERGE (collect)-[:REUSED_AS {source_id:'chunk-ch4-001'}]->(u)
"""
