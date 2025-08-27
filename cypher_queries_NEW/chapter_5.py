cypher = """
// ================================================
// Chapter 5: Trends and Digital Innovations in Rice
// ================================================
MERGE (ch5:Chapter:Searchable {
  entity_id:  'Digital Innovations in Rice Farming - Ch5',
  entity_type:'chapter',
  name:       'Digital Innovations in Rice Farming'
})
SET ch5.source_id   = 'chunk-ch5-001',
    ch5.description = 'Integration of digital technologies across the rice farming value chain to enhance climate-smart practices, traceability, and emission reductions in Vietnam’s One Million Hectares Project.',
    ch5.chapter     = 'Ch5',
    ch5.search_text = 'Chapter 5 | digital agriculture | rice | SeedCast | SSNM | CS-MAP | AWD | EasyHarvest | IoT drying | smart storage | MRV | CF-Rice | traceability | emissions'
WITH ch5

// === Core Technologies in Digital Agriculture ===
UNWIND [
  ['SeedCast - Ch5',           'Forecasting seed demand using digital tools to match supply with regional varietal needs.'],
  ['SSNM - Ch5',               'Site-Specific Nutrient Management: Customized fertilizer recommendations using field-specific data and tools like AWD and RCM.'],
  ['CS-MAP - Ch5',             'Climate Smart Mapping and Adaptation Planning: Risk zoning, adaptation strategy development, and emission mitigation across 600,000 ha.'],
  ['AWD - Ch5',                'Alternate Wetting and Drying: Precision water management to cut methane emissions and conserve resources.'],
  ['EasyHarvest - Ch5',        'Mobile app connecting farmers to harvester services using field status and weather data for optimized harvest logistics.'],
  ['IoT Drying Monitors - Ch5','Sensor-based smart monitoring of post-harvest drying using solar and thermal data inputs.'],
  ['Smart Storage Sensors - Ch5','IoT tools to track humidity, temperature, and gas levels in sealed silos for post-harvest storage safety.'],
  ['MRV System - Ch5',         'Monitoring, Reporting, and Verification platform for geo-referenced tracking of emission reductions, piloted in Vietnam.'],
  ['CF-Rice Tool - Ch5',       'Life Cycle Assessment-based tool that calculates and labels carbon footprints for rice products.']
] AS tech
MERGE (t:Technology:Searchable {
  entity_id:  tech[0],
  entity_type:'technology',
  name:       tech[0]
})
SET t.source_id   = 'chunk-ch5-001',
    t.description = tech[1],
    t.chapter     = 'Ch5',
    t.search_text = 'digital ag | technology | ' + tech[0] + ' | ' + tech[1]
MERGE (ch5)-[:HIGHLIGHTS {source_id:'chunk-ch5-001'}]->(t)
WITH ch5

// === Benefits of Digital Integration ===
UNWIND [
  ['Efficiency Gains - Ch5',        'Reduces input waste, manual labor, and enhances data-driven precision farming.'],
  ['GHG Emissions Reduction - Ch5', 'Supports emission tracking and cuts methane, nitrous oxide through optimized irrigation and nutrient management.'],
  ['Market Traceability - Ch5',     'Improves consumer trust and allows product labeling via digital traceability platforms.'],
  ['Climate-Smart Compliance - Ch5','Aligns production with climate-smart agriculture standards and policy initiatives.']
] AS impact
MERGE (b:Benefit:Searchable {
  entity_id:  impact[0],
  entity_type:'benefit',
  name:       impact[0]
})
SET b.source_id   = 'chunk-ch5-001',
    b.description = impact[1],
    b.chapter     = 'Ch5',
    b.search_text = 'benefit | digital | ' + impact[0] + ' | ' + impact[1]
MERGE (ch5)-[:ACHIEVES {source_id:'chunk-ch5-001'}]->(b)
"""
