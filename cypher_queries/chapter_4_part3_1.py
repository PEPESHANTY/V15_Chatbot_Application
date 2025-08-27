cypher= """


// === Chapter 4 - Part 3: Uses of Collected Straw ===
MERGE (use_straw:Practice {
  entity_id: "Uses of Collected Straw - Ch4",
  entity_type: "practice",
  description: "Collected straw from GAP-compliant fields can be used as mulch, mushroom substrate, livestock feed, biobed material, or compost. This enables nutrient recycling and sustainable soil health.",
  source_id: "chunk-ch4-003"
})
WITH use_straw

MATCH (ch4:Chapter {entity_id: "Straw Management - Ch4"})
MERGE (ch4)-[:COVERS]->(use_straw)
WITH use_straw

// === Clean Source Guideline ===
MERGE (gap:Guideline {
  entity_id: "GAP-Compliant Straw - Ch4",
  entity_type: "guideline",
  description: "Straw should come from well-managed fields following Good Agricultural Practices to avoid pesticide residues, heavy metals, or pathogens.",
  source_id: "chunk-ch4-003"
})
MERGE (use_straw)-[:REQUIRES]->(gap)
WITH use_straw

// === List of Applications ===
UNWIND [
  ["Mulching for Crops - Ch4", "Applying straw at the base of crops or trees to conserve moisture, suppress weeds, improve structure, and enrich soil via decomposition."],
  ["Mushroom Cultivation - Ch4", "Using clean, nutrient-rich straw as substrate for growing edible mushrooms like oyster or straw mushrooms."],
  ["Animal Feed - Ch4", "Processed or chopped straw fed to buffaloes and cattle as part of a nutrient-supplemented livestock diet."],
  ["Biobed Materials - Ch4", "Straw used in bio-beds or animal bedding systems to absorb waste and support microbial filtering."],
  ["Organic Fertilizer - Ch4", "Decomposed straw composted into organic fertilizer for nutrient recycling."]
] AS entry
MERGE (u:UseCase {
  entity_id: entry[0],
  entity_type: "use_case",
  name: entry[0],
  description: entry[1],
  source_id: "chunk-ch4-003"
})
MERGE (use_straw)-[:INCLUDES]->(u)
WITH use_straw

// === 3.1 Mulching for Crops ===
MERGE (mulch:Practice {
  entity_id: "Straw Mulching - Ch4",
  entity_type: "practice",
  description: "Straw mulch helps suppress weeds, retain soil moisture, regulate temperature, reduce chemical input needs, and add organic matter during decomposition.",
  source_id: "chunk-ch4-003"
})
MERGE (use_straw)-[:DETAILED_IN]->(mulch)
WITH mulch

MERGE (weed_suppress:Benefit {
  entity_id: "Weed Suppression - Ch4",
  entity_type: "benefit",
  description: "Mulching blocks sunlight and inhibits weed growth, reducing competition for light and nutrients.",
  source_id: "chunk-ch4-003"
})
MERGE (moisture_retain:Benefit {
  entity_id: "Soil Moisture Retention - Ch4",
  entity_type: "benefit",
  description: "Straw mulch reduces evaporation and retains water near root zones.",
  source_id: "chunk-ch4-003"
})
MERGE (soil_structure:Benefit {
  entity_id: "Soil Structure Improvement - Ch4",
  entity_type: "benefit",
  description: "Preserves porosity and root aeration. Decomposing straw enhances soil tilth and organic matter.",
  source_id: "chunk-ch4-003"
})
MERGE (reduced_inputs:Benefit {
  entity_id: "Reduced Input Needs - Ch4",
  entity_type: "benefit",
  description: "Lowers labor, watering, weeding, and fertilizer needs, saving time and money.",
  source_id: "chunk-ch4-003"
})
MERGE (mulch)-[:ACHIEVES]->(weed_suppress)
MERGE (mulch)-[:ACHIEVES]->(moisture_retain)
MERGE (mulch)-[:ACHIEVES]->(soil_structure)
MERGE (mulch)-[:ACHIEVES]->(reduced_inputs)
WITH mulch

// === Mulching for Vegetable & Row Crops ===
MERGE (veg_mulch:UseCase {
  entity_id: "Straw Mulch on Vegetables - Ch4",
  entity_type: "use_case",
  description: "Straw applied on vegetable beds retains moisture, controls weeds, regulates temperature, and supports microbial life. Works with dry or wet straw.",
  source_id: "chunk-ch4-003"
})
MERGE (mulch)-[:USED_ON]->(veg_mulch)

MERGE (non_host:Guideline {
  entity_id: "Non-host Crop Recommendation - Ch4",
  entity_type: "guideline",
  description: "Straw should be applied to crops that are not hosts of rice pests to avoid cross-contamination.",
  source_id: "chunk-ch4-003"
})
MERGE (veg_mulch)-[:FOLLOWS]->(non_host)
WITH mulch, veg_mulch

MERGE (soil_prep:Step {
  entity_id: "Soil Preparation Before Mulching - Ch4",
  entity_type: "step",
  description: "Prepare soil and raised beds before applying straw mulch to ensure good placement and efficiency.",
  source_id: "chunk-ch4-003"
})
MERGE (thin_layer:Parameter {
  entity_id: "Thin Mulch Layer for Small Seeds - Ch4",
  entity_type: "parameter",
  description: "Use a light straw layer for small-seeded crops to avoid blocking emergence.",
  source_id: "chunk-ch4-003"
})
MERGE (uniform_spread:Step {
  entity_id: "Even Straw Distribution - Ch4",
  entity_type: "step",
  description: "Spread straw evenly over the bed surface to ensure uniform coverage, temperature regulation, and moisture conservation.",
  source_id: "chunk-ch4-003"
})
MERGE (thick_layer:Parameter {
  entity_id: "Thick Mulch for Seedlings - Ch4",
  entity_type: "parameter",
  description: "For transplanted crops and legumes, use thicker mulch to insulate roots and reduce watering frequency.",
  source_id: "chunk-ch4-003"
})
MERGE (veg_mulch)-[:REQUIRES]->(soil_prep)
MERGE (veg_mulch)-[:REQUIRES]->(thin_layer)
MERGE (veg_mulch)-[:REQUIRES]->(uniform_spread)
MERGE (veg_mulch)-[:REQUIRES]->(thick_layer)
WITH mulch, veg_mulch

MERGE (reincorp:Step {
  entity_id: "Plow Decomposed Mulch into Soil - Ch4",
  entity_type: "step",
  description: "After harvest, plow decomposed mulch into soil to recycle nutrients, improve structure, and enhance carbon sequestration.",
  source_id: "chunk-ch4-003"
})
MERGE (veg_mulch)-[:FOLLOWS_WITH]->(reincorp)
WITH mulch

// === Mulching for Fruit Trees ===
MERGE (tree_mulch:UseCase {
  entity_id: "Straw Mulching for Fruit Trees - Ch4",
  entity_type: "use_case",
  description: "Apply straw around fruit trees to retain moisture, suppress weeds, and enrich soil. Adjust placement to avoid rot risk.",
  source_id: "chunk-ch4-003"
})
MERGE (mulch)-[:USED_ON]->(tree_mulch)

MERGE (establish_phase:Step {
  entity_id: "Early Tree Mulching - Ch4",
  entity_type: "step",
  description: "At planting, apply thick straw mulch over entire soil surface under canopy to stabilize microclimate and aid establishment.",
  source_id: "chunk-ch4-003"
})
MERGE (mature_phase:Step {
  entity_id: "Mature Tree Mulching - Ch4",
  entity_type: "step",
  description: "Apply mulch at canopy drip line, avoiding direct contact with trunk to prevent stem rot.",
  source_id: "chunk-ch4-003"
})
MERGE (vent_during_rain:Step {
  entity_id: "Rainy Season Ventilation - Ch4",
  entity_type: "step",
  description: "During rainy season, remove mulch near trunk base to prevent root rot and allow air flow.",
  source_id: "chunk-ch4-003"
})
MERGE (no_tillage:Benefit {
  entity_id: "No-Till Straw Decomposition - Ch4",
  entity_type: "benefit",
  description: "Straw decomposes in place, enriching orchard soil without tilling. Low-labor and improves fertility long-term.",
  source_id: "chunk-ch4-003"
})
MERGE (tree_mulch)-[:REQUIRES]->(establish_phase)
MERGE (tree_mulch)-[:REQUIRES]->(mature_phase)
MERGE (tree_mulch)-[:REQUIRES]->(vent_during_rain)
MERGE (tree_mulch)-[:ACHIEVES]->(no_tillage)


"""