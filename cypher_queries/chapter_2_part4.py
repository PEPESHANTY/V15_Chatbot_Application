cypher= """

// === Chapter 2 Water Management Section ===
MATCH (ch2:Chapter {entity_id: "Cultivation Techniques - Ch2"})

// --- Water Management Parent Node ---
MERGE (wm:Practice {
  entity_id: "Water Management - AWD",
  entity_type: "practice",
  source_id: "chunk-ch2-004",
  description: "Alternate Wetting and Drying (AWD) is a water-saving irrigation technique that balances rice crop needs while reducing methane emissions and water waste."
})
MERGE (ch2)-[:COVERS]->(wm)

// --- Technique: Alternate Wetting and Drying ---
MERGE (awd:Technique {
  entity_id: "Alternate Wetting and Drying",
  entity_type: "method",
  source_id: "chunk-ch2-004",
  description: "AWD involves irrigating only when the water table drops at least 15 cm below the soil surface, reducing methane emissions and improving water-use efficiency."
})
MERGE (wm)-[:USES]->(awd)

// --- Pre-Sowing Water Management Rule ---
MERGE (presow:Guideline {
  entity_id: "No Flooding > 30 Days",
  description: "Before sowing, avoid keeping the field continuously flooded for more than 30 days to reduce anaerobic conditions and methane buildup.",
  source_id: "chunk-ch2-004"
})
MERGE (wm)-[:REQUIRES]->(presow)

// --- Observation Indicator ---
MERGE (obs:Tool {
  entity_id: "AWD Monitoring Pipe",
  entity_type: "tool",
  description: "A 10–15 cm perforated tube inserted into the soil to observe water depth and determine AWD irrigation timing.",
  source_id: "chunk-ch2-004"
})
MERGE (awd)-[:MONITORED_BY]->(obs)

// --- AWD Irrigation Trigger Condition ---
MERGE (trigger:Condition {
  entity_id: "Irrigation Trigger - 15cm Dry Depth",
  description: "Water is re-applied when the water level drops 15 cm below the surface or 'nứt chân chim' cracks appear.",
  source_id: "chunk-ch2-004"
})
MERGE (awd)-[:TRIGGERED_BY]->(trigger)

// --- AWD Re-flooding Rule ---
MERGE (reflood:Guideline {
  entity_id: "Re-flooding Limit - 5cm",
  description: "When re-irrigating under AWD, water should be added up to 3–5 cm depth only.",
  source_id: "chunk-ch2-004"
})
MERGE (awd)-[:FOLLOWS]->(reflood)

// === WITH before UNWIND ===
WITH awd

// --- AWD Schedule Stages ---
UNWIND [
  ["Day 1–7", "Keep the field moist to promote healthy germination."],
  ["Day 12–22", "Drain water to oxygenate the root zone and stimulate deeper rooting."],
  ["Day 28–40", "Second drying cycle; critical for root strength and methane reduction."],
  ["7–15 Days Before Harvest", "Final drying phase improves grain quality and supports easier harvesting."]
] AS phase
MERGE (p:Stage {
  entity_id: "AWD Phase - " + phase[0],
  description: phase[1],
  source_id: "chunk-ch2-004"
})
MERGE (awd)-[:INCLUDES]->(p)

WITH awd

// --- Optional Mid-Season Application ---
MERGE (optional:Option {
  entity_id: "Mid-Season AWD (Optional)",
  description: "AWD can be applied just once between days 28–40 to reduce emissions if conditions allow.",
  source_id: "chunk-ch2-004"
})
MERGE (awd)-[:OPTIONAL_STAGE]->(optional)

WITH awd

// --- AWD Benefits ---
UNWIND [
  ["Water-Use Efficiency", "Reduces water consumption by irrigating only when needed."],
  ["Methane Reduction", "AWD helps cut methane emissions by limiting anaerobic conditions."],
  ["Nutrient Retention", "Minimizes nutrient runoff and nitrogen loss."],
  ["Stronger Root Systems", "Drying cycles promote deeper root development."],
  ["Improved Grain Quality", "Final drying improves rice grain ripening and harvest efficiency."]
] AS benefit
MERGE (b:Benefit {
  entity_id: benefit[0],
  description: benefit[1],
  source_id: "chunk-ch2-004"
})
MERGE (awd)-[:ACHIEVES]->(b)

"""