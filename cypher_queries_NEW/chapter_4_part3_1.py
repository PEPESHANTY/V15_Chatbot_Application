cypher = """
// =======================================================
// Chapter 4 — Part 3: Uses of Collected Straw (single statement)
// =======================================================

// Root practice
MERGE (use_straw:Practice:Searchable {
  entity_id:  'Uses of Collected Straw - Ch4',
  entity_type:'practice',
  name:       'Uses of Collected Straw'
})
SET use_straw.chapter     = 'Ch4',
    use_straw.source_id   = 'chunk-ch4-003',
    use_straw.description = 'Collected straw from GAP-compliant fields can be used as mulch, mushroom substrate, livestock feed, biobed material, or compost. Enables nutrient recycling and sustainable soil health.',
    use_straw.search_text = 'straw uses | mulch | mushroom substrate | animal feed | biobed | compost | nutrient recycling | soil health'

// Link to Chapter 4
WITH use_straw
MATCH (ch4:Chapter {entity_id:'Straw Management - Ch4'})
MERGE (ch4)-[:COVERS {source_id:'chunk-ch4-003'}]->(use_straw)

// Clean source guideline
WITH use_straw
MERGE (gap:Guideline:Searchable {
  entity_id:  'GAP-Compliant Straw - Ch4',
  entity_type:'guideline',
  name:       'GAP-Compliant Straw'
})
SET gap.chapter     = 'Ch4',
    gap.source_id   = 'chunk-ch4-003',
    gap.description = 'Straw should come from well-managed fields following Good Agricultural Practices to avoid pesticide residues, heavy metals, or pathogens.',
    gap.search_text = 'GAP | clean straw source | avoid residues | heavy metals | pathogens'
MERGE (use_straw)-[:REQUIRES {source_id:'chunk-ch4-003'}]->(gap)

// List of top-level applications
WITH use_straw
UNWIND [
  ['Mulching for Crops - Ch4', 'Applying straw at the base of crops or trees to conserve moisture, suppress weeds, improve structure, and enrich soil via decomposition.'],
  ['Mushroom Cultivation - Ch4', 'Using clean, nutrient-rich straw as substrate for growing edible mushrooms (e.g., oyster, straw mushrooms).'],
  ['Animal Feed - Ch4', 'Processed or chopped straw fed to buffaloes and cattle as part of a nutrient-supplemented diet.'],
  ['Biobed Materials - Ch4', 'Straw used in bio-beds/animal bedding to absorb waste and support microbial filtering.'],
  ['Organic Fertilizer - Ch4', 'Decomposed straw composted into organic fertilizer for nutrient recycling.']
] AS entry
MERGE (u:UseCase:Searchable {
  entity_id:  entry[0],
  entity_type:'use_case',
  name:       entry[0]
})
SET u.chapter     = 'Ch4',
    u.source_id   = 'chunk-ch4-003',
    u.description = entry[1],
    u.search_text = entry[0] + ' | ' + entry[1]
MERGE (use_straw)-[:INCLUDES {source_id:'chunk-ch4-003'}]->(u)

// 3.1 Mulching for Crops (detailed)
WITH use_straw
MERGE (mulch:Practice:Searchable {
  entity_id:  'Straw Mulching - Ch4',
  entity_type:'practice',
  name:       'Straw Mulching'
})
SET mulch.chapter     = 'Ch4',
    mulch.source_id   = 'chunk-ch4-003',
    mulch.description = 'Straw mulch suppresses weeds, retains soil moisture, regulates temperature, reduces input needs, and adds organic matter as it decomposes.',
    mulch.search_text = 'straw mulch | weed suppression | moisture retention | temperature regulation | organic matter'
MERGE (use_straw)-[:DETAILED_IN {source_id:'chunk-ch4-003'}]->(mulch)

// Mulching benefits
WITH mulch
UNWIND [
  ['Weed Suppression - Ch4','Mulching blocks sunlight and inhibits weed growth, reducing competition for light and nutrients.'],
  ['Soil Moisture Retention - Ch4','Straw mulch reduces evaporation and retains water near root zones.'],
  ['Soil Structure Improvement - Ch4','Preserves porosity and aeration; decomposing straw enhances tilth and organic matter.'],
  ['Reduced Input Needs - Ch4','Lowers labor, watering, weeding, and fertilizer needs, saving time and money.']
] AS ben
MERGE (b:Benefit:Searchable {
  entity_id:  ben[0],
  entity_type:'benefit',
  name:       ben[0]
})
SET b.chapter     = 'Ch4',
    b.source_id   = 'chunk-ch4-003',
    b.description = ben[1],
    b.search_text = ben[0] + ' | ' + ben[1]
MERGE (mulch)-[:ACHIEVES {source_id:'chunk-ch4-003'}]->(b)

// Mulching for vegetable & row crops
WITH mulch
MERGE (veg_mulch:UseCase:Searchable {
  entity_id:  'Straw Mulch on Vegetables - Ch4',
  entity_type:'use_case',
  name:       'Straw Mulch on Vegetables'
})
SET veg_mulch.chapter     = 'Ch4',
    veg_mulch.source_id   = 'chunk-ch4-003',
    veg_mulch.description = 'Straw applied on vegetable beds retains moisture, controls weeds, regulates temperature, and supports microbial life. Works with dry or wet straw.',
    veg_mulch.search_text = 'vegetable mulch | row crops | dry/wet straw | microbial life'
MERGE (mulch)-[:USED_ON {source_id:'chunk-ch4-003'}]->(veg_mulch)

// Non-host guideline + application steps/params
WITH mulch, veg_mulch
MERGE (non_host:Guideline:Searchable {
  entity_id:  'Non-host Crop Recommendation - Ch4',
  entity_type:'guideline',
  name:       'Non-host Crop Recommendation'
})
SET non_host.chapter     = 'Ch4',
    non_host.source_id   = 'chunk-ch4-003',
    non_host.description = 'Apply straw to crops that are not hosts of rice pests to avoid cross-contamination.',
    non_host.search_text = 'non-host crops | avoid rice pest hosts | cross-contamination'
MERGE (veg_mulch)-[:FOLLOWS {source_id:'chunk-ch4-003'}]->(non_host)

MERGE (soil_prep:Step:Searchable {
  entity_id:  'Soil Preparation Before Mulching - Ch4',
  entity_type:'step',
  name:       'Soil Preparation Before Mulching'
})
SET soil_prep.chapter     = 'Ch4',
    soil_prep.source_id   = 'chunk-ch4-003',
    soil_prep.description = 'Prepare soil and raised beds before applying straw mulch to ensure good placement and efficiency.',
    soil_prep.search_text = 'soil preparation | raised beds | mulch placement'
MERGE (veg_mulch)-[:REQUIRES {source_id:'chunk-ch4-003'}]->(soil_prep)

MERGE (thin_layer:Parameter:Searchable {
  entity_id:  'Thin Mulch Layer for Small Seeds - Ch4',
  entity_type:'parameter',
  name:       'Thin Mulch Layer for Small Seeds'
})
SET thin_layer.chapter     = 'Ch4',
    thin_layer.source_id   = 'chunk-ch4-003',
    thin_layer.description = 'Use a light straw layer for small-seeded crops to avoid blocking emergence.',
    thin_layer.search_text = 'thin mulch | small seeds | emergence'
MERGE (veg_mulch)-[:REQUIRES {source_id:'chunk-ch4-003'}]->(thin_layer)

MERGE (uniform_spread:Step:Searchable {
  entity_id:  'Even Straw Distribution - Ch4',
  entity_type:'step',
  name:       'Even Straw Distribution'
})
SET uniform_spread.chapter     = 'Ch4',
    uniform_spread.source_id   = 'chunk-ch4-003',
    uniform_spread.description = 'Spread straw evenly over the bed surface to ensure uniform coverage, temperature regulation, and moisture conservation.',
    uniform_spread.search_text = 'even spread | uniform coverage | temperature | moisture'
MERGE (veg_mulch)-[:REQUIRES {source_id:'chunk-ch4-003'}]->(uniform_spread)

MERGE (thick_layer:Parameter:Searchable {
  entity_id:  'Thick Mulch for Seedlings - Ch4',
  entity_type:'parameter',
  name:       'Thick Mulch for Seedlings'
})
SET thick_layer.chapter     = 'Ch4',
    thick_layer.source_id   = 'chunk-ch4-003',
    thick_layer.description = 'For transplanted crops and legumes, use thicker mulch to insulate roots and reduce watering frequency.',
    thick_layer.search_text = 'thick mulch | seedlings | legumes | insulation'
MERGE (veg_mulch)-[:REQUIRES {source_id:'chunk-ch4-003'}]->(thick_layer)

// Reincorporation step
WITH mulch, veg_mulch
MERGE (reincorp:Step:Searchable {
  entity_id:  'Plow Decomposed Mulch into Soil - Ch4',
  entity_type:'step',
  name:       'Plow Decomposed Mulch into Soil'
})
SET reincorp.chapter     = 'Ch4',
    reincorp.source_id   = 'chunk-ch4-003',
    reincorp.description = 'After harvest, plow decomposed mulch into soil to recycle nutrients, improve structure, and enhance carbon sequestration.',
    reincorp.search_text = 'reincorporate mulch | recycle nutrients | structure | carbon'
MERGE (veg_mulch)-[:FOLLOWS_WITH {source_id:'chunk-ch4-003'}]->(reincorp)

// Mulching for fruit trees
WITH mulch
MERGE (tree_mulch:UseCase:Searchable {
  entity_id:  'Straw Mulching for Fruit Trees - Ch4',
  entity_type:'use_case',
  name:       'Straw Mulching for Fruit Trees'
})
SET tree_mulch.chapter     = 'Ch4',
    tree_mulch.source_id   = 'chunk-ch4-003',
    tree_mulch.description = 'Apply straw around fruit trees to retain moisture, suppress weeds, and enrich soil; avoid direct trunk contact to prevent rot.',
    tree_mulch.search_text = 'fruit trees | mulch at drip line | avoid trunk contact | moisture | weeds'
MERGE (mulch)-[:USED_ON {source_id:'chunk-ch4-003'}]->(tree_mulch)

// Fruit tree steps & benefit
WITH tree_mulch
MERGE (establish_phase:Step:Searchable {
  entity_id:  'Early Tree Mulching - Ch4',
  entity_type:'step',
  name:       'Early Tree Mulching'
})
SET establish_phase.chapter     = 'Ch4',
    establish_phase.source_id   = 'chunk-ch4-003',
    establish_phase.description = 'At planting, apply thick straw mulch under the canopy to stabilize microclimate and aid establishment.',
    establish_phase.search_text = 'early stage | thick mulch | establishment | microclimate'
MERGE (tree_mulch)-[:REQUIRES {source_id:'chunk-ch4-003'}]->(establish_phase)

MERGE (mature_phase:Step:Searchable {
  entity_id:  'Mature Tree Mulching - Ch4',
  entity_type:'step',
  name:       'Mature Tree Mulching'
})
SET mature_phase.chapter     = 'Ch4',
    mature_phase.source_id   = 'chunk-ch4-003',
    mature_phase.description = 'Apply mulch at canopy drip line; avoid direct trunk contact to prevent stem rot.',
    mature_phase.search_text = 'mature trees | drip line | avoid trunk | stem rot'
MERGE (tree_mulch)-[:REQUIRES {source_id:'chunk-ch4-003'}]->(mature_phase)

MERGE (vent_during_rain:Step:Searchable {
  entity_id:  'Rainy Season Ventilation - Ch4',
  entity_type:'step',
  name:       'Rainy Season Ventilation'
})
SET vent_during_rain.chapter     = 'Ch4',
    vent_during_rain.source_id   = 'chunk-ch4-003',
    vent_during_rain.description = 'During rainy season, clear mulch near trunk to prevent root/stem rot and allow airflow.',
    vent_during_rain.search_text = 'rainy season | clear near trunk | airflow | root rot'
MERGE (tree_mulch)-[:REQUIRES {source_id:'chunk-ch4-003'}]->(vent_during_rain)

MERGE (no_tillage:Benefit:Searchable {
  entity_id:  'No-Till Straw Decomposition - Ch4',
  entity_type:'benefit',
  name:       'No-Till Straw Decomposition'
})
SET no_tillage.chapter     = 'Ch4',
    no_tillage.source_id   = 'chunk-ch4-003',
    no_tillage.description = 'Straw decomposes in place, enriching orchard soil without tilling; low-labor and improves long-term fertility.',
    no_tillage.search_text = 'no-till | in-place decomposition | orchard fertility | low labor'
MERGE (tree_mulch)-[:ACHIEVES {source_id:'chunk-ch4-003'}]->(no_tillage)
"""
