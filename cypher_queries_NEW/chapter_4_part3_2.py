cypher = """
// =======================================================
// Chapter 4 — Part 3.2: Straw Mushroom Cultivation (single statement)
// =======================================================

MERGE (mushroom:Practice:Searchable {
  entity_id:  'Straw Mushroom Cultivation - Ch4',
  entity_type:'practice',
  name:       'Straw Mushroom Cultivation'
})
SET mushroom.chapter     = 'Ch4',
    mushroom.source_id   = 'chunk-ch4-003',
    mushroom.description = 'Low-cost outdoor and indoor cultivation of straw mushrooms using clean rice straw and composted substrate with fungal spawn. Supports circular agriculture and income diversification.',
    mushroom.search_text = 'straw mushroom | nấm rơm | outdoor | indoor | rice straw | compost | spawn | circular agriculture | income diversification'

WITH mushroom
MATCH (ch4:Chapter {entity_id:'Straw Management - Ch4'})
MERGE (ch4)-[:COVERS {source_id:'chunk-ch4-003'}]->(mushroom)

// --- Subtypes: Outdoor & Indoor
WITH mushroom
UNWIND [
  ['Outdoor Straw Mushroom Cultivation - Ch4',
   'Outdoor cultivation using lime-treated straw soaked in CaO solution, fermented on bamboo racks under tarp, with daily watering and two harvest flushes.'],
  ['Indoor Straw Mushroom Cultivation - Ch4',
   'Indoor tiered-rack cultivation with sanitized straw, temperature-humidity control, 12h light during fruiting, and nutrient additives for optimized yield.']
] AS type
MERGE (sub:Method:Searchable {
  entity_id:  type[0],
  entity_type:'method',
  name:       type[0]
})
SET sub.chapter     = 'Ch4',
    sub.source_id   = 'chunk-ch4-003',
    sub.description = type[1],
    sub.search_text = type[0] + ' | ' + type[1]
MERGE (mushroom)-[:USES_METHOD {source_id:'chunk-ch4-003'}]->(sub)

// --- Shared inputs
WITH mushroom
MERGE (straw:Input:Searchable {
  entity_id:  'Clean Rice Straw - Ch4',
  entity_type:'input',
  name:       'Clean Rice Straw'
})
SET straw.chapter     = 'Ch4',
    straw.source_id   = 'chunk-ch4-003',
    straw.description = 'Disease-free, pesticide-free straw in bundles or rolls; soaked in lime and composted before inoculation.',
    straw.search_text = 'clean straw | pesticide-free | bundles | rolls | lime soak | composted'
MERGE (spawn:Input:Searchable {
  entity_id:  'Mushroom Spawn - Ch4',
  entity_type:'input',
  name:       'Mushroom Spawn'
})
SET spawn.chapter     = 'Ch4',
    spawn.source_id   = 'chunk-ch4-003',
    spawn.description = 'High-quality straw-based mycelium; may be enriched with cow dung, worm compost, banana stem powder, or HVP/HQ.',
    spawn.search_text = 'spawn | mycelium | cow dung | worm compost | banana stem | HVP | HQ'
MERGE (mushroom)-[:USES {source_id:'chunk-ch4-003'}]->(straw)
MERGE (mushroom)-[:USES {source_id:'chunk-ch4-003'}]->(spawn)

// --- Outdoor cultivation steps
WITH mushroom
UNWIND [
  ['Site Preparation - Outdoor - Ch4', 'Flat, moist, shaded site (paddy/raised beds); lime treat soil at 5 kg CaCO3 / 100 m².'],
  ['Straw Soaking - Outdoor - Ch4', 'Soak straw 5–10 min in 5 kg CaO / 1 m³ water; drain to reach pH 13–14.'],
  ['Composting - Outdoor - Ch4', 'Pile on bamboo frames ~10–20 cm high, cover with tarp; turn on days 7 & 17; maintain ~70°C core.'],
  ['Bed Formation - Outdoor - Ch4', 'Form 35 cm wide, 35–40 cm tall beds; per bed use ~4 kg straw + 160 g spawn + 1–2 kg top straw.'],
  ['Moisture Management - Outdoor - Ch4', 'Cover with mesh + straw; water daily ~16:00; ventilate with tarp during rain.'],
  ['Fruiting & Harvesting - Outdoor - Ch4', 'Pinheads day 9–10; harvest twice daily from day 12; two flushes ~5-day interval.'],
  ['Spent Straw Compost - Outdoor - Ch4', 'After harvest, spent substrate is composted as organic matter for reuse.']
] AS step
MERGE (s:Step:Searchable {
  entity_id:  step[0],
  entity_type:'step',
  name:       step[0]
})
SET s.chapter     = 'Ch4',
    s.source_id   = 'chunk-ch4-003',
    s.description = step[1],
    s.search_text = step[0] + ' | ' + step[1]
MERGE (mushroom)-[:HAS_STEP {source_id:'chunk-ch4-003'}]->(s)

// --- Indoor cultivation steps
WITH mushroom
UNWIND [
  ['Infrastructure Setup - Indoor - Ch4', 'Ventilated house with racks (2–4 tiers, 0.5 m apart), netted walls, tarp/roof, dry soil or concrete base.'],
  ['Straw Soaking - Indoor - Ch4', 'Soak straw 5–10 min in 5 kg CaO + 1 kg superphosphate + 0.5 kg KCl per 1 m³ water; drain well.'],
  ['Composting & Turning - Indoor - Ch4', 'Pile soaked straw, cover with tarp; turn on days 7 & 17; maintain ~70°C; adjust moisture.'],
  ['Spawn Enrichment - Indoor - Ch4', 'Mix spawn with cow dung, worm compost, HVP/HQ; finely chop and distribute uniformly.'],
  ['Rack Setup & Inoculation - Indoor - Ch4', 'Distribute straw on racks; apply ~200 g spawn/m²; incubate 3 days; add 2 kg/m² worm compost.'],
  ['Fruiting Management - Indoor - Ch4', 'RH 50–70% then 80–100%; temp 25–30°C at fruiting; mist if dry; expose to ~12 h light.'],
  ['Sodium Acetate Spray - Indoor - Ch4', 'Spray 0.05% sodium acetate (~1 L/m²) to stimulate synchronized fruiting.'],
  ['Harvesting - Indoor - Ch4', 'Harvest from ~day 12, twice daily; flush 1 ~4 days; flush 2 after 3–5 days; convert spent straw to compost.']
] AS indoor_step
MERGE (i:Step:Searchable {
  entity_id:  indoor_step[0],
  entity_type:'step',
  name:       indoor_step[0]
})
SET i.chapter     = 'Ch4',
    i.source_id   = 'chunk-ch4-003',
    i.description = indoor_step[1],
    i.search_text = indoor_step[0] + ' | ' + indoor_step[1]
MERGE (mushroom)-[:HAS_STEP {source_id:'chunk-ch4-003'}]->(i)

// --- Compost output
WITH mushroom
MERGE (compost:Output:Searchable {
  entity_id:  'Organic Compost from Spent Straw - Ch4',
  entity_type:'output',
  name:       'Organic Compost from Spent Straw'
})
SET compost.chapter     = 'Ch4',
    compost.source_id   = 'chunk-ch4-003',
    compost.description = 'After harvesting, spent straw is recycled as organic compost (giá thể hữu cơ rơm) to enhance soil health.',
    compost.search_text = 'compost | spent straw | organic matter | soil health | circular reuse'
MERGE (mushroom)-[:PRODUCES {source_id:'chunk-ch4-003'}]->(compost)
"""
