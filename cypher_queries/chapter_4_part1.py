cypher= """


// === Chapter 4 Central Node ===
MERGE (ch4:Chapter {
  entity_id: "Straw Management - Ch4",
  entity_type: "chapter",
  description: "Chapter 4 focuses on circular straw management to minimize emissions, improve soil health, and utilize rice straw in sustainable ways such as mulching, composting, mushroom cultivation, and feed.",
  file_path: "book_1.pdf",
  source_id: "chunk-ch4-001",
  created_at: timestamp()
})
WITH ch4

// === Part 1 Main Practice Node ===
MERGE (collect:Practice {
  entity_id: "Straw Collection - Ch4",
  entity_type: "practice",
  description: "Straw should be collected within 5 days post-harvest to preserve nutritional quality and reduce methane emissions. Immediate collection is critical in wet fields.",
  source_id: "chunk-ch4-001"
})
MERGE (ch4)-[:COVERS]->(collect)
WITH ch4, collect

// === Circular Management Principle ===
MERGE (circular:Concept {
  entity_id: "Circular Straw Management - Ch4",
  entity_type: "concept",
  description: "Discourages burning and field burial. Promotes collection and reuse of straw for mushroom cultivation, animal feed, organic fertilizer, and other circular uses.",
  source_id: "chunk-ch4-001"
})
MERGE (collect)-[:ALIGNS_WITH]->(circular)

MERGE (burning:Threat {
  entity_id: "Straw Burning - Ch4",
  entity_type: "threat",
  description: "Causes air pollution, nutrient loss, and biodiversity degradation.",
  source_id: "chunk-ch4-001"
})
MERGE (circular)-[:AVOIDS]->(burning)

MERGE (burial:Threat {
  entity_id: "Flooded Straw Burial - Ch4",
  entity_type: "threat",
  description: "Releases methane (CH₄) during anaerobic decomposition in flooded fields.",
  source_id: "chunk-ch4-001"
})
MERGE (circular)-[:AVOIDS]->(burial)

MERGE (srp:Standard {
  entity_id: "Sustainable Rice Platform Goals - Ch4",
  entity_type: "standard",
  description: "Low-emission, resource-efficient guidelines aligned with circular straw reuse and regenerative practices.",
  source_id: "chunk-ch4-001"
})
MERGE (circular)-[:SUPPORTS]->(srp)

WITH collect

// === Collection Timing ===
MERGE (timing:Parameter {
  entity_id: "Straw Collection Timing - Ch4",
  entity_type: "parameter",
  description: "Straw must be collected within 5 days post-harvest to preserve protein content and prevent microbial degradation.",
  source_id: "chunk-ch4-001"
})
MERGE (collect)-[:REQUIRES]->(timing)

// === Machinery Types ===
MERGE (tractor_baler:Equipment {
  entity_id: "Tractor-Mounted Baler - Ch4",
  entity_type: "equipment",
  description: "Requires 25 HP tractor, effective only in dry fields, lacks onboard storage and needs extra vehicle for transport.",
  source_id: "chunk-ch4-001"
})
MERGE (self_baler:Equipment {
  entity_id: "Self-Propelled Baler - Ch4",
  entity_type: "equipment",
  description: "70+ HP baler with onboard storage (50 bales), crawler tracks for wet conditions, and output of 70–150 bales/hour.",
  source_id: "chunk-ch4-001"
})
MERGE (collect)-[:USES]->(tractor_baler)
MERGE (collect)-[:USES]->(self_baler)

MERGE (crawler:Feature {
  entity_id: "Rubber Crawlers - Ch4",
  entity_type: "feature",
  description: "Enable self-propelled balers to function in wet, muddy fields without getting stuck.",
  source_id: "chunk-ch4-001"
})
MERGE (self_baler)-[:FEATURES]->(crawler)

MERGE (bale_output:Parameter {
  entity_id: "Baling Output - Ch4",
  entity_type: "parameter",
  description: "Self-propelled baler produces 70–150 bales/hour. Bale size: 50x70 cm. Weight: 12–18kg (dry), 20–30kg (wet).",
  source_id: "chunk-ch4-001"
})
MERGE (self_baler)-[:DELIVERS]->(bale_output)

WITH collect

// === Field Conditions Logic ===
MERGE (wet_fields:Condition {
  entity_id: "Wet Field Straw Collection - Ch4",
  entity_type: "condition",
  description: "Requires immediate collection after harvest. Self-propelled baler preferred. Tractor-mounted baler not recommended.",
  source_id: "chunk-ch4-001"
})
MERGE (dry_fields:Condition {
  entity_id: "Dry Field Straw Collection - Ch4",
  entity_type: "condition",
  description: "Straw can be left for ≤5 days. Both baler types possible, but self-propelled more efficient.",
  source_id: "chunk-ch4-001"
})
MERGE (collect)-[:TAILORED_TO]->(wet_fields)
MERGE (collect)-[:TAILORED_TO]->(dry_fields)

// === Raking Machine Use ===
MERGE (rake:Equipment {
  entity_id: "Raking Machine - Ch4",
  entity_type: "equipment",
  description: "Used before baling to aerate and gather straw, improving drying and baling efficiency.",
  source_id: "chunk-ch4-001"
})
MERGE (collect)-[:PRECEDED_BY]->(rake)

// === Manual Collection Option ===
MERGE (manual:Method {
  entity_id: "Manual Straw Collection - Ch4",
  entity_type: "method",
  description: "Labor-intensive fallback for areas without access to mechanized baling.",
  source_id: "chunk-ch4-001"
})
MERGE (collect)-[:ALTERNATIVE_METHOD]->(manual)

"""