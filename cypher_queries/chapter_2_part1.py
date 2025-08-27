cypher = """
// === Chapter 2 Central Node ===
MERGE (ch2:Chapter {
  entity_id: "Cultivation Techniques - Ch2",
  entity_type: "chapter",
  description: "Chapter 2 of the One Million Hectares Project focuses on sustainable rice cultivation techniques in the Mekong Delta, including land preparation, sowing, irrigation, fertilization, pest management, and harvesting.",
  file_path: "book_1.pdf",
  source_id: "chunk-ch2-001"
})
WITH ch2

// === Land Preparation Main Node ===
MERGE (lp:Practice {
  entity_id: "Land Preparation - Ch2",
  entity_type: "practice",
  description: "Pre-sowing preparation stage involving weed control, laser leveling, plowing, soil drying, and rotary tillage. Foundation for mechanized and sustainable rice farming.",
  source_id: "chunk-ch2-001"
})
MERGE (ch2)-[:COVERS]->(lp)
WITH ch2, lp

// === Guideline Document ===
MERGE (guideline:Document {
  entity_id: "Decision No. 73/QĐ-TT-VPPN",
  entity_type: "document",
  description: "Official guideline on soil preparation in Mekong Delta, issued April 25, 2022 by the Department of Crop Production.",
  source_id: "chunk-ch2-001"
})
MERGE (lp)-[:GUIDED_BY]->(guideline)
WITH lp

// === Laser Land Leveling ===
MERGE (laser:Technology {
  entity_id: "Laser Land Leveling",
  entity_type: "technology",
  description: "Automated leveling system using laser transmitters, receivers, and hydraulic blade control to ensure <5cm elevation difference.",
  source_id: "chunk-ch2-001"
})
MERGE (lp)-[:USES]->(laser)
WITH lp, laser

MERGE (comp:Equipment {
  entity_id: "Laser Leveling System Components",
  entity_type: "equipment",
  description: "Includes laser transmitter, receiver, hydraulic blade controller, and electronic control box mounted on tractors.",
  source_id: "chunk-ch2-001"
})
MERGE (laser)-[:COMPRISES]->(comp)
WITH lp

// === Rotary Tillage ===
MERGE (tillage:Practice {
  entity_id: "Rotary Tillage",
  entity_type: "practice",
  description: "Includes wet tillage (2 stages) and dry tillage using rotary blades (C, L, LC) at 7–15cm depth to aerate soil and prepare seedbed.",
  source_id: "chunk-ch2-001"
})
MERGE (lp)-[:INCLUDES]->(tillage)
WITH lp, tillage

MERGE (tractor:Equipment {
  entity_id: "4-Wheel Tractor with Cage Wheels",
  entity_type: "equipment",
  description: "Used in wet tillage to increase traction; supports blade-based rotary tilling.",
  source_id: "chunk-ch2-001"
})
MERGE (tillage)-[:USES]->(tractor)
WITH lp

// === Soil Drying and Sanitation ===
MERGE (sun_drying:Practice {
  entity_id: "Soil Sun-Drying",
  entity_type: "practice",
  description: "Phơi ải phase (15–30 days): exposes soil to sunlight to kill pathogens, improve aeration, and decompose straw.",
  source_id: "chunk-ch2-001"
})
MERGE (lp)-[:INCLUDES]->(sun_drying)

MERGE (sanitation:Practice {
  entity_id: "Field Sanitation",
  entity_type: "practice",
  description: "Cleaning field edges, reinforcing dikes, destroying golden apple snail eggs before sowing.",
  source_id: "chunk-ch2-001"
})
MERGE (lp)-[:INCLUDES]->(sanitation)
WITH lp

// === Drainage Furrows ===
MERGE (furrows:Practice {
  entity_id: "Water Drainage Furrows",
  entity_type: "practice",
  description: "6–9 meter spaced furrows (20–30 cm wide, 15–20 cm deep) to improve drainage, aeration, and salt leaching.",
  source_id: "chunk-ch2-001"
})
MERGE (lp)-[:INCLUDES]->(furrows)
WITH lp

// === Soil Preparation Methods ===
UNWIND range(1,6) AS idx
MERGE (m:Method {
  entity_id: "Soil Prep Method #" + idx,
  entity_type: "method",
  description: "Context-specific soil preparation method #" + idx + " used in the Mekong Delta based on water, season, or soil condition.",
  source_id: "chunk-ch2-001"
})
MERGE (lp)-[:USES_METHOD]->(m)
WITH lp

// === Final Field Leveling ===
MERGE (leveling:Practice {
  entity_id: "Final Field Leveling",
  entity_type: "practice",
  description: "Last step before sowing, using 2-wheel or 4-wheel tractors to ensure flat surface with <5cm height difference.",
  source_id: "chunk-ch2-001"
})
MERGE (lp)-[:FOLLOWS_WITH]->(leveling)
WITH lp

// === Golden Apple Snail Control ===
MERGE (snail:Threat {
  entity_id: "Golden Apple Snail",
  entity_type: "pest",
  description: "Invasive snail species; control includes drainage, sun-drying, egg removal, and mechanical disruption during tillage.",
  source_id: "chunk-ch2-001"
})
MERGE (lp)-[:TARGETS]->(snail)
WITH lp

// === Summary Node for Emissions Relevance ===
MERGE (emissions:Concept {
  entity_id: "GHG Emission Reduction",
  entity_type: "concept",
  description: "Land preparation techniques reduce methane by minimizing waterlogging and integrating organic decomposition strategies.",
  source_id: "chunk-ch2-001"
})
MERGE (lp)-[:CONTRIBUTES_TO]->(emissions)


"""