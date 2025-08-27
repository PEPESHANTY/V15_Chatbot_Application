cypher = """
// =======================================
// Chapter 2 (Part 4) — Water Management (AWD)
// Single-statement, idempotent upsert with :Searchable + search_text
// =======================================

// Ensure Chapter 2 node exists
MERGE (ch2:Chapter {entity_id:'Cultivation Techniques - Ch2'})
SET ch2:Searchable,
    ch2.entity_type = coalesce(ch2.entity_type, 'chapter'),
    ch2.chapter     = 'Ch2',
    ch2.file_path   = coalesce(ch2.file_path, 'book_1.pdf')

// --- Water Management Parent Node ---
MERGE (wm:Practice:Searchable {
  entity_id:  'Water Management - AWD',
  entity_type:'practice',
  name:       'Water Management (AWD)'
})
SET wm.chapter     = 'Ch2',
    wm.source_id   = 'chunk-ch2-004',
    wm.description = 'Alternate Wetting and Drying (AWD) conserves water and reduces methane by irrigating on need (trigger-based) rather than continuous flooding.',
    wm.search_text = 'water management | AWD | alternate wetting and drying | irrigation scheduling | methane reduction | water saving | Mekong Delta'
MERGE (ch2)-[:COVERS {source_id:'chunk-ch2-004'}]->(wm)

// --- Technique: Alternate Wetting and Drying ---
MERGE (awd:Technique:Searchable {
  entity_id:  'Alternate Wetting and Drying',
  entity_type:'method',
  name:       'Alternate Wetting and Drying (AWD)'
})
SET awd.chapter     = 'Ch2',
    awd.source_id   = 'chunk-ch2-004',
    awd.description = 'Irrigate only when the water table drops ~15 cm below soil surface; then re-flood shallowly. Cuts methane, saves water, and keeps roots oxygenated.',
    awd.search_text = 'AWD | 15 cm trigger | re-flood 3–5 cm | oxygenation | anaerobic avoidance | methane | water-use efficiency'
MERGE (wm)-[:USES {source_id:'chunk-ch2-004'}]->(awd)

// --- Pre-Sowing Water Management Rule ---
MERGE (presow:Guideline:Searchable {
  entity_id:  'No Flooding > 30 Days',
  entity_type:'guideline',
  name:       'Avoid Continuous Flooding > 30 Days'
})
SET presow.chapter     = 'Ch2',
    presow.source_id   = 'chunk-ch2-004',
    presow.description = 'Before sowing, avoid keeping fields flooded for >30 days to limit anaerobic conditions and methane build-up.',
    presow.search_text = 'pre-sowing rule | avoid >30 days flooding | methane | anaerobic | field preparation'
MERGE (wm)-[:REQUIRES {source_id:'chunk-ch2-004'}]->(presow)

// --- Observation Indicator ---
MERGE (obs:Tool:Searchable {
  entity_id:  'AWD Monitoring Pipe',
  entity_type:'tool',
  name:       'AWD Monitoring Pipe'
})
SET obs.chapter     = 'Ch2',
    obs.source_id   = 'chunk-ch2-004',
    obs.description = 'Perforated tube (≈10–15 cm) inserted into soil to read water depth and time AWD irrigation.',
    obs.search_text = 'monitoring pipe | perforated tube | 10–15 cm | water level | irrigation timing | field water table'
MERGE (awd)-[:MONITORED_BY {source_id:'chunk-ch2-004'}]->(obs)

// --- AWD Irrigation Trigger Condition ---
MERGE (trigger:Condition:Searchable {
  entity_id:  'Irrigation Trigger - 15cm Dry Depth',
  entity_type:'condition',
  name:       'Irrigation Trigger (15 cm below surface)'
})
SET trigger.chapter     = 'Ch2',
    trigger.source_id   = 'chunk-ch2-004',
    trigger.description = 'Re-apply water when water table falls ~15 cm below soil surface or when “nứt chân chim” surface cracks appear.',
    trigger.search_text = 'trigger | 15 cm below surface | water table | surface cracks | nứt chân chim | re-irrigate'
MERGE (awd)-[:TRIGGERED_BY {source_id:'chunk-ch2-004'}]->(trigger)

// --- AWD Re-flooding Rule ---
MERGE (reflood:Guideline:Searchable {
  entity_id:  'Re-flooding Limit - 5cm',
  entity_type:'guideline',
  name:       'Re-flooding Limit (≤5 cm)'
})
SET reflood.chapter     = 'Ch2',
    reflood.source_id   = 'chunk-ch2-004',
    reflood.description = 'Under AWD, refill to only ~3–5 cm standing water to avoid prolonged anaerobic conditions.',
    reflood.search_text = 'reflooding | re-irrigation depth | 3–5 cm | AWD refill | anaerobic avoidance'
MERGE (awd)-[:FOLLOWS {source_id:'chunk-ch2-004'}]->(reflood)

// --- AWD Schedule Stages ---
WITH awd
UNWIND [
  {id:'AWD Phase - Day 1–7', name:'Day 1–7', desc:'Keep field moist to promote healthy germination; avoid deep flooding.'},
  {id:'AWD Phase - Day 12–22', name:'Day 12–22', desc:'Drain to oxygenate root zone and stimulate deeper rooting.'},
  {id:'AWD Phase - Day 28–40', name:'Day 28–40', desc:'Second drying cycle; critical for root strength and methane reduction.'},
  {id:'AWD Phase - 7–15 Days Before Harvest', name:'7–15 Days Before Harvest', desc:'Final drying improves grain ripening and supports easier harvesting.'}
] AS phase
MERGE (p:Stage:Searchable {
  entity_id:  phase.id,
  entity_type:'stage',
  name:       phase.name
})
SET p.chapter     = 'Ch2',
    p.source_id   = 'chunk-ch2-004',
    p.description = phase.desc,
    p.search_text = 'AWD stage | '+phase.name+' | '+phase.desc
MERGE (awd)-[:INCLUDES {source_id:'chunk-ch2-004'}]->(p)

// --- Optional Mid-Season Application ---
WITH awd
MERGE (optional:Option:Searchable {
  entity_id:  'Mid-Season AWD (Optional)',
  entity_type:'option',
  name:       'Mid-Season AWD (Optional)'
})
SET optional.chapter     = 'Ch2',
    optional.source_id   = 'chunk-ch2-004',
    optional.description = 'Apply AWD once between days 28–40 when conditions allow to cut emissions without stressing the crop.',
    optional.search_text = 'optional AWD | mid-season | day 28–40 | single cycle | emission reduction'
MERGE (awd)-[:OPTIONAL_STAGE {source_id:'chunk-ch2-004'}]->(optional)

// --- AWD Benefits ---
WITH awd
UNWIND [
  {id:'Water-Use Efficiency', desc:'Reduces water consumption by irrigating only when needed (trigger-based).'},
  {id:'Methane Reduction',    desc:'Limits anaerobic conditions, reducing methane emissions from paddy fields.'},
  {id:'Nutrient Retention',   desc:'Minimizes nutrient runoff and nitrogen loss by controlling water levels.'},
  {id:'Stronger Root Systems',desc:'Drying cycles encourage deeper, stronger roots, improving resilience.'},
  {id:'Improved Grain Quality',desc:'Final drying improves ripening and harvest efficiency/cleanliness.'}
] AS benefit
MERGE (b:Benefit:Searchable {
  entity_id:  benefit.id,
  entity_type:'benefit',
  name:       benefit.id
})
SET b.chapter     = 'Ch2',
    b.source_id   = 'chunk-ch2-004',
    b.description = benefit.desc,
    b.search_text = benefit.id+' | '+benefit.desc+' | AWD benefit | water | methane | quality | roots'
MERGE (awd)-[:ACHIEVES {source_id:'chunk-ch2-004'}]->(b)

// --- Helpful cross-link to GHG concept ---
WITH awd
MERGE (ghg:Concept:Searchable {
  entity_id:  'Greenhouse Gas Emissions',
  entity_type:'concept',
  name:       'Greenhouse Gas Emissions'
})
SET ghg.description = coalesce(ghg.description, 'Methane and related GHGs emitted by flooded paddy systems.'),
    ghg.search_text = coalesce(ghg.search_text, 'GHG | methane | paddy emissions | AWD reduction')
MERGE (awd)-[:REDUCES {source_id:'chunk-ch2-004'}]->(ghg)
"""
