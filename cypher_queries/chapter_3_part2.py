cypher= """

// === Chapter 3 Central Node (reuse if already created) ===
MATCH (ch3:Chapter {entity_id: "Harvesting and Post-Harvest Management - Ch3"})

// === Drying Practice Node ===
MERGE (drying:Practice {
  entity_id: "Rice Drying - Ch3",
  entity_type: "practice",
  description: "Rice must be dried within 24 hours post-harvest to prevent spoilage and ensure storage safety. Drying targets are 14% moisture for commercial rice and 13.5% for seed rice.",
  source_id: "chunk-ch3-002"
})
MERGE (ch3)-[:COVERS]->(drying)
WITH drying

// === Moisture Targets ===
MERGE (moisture_commercial:Parameter {
  entity_id: "Moisture Target for Commercial Rice - Ch3",
  entity_type: "parameter",
  description: "Target moisture content of 14% for commercial rice to ensure safe storage and quality preservation.",
  source_id: "chunk-ch3-002"
})
MERGE (moisture_seed:Parameter {
  entity_id: "Moisture Target for Seed Rice - Ch3",
  entity_type: "parameter",
  description: "Target moisture content of 13.5% for seed rice to maintain germination viability and safe storage.",
  source_id: "chunk-ch3-002"
})
MERGE (drying)-[:TARGETS]->(moisture_commercial)
MERGE (drying)-[:TARGETS]->(moisture_seed)
WITH drying

// === Static Horizontal Reversible Airflow Dryer ===
MERGE (static_dryer:Technology {
  entity_id: "Static Reversible Airflow Dryer - Ch3",
  entity_type: "technology",
  description: "Handles 4–50 tons per batch using rice husk as fuel. Offers high thermal efficiency and even air distribution. Suitable for small to medium-scale farms.",
  source_id: "chunk-ch3-002"
})
MERGE (drying)-[:USES]->(static_dryer)

MERGE (husk:Input {
  entity_id: "Rice Husk Fuel - Ch3",
  entity_type: "input",
  description: "Low-cost, sustainable fuel source used in static reversible dryers for thermal energy.",
  source_id: "chunk-ch3-002"
})
MERGE (static_dryer)-[:POWERED_BY]->(husk)

MERGE (capacity_static:Parameter {
  entity_id: "Batch Capacity - Static Dryer - Ch3",
  entity_type: "parameter",
  description: "Processes 4–50 tons per drying batch, optimized for small and medium operations.",
  source_id: "chunk-ch3-002"
})
MERGE (static_dryer)-[:CAPACITY]->(capacity_static)
WITH drying

// === Two-Stage Drying System ===
MERGE (twostage_dryer:Technology {
  entity_id: "Two-Stage Drying System - Ch3",
  entity_type: "technology",
  description: "Combines fluidized bed drying with a circulating column dryer for industrial-scale, high-throughput drying. Ensures uniformity and quality preservation.",
  source_id: "chunk-ch3-002"
})
MERGE (drying)-[:USES]->(twostage_dryer)

MERGE (fluidized:Component {
  entity_id: "Fluidized Bed Dryer - Ch3",
  entity_type: "component",
  description: "Initial stage in the two-stage system, rapidly reduces high moisture levels with heated airflow.",
  source_id: "chunk-ch3-002"
})
MERGE (column:Component {
  entity_id: "Circulating Column Dryer - Ch3",
  entity_type: "component",
  description: "Final drying stage for moisture stabilization and uniformity in industrial rice drying systems.",
  source_id: "chunk-ch3-002"
})
MERGE (twostage_dryer)-[:INCLUDES]->(fluidized)
MERGE (twostage_dryer)-[:INCLUDES]->(column)

MERGE (capacity_industrial:Parameter {
  entity_id: "Daily Capacity - Two-Stage Dryer - Ch3",
  entity_type: "parameter",
  description: "Drying capacity ranges from 200 to 1,000 tons per day, suitable for industrial-scale rice operations.",
  source_id: "chunk-ch3-002"
})
MERGE (twostage_dryer)-[:CAPACITY]->(capacity_industrial)
WITH drying

// === Energy Efficiency and Airflow Mechanism ===
MERGE (efficiency:Concept {
  entity_id: "Energy-Efficient Drying - Ch3",
  entity_type: "concept",
  description: "Diagram Hình 13 illustrates airflow systems that optimize energy use and throughput in modern dryers.",
  source_id: "chunk-ch3-002"
})
MERGE (drying)-[:ILLUSTRATED_BY]->(efficiency)
WITH drying

// === Benefits of Proper Drying ===
MERGE (preserve:Benefit {
  entity_id: "Rice Quality Preservation - Ch3",
  entity_type: "benefit",
  description: "Maintains grain structure, prevents microbial spoilage, and ensures safe storage conditions.",
  source_id: "chunk-ch3-002"
})
MERGE (drying)-[:ACHIEVES]->(preserve)

MERGE (market:Benefit {
  entity_id: "Maximized Market Value - Ch3",
  entity_type: "benefit",
  description: "Proper drying enhances visual quality and value of rice in domestic and export markets.",
  source_id: "chunk-ch3-002"
})
MERGE (drying)-[:INCREASES]->(market)

MERGE (losses:Concept {
  entity_id: "Post-Harvest Loss Reduction - Ch3",
  entity_type: "concept",
  description: "Quick and controlled drying significantly reduces post-harvest losses due to spoilage or improper storage.",
  source_id: "chunk-ch3-002"
})
MERGE (drying)-[:REDUCES]->(losses)


"""