cypher= """

// === Chapter 2 Fertilizer Management Section ===
MATCH (ch2:Chapter {entity_id: "Cultivation Techniques - Ch2"})

// --- Fertilizer Management Root Node ---
MERGE (fert:Practice {
  entity_id: "Fertilizer Management - Ch2",
  entity_type: "practice",
  source_id: "chunk-ch2-005",
  description: "Covers fertilization strategy for rice in Mekong Delta: includes SSNM, organic and inorganic inputs, mechanized methods, and soil-season-specific dosing. Optimizes root health, yield, and input efficiency."
})
MERGE (ch2)-[:COVERS]->(fert)

// --- Site-Specific Nutrient Management ---
MERGE (ssnm:Technique {
  entity_id: "Site-Specific Nutrient Management",
  entity_type: "method",
  source_id: "chunk-ch2-005",
  description: "Soil-analysis-based fertilizer strategy recalibrated every 5 years. Matches inputs to field-specific nutrient demands and cropping seasons."
})
MERGE (fert)-[:USES]->(ssnm)

// --- Organic Fertilizer ---
MERGE (organic:Input {
  entity_id: "Organic Fertilizer",
  entity_type: "input",
  source_id: "chunk-ch2-005",
  description: "Apply 1.5–3 tons/ha to improve soil microbial activity and physical structure."
})
MERGE (fert)-[:USES]->(organic)

// --- Lime Application by pH ---
MERGE (lime:Input {
  entity_id: "Lime",
  entity_type: "input",
  source_id: "chunk-ch2-005",
  description: "Neutralizes soil acidity. 200–300 kg/ha for pH 4.0–5.0; 400–500 kg/ha for pH < 4.0."
})
MERGE (fert)-[:USES]->(lime)

// --- Soil-specific Fertilizer Recommendations (Winter–Spring) ---
WITH fert
UNWIND [
  ["Alluvial Soil", 90, 100, 30, 40, 30, 40],
  ["Light Acid Sulfate Soil", 80, 100, 40, 50, 25, 30],
  ["Medium Acid Sulfate Soil", 68, 80, 50, 60, 25, 30]
] AS soil
MERGE (stype:SoilType {
  entity_id: soil[0],
  description: "Fertilizer recommendation during Winter–Spring crop in Mekong Delta.",
  source_id: "chunk-ch2-005",
  nitrogen_min: soil[1],
  nitrogen_max: soil[2],
  p2o5_min: soil[3],
  p2o5_max: soil[4],
  k2o_min: soil[5],
  k2o_max: soil[6]
})
MERGE (fert)-[:HAS_RECOMMENDATION]->(stype)

// --- Seasonal Adjustment ---
WITH fert
MERGE (adj:Guideline {
  entity_id: "Summer-Autumn Nitrogen Adjustment",
  source_id: "chunk-ch2-005",
  description: "In Summer–Autumn and Autumn–Winter, reduce nitrogen by 15–20% compared to Winter–Spring due to higher volatilization losses."
})
MERGE (fert)-[:ADJUSTS_FOR]->(adj)

// --- Fertilizer Timing: 3 stages ---
WITH fert
UNWIND [
  ["7–10 DAS", "Apply 40% of total N at 7–10 days after sowing for seedling support."],
  ["18–22 DAS", "Apply 40% N and 40% K₂O during tillering phase."],
  ["38–42 DAS", "Apply remaining 20% N and 60% K₂O to support panicle formation and grain filling."]
] AS stage
MERGE (timing:Timing {
  entity_id: "Fertilizer Timing - " + stage[0],
  description: stage[1],
  source_id: "chunk-ch2-005"
})
MERGE (fert)-[:TIMED_AT]->(timing)

// --- Mechanized Fertilization Adjustments ---
WITH fert
MERGE (mech:Guideline {
  entity_id: "Mechanized Fertilizer Management",
  source_id: "chunk-ch2-005",
  description: "When using sowing machines with fertilizer burial, reduce nitrogen by 10–15% due to improved uptake. Use slow-release granular fertilizers (2–4 mm) to prevent clogging."
})
MERGE (fert)-[:MODIFIED_BY]->(mech)

// --- Mechanized Timing: 2 stages ---
WITH fert, mech
UNWIND [
  ["At Sowing", "Apply 70–80% of total fertilizer during sowing and bury it using machines."],
  ["38–42 DAS", "Top-dress remaining fertilizer to support reproductive stage."]
] AS mstage
MERGE (mt:Timing {
  entity_id: "Mechanized Fertilizer Timing - " + mstage[0],
  description: mstage[1],
  source_id: "chunk-ch2-005"
})
MERGE (mech)-[:TIMED_AT]->(mt)

// --- Fertilizer Types Used ---
WITH fert
UNWIND [
  ["NPK", "Balanced fertilizer containing nitrogen (N), phosphorus (P), and potassium (K)."],
  ["DAP", "Diammonium phosphate — source of phosphorus and nitrogen."],
  ["KCl", "Potassium chloride — potassium source for strong stems and grains."],
  ["Urea", "High nitrogen fertilizer, used primarily during vegetative phases."]
] AS fertype
MERGE (ftype:Input {
  entity_id: fertype[0],
  description: fertype[1],
  source_id: "chunk-ch2-005"
})
MERGE (fert)-[:USES]->(ftype)

// --- Monitoring Tool ---
WITH fert
MERGE (tool:Tool {
  entity_id: "Leaf Color Chart",
  description: "Color scale used to guide nitrogen application based on leaf greenness, ensuring real-time nutrient adjustment.",
  source_id: "chunk-ch2-005"
})
MERGE (fert)-[:MONITORED_BY]->(tool)



"""