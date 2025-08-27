cypher= """


// === Chapter 4 – Part 3.4: Biological Bedding for Livestock ===
MERGE (biobed:Practice {
  entity_id: "Biological Straw Bedding - Ch4",
  entity_type: "practice",
  description: "Using dry rice straw mixed with microbial inoculants and manure to create biological bedding for buffaloes and cows. Enhances hygiene and is recyclable into organic fertilizer.",
  source_id: "chunk-ch4-003"
})
WITH biobed

MATCH (ch4:Chapter {entity_id: "Straw Management - Ch4"})
MERGE (ch4)-[:COVERS]->(biobed)
WITH biobed

// === Required Input: GAP-Compliant Dry Straw ===
MERGE (straw:Input {
  entity_id: "Dry GAP Straw - Ch4",
  entity_type: "input",
  description: "Straw collected from GAP-certified rice fields with moisture <18%, resistant to mold and easy to store.",
  source_id: "chunk-ch4-003"
})
MERGE (biobed)-[:REQUIRES]->(straw)
WITH biobed

// === Additional Components ===
UNWIND [
  ["Microbial Inoculant - Ch4", "Biological agents added to the bedding mix to enhance microbial activity and decomposition."],
  ["Cattle or Buffalo Manure - Ch4", "Animal waste added to bedding to improve microbial fermentation and nutrient content."]
] AS comp
MERGE (c:Input {
  entity_id: comp[0],
  entity_type: "input",
  description: comp[1],
  source_id: "chunk-ch4-003"
})
MERGE (biobed)-[:COMBINED_WITH]->(c)
WITH biobed

// === Application Step ===
MERGE (setup:Step {
  entity_id: "Bedding Preparation and Use - Ch4",
  entity_type: "step",
  description: "Mix 50% shredded straw with 50% organic matter and microbial agents; apply in 20–30 cm layers in barns.",
  source_id: "chunk-ch4-003"
})
MERGE (biobed)-[:HAS_STEP]->(setup)
WITH biobed

// === Benefit: Hygiene and Animal Health ===
MERGE (benefit1:Benefit {
  entity_id: "Improved Hygiene and Comfort - Ch4",
  entity_type: "benefit",
  description: "Biological bedding absorbs moisture, reduces odor, and improves animal comfort and health.",
  source_id: "chunk-ch4-003"
})
MERGE (biobed)-[:ACHIEVES]->(benefit1)
WITH biobed

// === Output: Organic Fertilizer ===
MERGE (output:Output {
  entity_id: "Organic Fertilizer from Biobed - Ch4",
  entity_type: "output",
  description: "After use, the nutrient-rich bedding is composted into organic fertilizer, supporting circular agriculture.",
  source_id: "chunk-ch4-003"
})
MERGE (biobed)-[:PRODUCES]->(output)



"""