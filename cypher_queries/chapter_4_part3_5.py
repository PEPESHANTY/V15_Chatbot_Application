cypher= """


// === Chapter 4 – Part 3.5: Organic Fertilizer from Rice Straw ===
MERGE (fert:Practice {
  entity_id: "Organic Fertilizer from Rice Straw - Ch4",
  entity_type: "practice",
  description: "Mechanized composting of rice straw with manure and microbial inoculants under regulated temperature, moisture, and pH to produce high-quality organic fertilizer.",
  source_id: "chunk-ch4-003"
})
WITH fert

MATCH (ch4:Chapter {entity_id: "Straw Management - Ch4"})
MERGE (ch4)-[:COVERS]->(fert)
WITH fert

// === Core Inputs ===
UNWIND [
  ["Rice Straw - Composting - Ch4", "Base substrate with ~14%–60% moisture, used in alternating layers with manure or urea."],
  ["Livestock Manure - Ch4", "Dry cattle manure or enriched agricultural soil used to balance C:N ratio."],
  ["Urea 46N - Ch4", "Alternative nitrogen supplement for semi-wet straw when manure is unavailable."],
  ["Microbial Inoculants - Compost - Ch4", "Biological agents added to accelerate decomposition and enhance microbial activity."],
  ["Water - Compost - Ch4", "Maintains 50–60% moisture during fermentation; added via spray system."],
  ["Coconut Husk Fiber - Ch4", "Optional additive to improve compost porosity and structure."],
  ["Rice Husk Ash - Ch4", "Optional ash additive to retain nutrients and regulate compost density."]
] AS mat
MERGE (input:Input {
  entity_id: mat[0],
  entity_type: "input",
  description: mat[1],
  source_id: "chunk-ch4-003"
})
MERGE (fert)-[:REQUIRES]->(input)
WITH fert

// === Compost Preparation and Layering ===
MERGE (prep:Step {
  entity_id: "Compost Trench Layering - Ch4",
  entity_type: "step",
  description: "Alternate 20cm layers of straw and manure/soil in a 1.2m x 0.7m trench. Maintain C:N ratio of 25–30. Use compost turner to mix and spray microbes at 1.5 m/min.",
  source_id: "chunk-ch4-003"
})
MERGE (fert)-[:HAS_STEP]->(prep)
WITH fert

// === Fermentation Stage ===
MERGE (phase3:Step {
  entity_id: "Fermentation Conditions - Ch4",
  entity_type: "step",
  description: "Cover with tarp; maintain 50–70°C temp, 50–60% moisture, and pH 6.5–7. Turn if >70°C.",
  source_id: "chunk-ch4-003"
})
MERGE (fert)-[:HAS_STEP]->(phase3)
WITH fert

// === Aeration and Cooling Stage ===
MERGE (phase4:Step {
  entity_id: "Cooling and Aeration Phase - Ch4",
  entity_type: "step",
  description: "After 10–15 days, turn again to lower temp to 30–50°C. Adjust moisture to 40–50%. Add coconut husk fiber and ash in 40:40:20 ratio with manure.",
  source_id: "chunk-ch4-003"
})
MERGE (fert)-[:HAS_STEP]->(phase4)
WITH fert

// === Maturation Stage ===
MERGE (mature:Step {
  entity_id: "Final Maturation - Ch4",
  entity_type: "step",
  description: "After 30–45 days, compost reaches 30–40% moisture. It becomes dark, crumbly, stable, and is sieved to remove coarse debris.",
  source_id: "chunk-ch4-003"
})
MERGE (fert)-[:HAS_STEP]->(mature)
WITH fert

// === Equipment ===
MERGE (machine:Equipment {
  entity_id: "Mechanical Compost Turner - Ch4",
  entity_type: "equipment",
  description: "Used for mixing, aeration, and spraying microbial solution during composting. Operates at 1.5 m/min; handles 30–50 tons/hour.",
  source_id: "chunk-ch4-003"
})
MERGE (fert)-[:USES_EQUIPMENT]->(machine)
WITH fert

// === Final Output ===
MERGE (output:Output {
  entity_id: "Mature Organic Fertilizer - Ch4",
  entity_type: "output",
  description: "Dark, crumbly fertilizer with 30–40% moisture. Improves soil health and supports sustainable rice production.",
  source_id: "chunk-ch4-003"
})
MERGE (fert)-[:PRODUCES]->(output)
WITH fert

// === Benefits ===
MERGE (impact:Benefit {
  entity_id: "Sustainable Soil Enrichment - Ch4",
  entity_type: "benefit",
  description: "Recycles straw waste, reduces chemical input, and boosts microbial soil fertility in rice-growing regions.",
  source_id: "chunk-ch4-003"
})
MERGE (fert)-[:ACHIEVES]->(impact)


"""