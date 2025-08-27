cypher= """


// === Chapter 3 Central Node (reuse) ===
MATCH (ch3:Chapter {entity_id: "Harvesting and Post-Harvest Management - Ch3"})

// === Storage Practice Node ===
MERGE (storage:Practice {
  entity_id: "Rice Storage - Ch3",
  entity_type: "practice",
  description: "Proper rice storage minimizes post-harvest losses and preserves grain quality. Requires low moisture, clean grain, airtight conditions, and controlled environments.",
  source_id: "chunk-ch3-003"
})
MERGE (ch3)-[:COVERS]->(storage)
WITH storage

// === Moisture Requirements ===
MERGE (moisture_comm:Parameter {
  entity_id: "Storage Moisture Limit - Commercial Rice - Ch3",
  entity_type: "parameter",
  description: "Commercial rice must be stored at or below 14% moisture content to prevent spoilage.",
  source_id: "chunk-ch3-003"
})
MERGE (moisture_seed:Parameter {
  entity_id: "Storage Moisture Limit - Seed Rice - Ch3",
  entity_type: "parameter",
  description: "Seed rice must be stored at or below 13.5% moisture to maintain viability.",
  source_id: "chunk-ch3-003"
})
MERGE (storage)-[:REQUIRES]->(moisture_comm)
MERGE (storage)-[:REQUIRES]->(moisture_seed)

// === Grain Cleaning Requirement ===
MERGE (cleaning:Step {
  entity_id: "Grain Cleaning Before Storage - Ch3",
  entity_type: "step",
  description: "Grains must be thoroughly cleaned before storage to eliminate contaminants and reduce spoilage risk.",
  source_id: "chunk-ch3-003"
})
MERGE (storage)-[:INCLUDES]->(cleaning)

// === Storage Methods ===
MERGE (airtight:Method {
  entity_id: "Airtight Bag Storage - Ch3",
  entity_type: "method",
  description: "Use sealed bags like 50kg or 5-ton Cocoon™ bags to limit oxygen and pest intrusion.",
  source_id: "chunk-ch3-003"
})
MERGE (silo:Technology {
  entity_id: "Sealed Silo Storage - Ch3",
  entity_type: "technology",
  description: "Forced-air or cooled silos enable long-term rice storage in Mekong Delta conditions.",
  source_id: "chunk-ch3-003"
})
MERGE (automation:Technology {
  entity_id: "Digital Monitoring Systems - Ch3",
  entity_type: "technology",
  description: "Automated sensors track temperature, humidity, and gas levels to maintain storage conditions.",
  source_id: "chunk-ch3-003"
})
MERGE (storage)-[:USES]->(airtight)
MERGE (storage)-[:USES]->(silo)
MERGE (storage)-[:USES]->(automation)

// === Pest & Fumigation Guidelines ===
MERGE (fumig:Guideline {
  entity_id: "Fumigation Policy - Ch3",
  entity_type: "guideline",
  description: "Minimize use of chemical fumigants in storage. Adhere to legal pesticide residue thresholds to ensure food safety.",
  source_id: "chunk-ch3-003"
})
MERGE (storage)-[:FOLLOWS]->(fumig)

// === Storage Facility Infrastructure Guidelines ===
MERGE (pallets:Guideline {
  entity_id: "Use of Pallets - Ch3",
  entity_type: "guideline",
  description: "Store rice on wooden pallets to promote ventilation and prevent contact with ground moisture.",
  source_id: "chunk-ch3-003"
})
MERGE (walls:Guideline {
  entity_id: "Wall Gap Guideline - Ch3",
  entity_type: "guideline",
  description: "Avoid placing rice bags directly against warehouse walls to reduce heat and moisture transfer.",
  source_id: "chunk-ch3-003"
})
MERGE (stacking:Guideline {
  entity_id: "Stacking Height Limit - Ch3",
  entity_type: "guideline",
  description: "Do not exceed 2.5 meters in height to ensure airflow and prevent compaction and mold.",
  source_id: "chunk-ch3-003"
})
MERGE (vent:Concept {
  entity_id: "Warehouse Ventilation - Ch3",
  entity_type: "concept",
  description: "Proper airflow within the storage area reduces condensation and protects grain from mold and pests.",
  source_id: "chunk-ch3-003"
})
MERGE (storage)-[:COMPLIES_WITH]->(pallets)
MERGE (storage)-[:COMPLIES_WITH]->(walls)
MERGE (storage)-[:COMPLIES_WITH]->(stacking)
MERGE (storage)-[:ENHANCES]->(vent)

// === Final Benefits ===
MERGE (preservation:Benefit {
  entity_id: "Grain Quality Preservation - Ch3",
  entity_type: "benefit",
  description: "Clean, low-moisture, ventilated storage preserves rice quality over time and avoids spoilage.",
  source_id: "chunk-ch3-003"
})
MERGE (storage)-[:ACHIEVES]->(preservation)

MERGE (loss_prevent:Concept {
  entity_id: "Post-Harvest Loss Prevention - Ch3",
  entity_type: "concept",
  description: "Best storage practices reduce losses due to pests, molds, poor airflow, and chemical misuse.",
  source_id: "chunk-ch3-003"
})
MERGE (storage)-[:REDUCES]->(loss_prevent)

MERGE (safety:Concept {
  entity_id: "Food Safety Assurance - Ch3",
  entity_type: "concept",
  description: "Safe storage protects rice from chemical residues and microbial contamination, ensuring consumer safety.",
  source_id: "chunk-ch3-003"
})
MERGE (storage)-[:ENSURES]->(safety)


"""