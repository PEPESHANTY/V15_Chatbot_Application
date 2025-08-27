cypher= """


// === Chapter 5: Trends and Digital Innovations in Rice Farming ===
MERGE (ch5:Chapter {
  entity_id: "Digital Innovations in Rice Farming - Ch5",
  entity_type: "chapter",
  description: "Integration of digital technologies across the rice farming value chain to enhance climate-smart practices, traceability, and emission reductions in Vietnam’s One Million Hectares Project.",
  source_id: "chunk-ch5-001"
})
WITH ch5

// === Core Technologies in Digital Agriculture ===
UNWIND [
  ["SeedCast - Ch5", "Forecasting seed demand using digital tools to match supply with regional varietal needs."],
  ["SSNM - Ch5", "Site-Specific Nutrient Management: Customized fertilizer recommendations using field-specific data and tools like AWD and RCM."],
  ["CS-MAP - Ch5", "Climate Smart Mapping and Adaptation Planning: Risk zoning, adaptation strategy development, and emission mitigation across 600,000 ha."],
  ["AWD - Ch5", "Alternate Wetting and Drying: Precision water management to cut methane emissions and conserve resources."],
  ["EasyHarvest - Ch5", "Mobile app connecting farmers to harvester services using field status and weather data for optimized harvest logistics."],
  ["IoT Drying Monitors - Ch5", "Sensor-based smart monitoring of post-harvest drying using solar and thermal data inputs."],
  ["Smart Storage Sensors - Ch5", "IoT tools to track humidity, temperature, and gas levels in sealed silos for post-harvest storage safety."],
  ["MRV System - Ch5", "Monitoring, Reporting, and Verification platform for geo-referenced tracking of emission reductions, piloted in Vietnam."],
  ["CF-Rice Tool - Ch5", "Life Cycle Assessment-based tool that calculates and labels carbon footprints for rice products."]
] AS tech
MERGE (t:Technology {
  entity_id: tech[0],
  entity_type: "technology",
  description: tech[1],
  source_id: "chunk-ch5-001"
})
MERGE (ch5)-[:HIGHLIGHTS]->(t)
WITH ch5

// === Benefits of Digital Integration ===
UNWIND [
  ["Efficiency Gains - Ch5", "Reduces input waste, manual labor, and enhances data-driven precision farming."],
  ["GHG Emissions Reduction - Ch5", "Supports emission tracking and cuts methane, nitrous oxide through optimized irrigation and nutrient management."],
  ["Market Traceability - Ch5", "Improves consumer trust and allows product labeling via digital traceability platforms."],
  ["Climate-Smart Compliance - Ch5", "Aligns production with climate-smart agriculture standards and policy initiatives."]
] AS impact
MERGE (b:Benefit {
  entity_id: impact[0],
  entity_type: "benefit",
  description: impact[1],
  source_id: "chunk-ch5-001"
})
MERGE (ch5)-[:ACHIEVES]->(b)


"""