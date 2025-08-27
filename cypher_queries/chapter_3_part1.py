cypher= """

// === Chapter 3 Central Node ===
MERGE (ch3:Chapter {
  entity_id: "Harvesting and Post-Harvest Management - Ch3",
  entity_type: "chapter",
  description: "Chapter 3 of the One Million Hectares Project focuses on post-harvest practices that reduce grain loss, improve rice quality, and maintain market value. It includes timely harvesting, threshing, drying, storage, milling, and market preparation.",
  file_path: "book_1.pdf",
  source_id: "chunk-ch3-001",
  created_at: timestamp()
})
WITH ch3

// === Main Harvesting Practice Node ===
MERGE (harvest:Practice {
  entity_id: "Harvesting - Ch3",
  entity_type: "practice",
  description: "Harvesting is a critical phase in rice production, best performed when 85–90% of grains are golden to maximize yield and quality. Delays lead to shattering and pest loss.",
  source_id: "chunk-ch3-001"
})
MERGE (ch3)-[:COVERS]->(harvest)
WITH ch3, harvest

// === Optimal Timing Node ===
MERGE (timing:Parameter {
  entity_id: "Optimal Harvest Timing - Ch3",
  entity_type: "parameter",
  description: "Harvest when 85–90% of grains have turned golden or straw-colored. This indicates full physiological maturity with maximum grain weight and quality.",
  source_id: "chunk-ch3-001"
})
MERGE (harvest)-[:REQUIRES]->(timing)

// === Combine Harvester Node ===
MERGE (combine:Technology {
  entity_id: "Combine Harvester - Ch3",
  entity_type: "technology",
  description: "Multi-functional machine that performs cutting, threshing, cleaning, and bagging in one operation, improving harvest efficiency and reducing labor needs.",
  source_id: "chunk-ch3-001"
})
MERGE (harvest)-[:USES]->(combine)

// === Mechanization Benefit Node ===
MERGE (mech:Concept {
  entity_id: "Mechanized Harvesting Efficiency - Ch3",
  entity_type: "concept",
  description: "Mechanized harvesting reduces grain loss, improves timeliness, and enables field turnover in multi-season systems. Essential for modern large-scale rice farming.",
  source_id: "chunk-ch3-001"
})
MERGE (combine)-[:IMPROVES]->(mech)
MERGE (harvest)-[:ENHANCES]->(mech)

// === Loss Reduction Concept ===
MERGE (loss:Concept {
  entity_id: "Post-Harvest Loss Reduction - Ch3",
  entity_type: "concept",
  description: "Timely and mechanized harvesting reduces grain loss due to delays, shattering, pest damage, and inefficient manual practices.",
  source_id: "chunk-ch3-001"
})
MERGE (harvest)-[:REDUCES]->(loss)

// === Sustainability Outcome Node ===
MERGE (sustain:Concept {
  entity_id: "Sustainability Gains - Ch3",
  entity_type: "concept",
  description: "Improved harvesting methods lower GHG emissions by over 10% and increase farmer income, contributing to sustainable rice value chains.",
  source_id: "chunk-ch3-001"
})
MERGE (harvest)-[:CONTRIBUTES_TO]->(sustain)

// === Field Turnover Impact ===
MERGE (turnover:Benefit {
  entity_id: "Timely Field Turnover - Ch3",
  entity_type: "benefit",
  description: "Mechanized harvest accelerates field clearance, enabling on-time land preparation for the next crop in multi-season systems.",
  source_id: "chunk-ch3-001"
})
MERGE (harvest)-[:ENABLES]->(turnover)


"""