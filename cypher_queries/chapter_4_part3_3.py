cypher= """


// === Chapter 4 – Part 3.3: Animal Feed for Buffaloes and Cows ===
MERGE (feed:Practice {
  entity_id: "Fermented Straw Feed for Cattle - Ch4",
  entity_type: "practice",
  description: "Fermenting rice straw to produce nutritious, low-cost feed for buffaloes and cows. Enhances digestibility, prevents waste, and supports circular livestock farming.",
  source_id: "chunk-ch4-003"
})
WITH feed

MATCH (ch4:Chapter {entity_id: "Straw Management - Ch4"})
MERGE (ch4)-[:COVERS]->(feed)
WITH feed

MERGE (input:Input {
  entity_id: "GAP-Compliant Rice Straw - Ch4",
  entity_type: "input",
  description: "Rice straw sourced from Good Agricultural Practice (GAP) fields, free from pesticide or microbial contamination.",
  source_id: "chunk-ch4-003"
})
MERGE (feed)-[:REQUIRES]->(input)
WITH feed

UNWIND [
  ["Dry Straw - Ch4", "Moisture <18%. Can be stored for up to 6 months before processing."],
  ["Wet Straw - Ch4", "Moisture >18%. Must be fermented immediately to avoid spoilage."]
] AS type
MERGE (cond:Condition {
  entity_id: type[0],
  entity_type: "condition",
  description: type[1],
  source_id: "chunk-ch4-003"
})
MERGE (feed)-[:USES]->(cond)
WITH feed

UNWIND [
  ["Lime-Urea Treatment - Ch4", "2 kg powdered lime + 2 kg urea mixed with 50–80 L water per 100 kg straw."],
  ["Enzyme-Salt Treatment - Ch4", "0.1 kg microbial enzyme + 0.1 kg salt mixed with 50–80 L water per 100 kg straw."]
] AS method
MERGE (treat:Method {
  entity_id: method[0],
  entity_type: "method",
  description: method[1],
  source_id: "chunk-ch4-003"
})
MERGE (feed)-[:TREATED_WITH]->(treat)
WITH feed

UNWIND [
  ["Nylon Bag Fermentation - Ch4", "Tightly sealed 16–20 kg straw bags, fermented for 7 days."],
  ["Pit Fermentation - Ch4", "Straw compacted in pits, anaerobically fermented."]
] AS ferment
MERGE (step:Step {
  entity_id: ferment[0],
  entity_type: "step",
  description: ferment[1],
  source_id: "chunk-ch4-003"
})
MERGE (feed)-[:INCLUDES]->(step)
WITH feed

MERGE (safe:Guideline {
  entity_id: "Fermentation Quality Control - Ch4",
  entity_type: "guideline",
  description: "Avoid contamination and mold by ensuring correct moisture levels and airtight sealing.",
  source_id: "chunk-ch4-003"
})
MERGE (feed)-[:FOLLOWS]->(safe)
WITH feed

MERGE (intake:Parameter {
  entity_id: "Daily Intake for Cattle - Ch4",
  entity_type: "parameter",
  description: "Each buffalo or cow can consume 2–7 kg of fermented straw per day depending on age and weight.",
  source_id: "chunk-ch4-003"
})
MERGE (feed)-[:RECOMMENDS]->(intake)
WITH feed

MERGE (value:Benefit {
  entity_id: "Circular Livestock Feed Value - Ch4",
  entity_type: "benefit",
  description: "Transforms agricultural waste into value-added livestock feed, reducing costs and enhancing sustainability.",
  source_id: "chunk-ch4-003"
})
MERGE (feed)-[:ACHIEVES]->(value)


"""