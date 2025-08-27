cypher= """

// === In-field Straw Treatment Node ===
MERGE (treat:Practice {
  entity_id: "In-field Straw Treatment - Ch4",
  entity_type: "practice",
  description: "Field stubble should be plowed or chopped into the soil in dry conditions, supported by biological agents like Trichoderma to accelerate decomposition and reduce emissions.",
  source_id: "chunk-ch4-002"
})
WITH treat

// === Chapter 4 Central Node ===
MATCH (ch4:Chapter {entity_id: "Straw Management - Ch4"})
MERGE (ch4)-[:COVERS]->(treat)
WITH treat

// === Season-specific Treatment Nodes ===
MERGE (winter:Season {
  entity_id: "Winter-Spring Crop - Ch4",
  entity_type: "season",
  description: "Immediately plow/bury stubble after harvest; maintain dry conditions for at least 3 weeks for effective aerobic decomposition.",
  source_id: "chunk-ch4-002"
})
MERGE (treat)-[:APPLIES_DURING]->(winter)

MERGE (summer:Season {
  entity_id: "Summer-Autumn & Autumn-Winter Crops - Ch4",
  entity_type: "season",
  description: "Till immediately after harvest and spray biological agents like Trichoderma to speed decomposition, especially for short crop cycles.",
  source_id: "chunk-ch4-002"
})
MERGE (treat)-[:APPLIES_DURING]->(summer)
WITH treat

// === Biological Treatment ===
MERGE (tricho:Input {
  entity_id: "Trichoderma - Ch4",
  entity_type: "input",
  description: "Microbial agent applied before plowing to accelerate straw breakdown. Recommended at 0.1% of total straw volume.",
  source_id: "chunk-ch4-002"
})
MERGE (bio:Method {
  entity_id: "Biological Decomposition - Ch4",
  entity_type: "method",
  description: "Incorporating straw under dry conditions, supported by microbial inoculants like Trichoderma, enhances aerobic decomposition and soil health.",
  source_id: "chunk-ch4-002"
})
MERGE (treat)-[:USES]->(tricho)
MERGE (treat)-[:USES]->(bio)
WITH treat, bio

// === Machinery ===
MERGE (tiller:Equipment {
  entity_id: "Rotary Tiller - Ch4",
  entity_type: "equipment",
  description: "Used to incorporate stubble into soil at 10–15 cm depth. Key for residue mixing and decomposition.",
  source_id: "chunk-ch4-002"
})
MERGE (tractor:Equipment {
  entity_id: "Tractor for Tillage - Ch4",
  entity_type: "equipment",
  description: "Tractor used with rotary tiller to plow and bury stubble, promoting aerobic breakdown and preparing field for next cycle.",
  source_id: "chunk-ch4-002"
})
MERGE (treat)-[:USES]->(tiller)
MERGE (treat)-[:USES]->(tractor)
WITH treat, bio

// === Conditions and Warnings ===
MERGE (dry_cond:Condition {
  entity_id: "Dry Field Condition - Ch4",
  entity_type: "condition",
  description: "After incorporation, field must remain non-flooded for 3+ weeks to ensure aerobic decomposition and prevent methane.",
  source_id: "chunk-ch4-002"
})
MERGE (flooded_cond:Threat {
  entity_id: "Flooded Straw Burial - Ch4",
  entity_type: "threat",
  description: "Anaerobic decomposition in flooded fields produces methane, leads to nutrient loss and environmental damage.",
  source_id: "chunk-ch4-002"
})
MERGE (burn_straw:Threat {
  entity_id: "Straw Burning - Ch4",
  entity_type: "threat",
  description: "Prohibited due to air pollution and complete nutrient loss, especially nitrogen.",
  source_id: "chunk-ch4-002"
})
MERGE (treat)-[:REQUIRES]->(dry_cond)
MERGE (treat)-[:AVOIDS]->(flooded_cond)
MERGE (treat)-[:AVOIDS]->(burn_straw)
WITH treat, bio, flooded_cond, burn_straw

// === Nutrient Content & Loss ===
MERGE (nutrients:Concept {
  entity_id: "Nutrient Composition in Straw - Ch4",
  entity_type: "concept",
  description: "1 ton of straw contains ~5–8 kg N, 1.6–2.7 kg P, 14–20 kg K. Burning or improper burial leads to major nutrient losses.",
  source_id: "chunk-ch4-002"
})
MERGE (loss:Concept {
  entity_id: "Nutrient Loss from Straw Burning - Ch4",
  entity_type: "concept",
  description: "Burning results in 100% N loss, 25% P loss, 20% K loss — severely impacting soil fertility.",
  source_id: "chunk-ch4-002"
})
MERGE (treat)-[:PRESERVES]->(nutrients)
MERGE (burn_straw)-[:CAUSES]->(loss)
WITH treat, bio, flooded_cond

// === Environmental Impact ===
MERGE (methane:Emission {
  entity_id: "Methane Emissions - Ch4",
  entity_type: "emission",
  description: "Anaerobic breakdown in flooded fields generates CH₄, a potent greenhouse gas contributing to climate change.",
  source_id: "chunk-ch4-002"
})
MERGE (flooded_cond)-[:RELEASES]->(methane)
MERGE (bio)-[:REDUCES]->(methane)
WITH treat

// === Post-Treatment Benefits ===
MERGE (fertility:Benefit {
  entity_id: "Soil Fertility Enhancement - Ch4",
  entity_type: "benefit",
  description: "Dry field decomposition retains nutrients and improves long-term soil fertility and structure.",
  source_id: "chunk-ch4-002"
})
MERGE (recycling:Benefit {
  entity_id: "Nutrient Recycling - Ch4",
  entity_type: "benefit",
  description: "Efficient decomposition supports recycling of N, P, and K back into the soil, aiding sustainable yields.",
  source_id: "chunk-ch4-002"
})
MERGE (climate:Benefit {
  entity_id: "GHG Reduction - Ch4",
  entity_type: "benefit",
  description: "Field treatment without flooding or burning reduces greenhouse gas emissions and aligns with climate goals.",
  source_id: "chunk-ch4-002"
})
MERGE (treat)-[:ACHIEVES]->(fertility)
MERGE (treat)-[:ACHIEVES]->(recycling)
MERGE (treat)-[:ACHIEVES]->(climate)


"""