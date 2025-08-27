cypher = """
// =======================================================
// Chapter 4 – Part 3.5: Organic Fertilizer from Rice Straw
// =======================================================

// Root practice
MERGE (fert:Practice:Searchable {
  entity_id:  'Organic Fertilizer from Rice Straw - Ch4',
  entity_type:'practice',
  name:       'Organic Fertilizer from Rice Straw'
})
SET fert.chapter     = 'Ch4',
    fert.source_id   = 'chunk-ch4-003',
    fert.description = 'Mechanized composting of rice straw with manure and microbial inoculants under regulated temperature, moisture, and pH to produce high-quality organic fertilizer.',
    fert.search_text = 'organic fertilizer | rice straw compost | composting | manure | microbial inoculant | C:N 25–30 | 50–70°C | moisture 50–60% | pH 6.5–7 | maturation 30–45 days'
WITH fert

// Link to Chapter 4
MATCH (ch4:Chapter {entity_id:'Straw Management - Ch4'})
MERGE (ch4)-[:COVERS {source_id:'chunk-ch4-003'}]->(fert)
WITH fert

// Core Inputs
UNWIND [
  ['Rice Straw - Composting - Ch4',           'Base substrate with ~14–60% moisture; layered with manure/soil or urea to balance C:N.'],
  ['Livestock Manure - Ch4',                  'Dry cattle manure or enriched agricultural soil used to balance C:N ratio.'],
  ['Urea 46N - Ch4',                          'Alternative nitrogen source for semi-wet straw when manure is unavailable.'],
  ['Microbial Inoculants - Compost - Ch4',    'Biological agents added to accelerate decomposition and enhance microbial activity.'],
  ['Water - Compost - Ch4',                   'Maintains 50–60% moisture during fermentation; added via spray systems.'],
  ['Coconut Husk Fiber - Ch4',                'Optional bulking agent to improve porosity and air flow.'],
  ['Rice Husk Ash - Ch4',                     'Optional additive to retain nutrients and regulate bulk density.']
] AS mat
MERGE (input:Input:Searchable {
  entity_id:  mat[0],
  entity_type:'input',
  name:       mat[0]
})
SET input.chapter     = 'Ch4',
    input.source_id   = 'chunk-ch4-003',
    input.description = mat[1],
    input.search_text = 'compost input | ' + mat[0] + ' | ' + mat[1]
MERGE (fert)-[:REQUIRES {source_id:'chunk-ch4-003'}]->(input)
WITH fert

// Helpful Parameters
MERGE (cn:Parameter:Searchable {
  entity_id:  'Compost C:N Ratio 25–30 - Ch4',
  entity_type:'parameter',
  name:       'C:N 25–30'
})
SET cn.chapter     = 'Ch4',
    cn.source_id   = 'chunk-ch4-003',
    cn.description = 'Maintain compost carbon-to-nitrogen ratio between 25 and 30 for efficient decomposition.',
    cn.search_text = 'C:N ratio 25–30 | compost balance | efficient decomposition'
MERGE (fert)-[:TARGETS {source_id:'chunk-ch4-003'}]->(cn)

MERGE (trench:Parameter:Searchable {
  entity_id:  'Trench Dimensions 1.2m x 0.7m - Ch4',
  entity_type:'parameter',
  name:       'Trench 1.2m × 0.7m'
})
SET trench.chapter     = 'Ch4',
    trench.source_id   = 'chunk-ch4-003',
    trench.description = 'Layer materials in a trench ~1.2 m wide and 0.7 m high for aeration and microbial activity.',
    trench.search_text = 'compost trench | 1.2m width | 0.7m height | aeration'
MERGE (fert)-[:USES {source_id:'chunk-ch4-003'}]->(trench)
WITH fert

// Compost Preparation and Layering
MERGE (prep:Step:Searchable {
  entity_id:  'Compost Trench Layering - Ch4',
  entity_type:'step',
  name:       'Compost Trench Layering'
})
SET prep.chapter     = 'Ch4',
    prep.source_id   = 'chunk-ch4-003',
    prep.description = 'Alternate ~20 cm layers of straw and manure/soil in a ~1.2 m × 0.7 m trench. Maintain C:N 25–30. Use compost turner to mix and spray microbes at ~1.5 m/min.',
    prep.search_text = 'layering | 20 cm layers | straw + manure | turner 1.5 m/min | microbial spray'
MERGE (fert)-[:HAS_STEP {source_id:'chunk-ch4-003'}]->(prep)
WITH fert

// Fermentation Stage
MERGE (phase3:Step:Searchable {
  entity_id:  'Fermentation Conditions - Ch4',
  entity_type:'step',
  name:       'Fermentation Conditions'
})
SET phase3.chapter     = 'Ch4',
    phase3.source_id   = 'chunk-ch4-003',
    phase3.description = 'Cover with tarp; maintain 50–70°C, 50–60% moisture, and pH 6.5–7. Turn if temperature exceeds 70°C.',
    phase3.search_text = 'fermentation | 50–70°C | 50–60% moisture | pH 6.5–7 | tarp cover | turn if >70°C'
MERGE (fert)-[:HAS_STEP {source_id:'chunk-ch4-003'}]->(phase3)
WITH fert

// Aeration and Cooling Stage
MERGE (phase4:Step:Searchable {
  entity_id:  'Cooling and Aeration Phase - Ch4',
  entity_type:'step',
  name:       'Cooling and Aeration Phase'
})
SET phase4.chapter     = 'Ch4',
    phase4.source_id   = 'chunk-ch4-003',
    phase4.description = 'After ~10–15 days, turn again to lower temperature to 30–50°C. Adjust moisture to 40–50%. Optionally add 40% manure, 40% coconut husk fiber, 20% rice husk ash.',
    phase4.search_text = 'cooling | aeration | 30–50°C | moisture 40–50% | coconut husk | rice husk ash | 40:40:20'
MERGE (fert)-[:HAS_STEP {source_id:'chunk-ch4-003'}]->(phase4)
WITH fert

// Maturation Stage
MERGE (mature:Step:Searchable {
  entity_id:  'Final Maturation - Ch4',
  entity_type:'step',
  name:       'Final Maturation'
})
SET mature.chapter     = 'Ch4',
    mature.source_id   = 'chunk-ch4-003',
    mature.description = 'At ~30–45 days, compost stabilizes at 30–40% moisture; dark, crumbly, and sieved to remove coarse debris.',
    mature.search_text = 'maturation | 30–45 days | 30–40% moisture | dark crumbly compost | sieving'
MERGE (fert)-[:HAS_STEP {source_id:'chunk-ch4-003'}]->(mature)
WITH fert

// Equipment
MERGE (machine:Equipment:Searchable {
  entity_id:  'Mechanical Compost Turner - Ch4',
  entity_type:'equipment',
  name:       'Mechanical Compost Turner'
})
SET machine.chapter     = 'Ch4',
    machine.source_id   = 'chunk-ch4-003',
    machine.description = 'Mixer/turner for aeration and microbial spraying during composting. Typical travel ~1.5 m/min; capacity ~30–50 tons/hour.',
    machine.search_text = 'compost turner | aeration | 1.5 m/min | 30–50 t/h | microbial spray'
MERGE (fert)-[:USES_EQUIPMENT {source_id:'chunk-ch4-003'}]->(machine)
WITH fert

// Final Output
MERGE (output:Output:Searchable {
  entity_id:  'Mature Organic Fertilizer - Ch4',
  entity_type:'output',
  name:       'Mature Organic Fertilizer'
})
SET output.chapter     = 'Ch4',
    output.source_id   = 'chunk-ch4-003',
    output.description = 'Dark, crumbly organic fertilizer at ~30–40% moisture; improves soil health and supports sustainable rice production.',
    output.search_text = 'finished compost | mature organic fertilizer | 30–40% moisture | soil health'
MERGE (fert)-[:PRODUCES {source_id:'chunk-ch4-003'}]->(output)
WITH fert

// Benefits
MERGE (impact:Benefit:Searchable {
  entity_id:  'Sustainable Soil Enrichment - Ch4',
  entity_type:'benefit',
  name:       'Sustainable Soil Enrichment'
})
SET impact.chapter     = 'Ch4',
    impact.source_id   = 'chunk-ch4-003',
    impact.description = 'Recycles straw waste, reduces chemical inputs, and boosts microbial fertility in rice-growing regions.',
    impact.search_text = 'soil enrichment | straw recycling | lower chemical input | microbial fertility'
MERGE (fert)-[:ACHIEVES {source_id:'chunk-ch4-003'}]->(impact)
"""
