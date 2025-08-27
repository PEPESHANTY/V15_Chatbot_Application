cypher = """
// =======================================================
// Chapter 4 — Part 3.3: Fermented Straw Feed for Cattle
// =======================================================

MERGE (feed:Practice:Searchable {
  entity_id:  'Fermented Straw Feed for Cattle - Ch4',
  entity_type:'practice',
  name:       'Fermented Straw Feed for Cattle'
})
SET feed.chapter     = 'Ch4',
    feed.source_id   = 'chunk-ch4-003',
    feed.description = 'Fermenting rice straw to produce nutritious, low-cost feed for buffaloes and cows. Enhances digestibility, prevents waste, and supports circular livestock farming.',
    feed.search_text = 'straw feed | fermented straw | buffalo | cow | cattle | lime-urea | enzyme-salt | nylon bag | pit fermentation | GAP straw | circular livestock'

WITH feed
MATCH (ch4:Chapter {entity_id:'Straw Management - Ch4'})
MERGE (ch4)-[:COVERS {source_id:'chunk-ch4-003'}]->(feed)

// --- Input: GAP-compliant straw
WITH feed
MERGE (input:Input:Searchable {
  entity_id:  'GAP-Compliant Rice Straw - Ch4',
  entity_type:'input',
  name:       'GAP-Compliant Rice Straw'
})
SET input.chapter     = 'Ch4',
    input.source_id   = 'chunk-ch4-003',
    input.description = 'Rice straw sourced from Good Agricultural Practice (GAP) fields, free from pesticide residues and harmful microbes.',
    input.search_text = 'GAP straw | clean straw | pesticide-free | microbial safe | source hygiene'
MERGE (feed)-[:REQUIRES {source_id:'chunk-ch4-003'}]->(input)

// --- Conditions: dry vs wet straw
WITH feed
UNWIND [
  ['Dry Straw - Ch4', 'Dry Straw', 'condition', 'Moisture <18%. Can be stored up to ~6 months before processing.'],
  ['Wet Straw - Ch4', 'Wet Straw', 'condition', 'Moisture >18%. Must be fermented immediately to avoid spoilage.']
] AS type
MERGE (cond:Condition:Searchable {
  entity_id:  type[0],
  entity_type:type[2],
  name:       type[1]
})
SET cond.chapter     = 'Ch4',
    cond.source_id   = 'chunk-ch4-003',
    cond.description = type[3],
    cond.search_text = type[1] + ' | ' + type[3]
MERGE (feed)-[:USES {source_id:'chunk-ch4-003'}]->(cond)

// --- Treatments: lime-urea or enzyme-salt
WITH feed
UNWIND [
  ['Lime-Urea Treatment - Ch4', 'Lime-Urea Treatment', '2 kg powdered lime + 2 kg urea mixed with 50–80 L water per 100 kg straw.'],
  ['Enzyme-Salt Treatment - Ch4', 'Enzyme-Salt Treatment', '0.1 kg microbial enzyme + 0.1 kg salt mixed with 50–80 L water per 100 kg straw.']
] AS method
MERGE (treat:Method:Searchable {
  entity_id:  method[0],
  entity_type:'method',
  name:       method[1]
})
SET treat.chapter     = 'Ch4',
    treat.source_id   = 'chunk-ch4-003',
    treat.description = method[2],
    treat.search_text = method[1] + ' | ' + method[2]
MERGE (feed)-[:TREATED_WITH {source_id:'chunk-ch4-003'}]->(treat)

// --- Fermentation steps: nylon bag or pit
WITH feed
UNWIND [
  ['Nylon Bag Fermentation - Ch4', 'Nylon Bag Fermentation', 'Tightly sealed 16–20 kg straw bags, anaerobically fermented for ~7 days.'],
  ['Pit Fermentation - Ch4', 'Pit Fermentation', 'Straw compacted in pits and fermented anaerobically; ensure airtight conditions.']
] AS ferment
MERGE (step:Step:Searchable {
  entity_id:  ferment[0],
  entity_type:'step',
  name:       ferment[1]
})
SET step.chapter     = 'Ch4',
    step.source_id   = 'chunk-ch4-003',
    step.description = ferment[2],
    step.search_text = ferment[1] + ' | ' + ferment[2]
MERGE (feed)-[:INCLUDES {source_id:'chunk-ch4-003'}]->(step)

// --- Quality control guideline
WITH feed
MERGE (safe:Guideline:Searchable {
  entity_id:  'Fermentation Quality Control - Ch4',
  entity_type:'guideline',
  name:       'Fermentation Quality Control'
})
SET safe.chapter     = 'Ch4',
    safe.source_id   = 'chunk-ch4-003',
    safe.description = 'Avoid contamination and mold by ensuring correct moisture (per method) and truly airtight sealing throughout fermentation.',
    safe.search_text = 'quality control | airtight sealing | moisture control | contamination | mold'
MERGE (feed)-[:FOLLOWS {source_id:'chunk-ch4-003'}]->(safe)

// --- Feeding parameter
WITH feed
MERGE (intake:Parameter:Searchable {
  entity_id:  'Daily Intake for Cattle - Ch4',
  entity_type:'parameter',
  name:       'Daily Intake for Cattle'
})
SET intake.chapter     = 'Ch4',
    intake.source_id   = 'chunk-ch4-003',
    intake.description = 'Each buffalo or cow can consume ~2–7 kg of fermented straw per day depending on age and weight.',
    intake.search_text = 'intake | 2–7 kg/day | buffalo | cow | body weight | age'
MERGE (feed)-[:RECOMMENDS {source_id:'chunk-ch4-003'}]->(intake)

// --- Benefit
WITH feed
MERGE (value:Benefit:Searchable {
  entity_id:  'Circular Livestock Feed Value - Ch4',
  entity_type:'benefit',
  name:       'Circular Livestock Feed Value'
})
SET value.chapter     = 'Ch4',
    value.source_id   = 'chunk-ch4-003',
    value.description = 'Transforms agricultural straw into value-added livestock feed, reducing costs and enhancing farm circularity and sustainability.',
    value.search_text = 'circular livestock | value-added feed | cost reduction | sustainability'
MERGE (feed)-[:ACHIEVES {source_id:'chunk-ch4-003'}]->(value)
"""
