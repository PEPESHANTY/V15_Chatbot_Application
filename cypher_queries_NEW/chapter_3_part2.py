cypher = """
// =======================================
// Chapter 3 (Part 2) — Rice Drying
// Single-statement, idempotent upsert with :Searchable + search_text
// =======================================

MATCH (ch3:Chapter {entity_id: 'Harvesting and Post-Harvest Management - Ch3'})

// === Drying Practice Node ===
MERGE (drying:Practice:Searchable {
  entity_id:  'Rice Drying - Ch3',
  entity_type:'practice',
  name:       'Rice Drying'
})
SET drying.chapter     = 'Ch3',
    drying.source_id   = 'chunk-ch3-002',
    drying.description = 'Rice must be dried within 24 hours post-harvest to prevent spoilage and ensure storage safety. Targets: 14% moisture (commercial) and 13.5% (seed).',
    drying.search_text = 'drying | within 24 hours | moisture target | 14% commercial | 13.5% seed | spoilage prevention | safe storage'
MERGE (ch3)-[:COVERS {source_id:'chunk-ch3-002'}]->(drying)

// === Moisture Targets ===
WITH ch3, drying
MERGE (moisture_commercial:Parameter:Searchable {
  entity_id:  'Moisture Target for Commercial Rice - Ch3',
  entity_type:'parameter',
  name:       'Moisture Target — Commercial Rice'
})
SET moisture_commercial.chapter     = 'Ch3',
    moisture_commercial.source_id   = 'chunk-ch3-002',
    moisture_commercial.description = 'Target moisture content of 14% for commercial rice to ensure safe storage and quality preservation.',
    moisture_commercial.search_text = 'moisture 14% | commercial rice | storage safety | quality'
MERGE (drying)-[:TARGETS {source_id:'chunk-ch3-002'}]->(moisture_commercial)

MERGE (moisture_seed:Parameter:Searchable {
  entity_id:  'Moisture Target for Seed Rice - Ch3',
  entity_type:'parameter',
  name:       'Moisture Target — Seed Rice'
})
SET moisture_seed.chapter     = 'Ch3',
    moisture_seed.source_id   = 'chunk-ch3-002',
    moisture_seed.description = 'Target moisture content of 13.5% for seed rice to maintain germination viability and safe storage.',
    moisture_seed.search_text = 'moisture 13.5% | seed rice | germination | storage safety'
MERGE (drying)-[:TARGETS {source_id:'chunk-ch3-002'}]->(moisture_seed)

// === Static Horizontal Reversible Airflow Dryer ===
WITH ch3, drying
MERGE (static_dryer:Technology:Searchable {
  entity_id:  'Static Reversible Airflow Dryer - Ch3',
  entity_type:'technology',
  name:       'Static Reversible Airflow Dryer'
})
SET static_dryer.chapter     = 'Ch3',
    static_dryer.source_id   = 'chunk-ch3-002',
    static_dryer.description = 'Handles ~4–50 tons per batch; uses rice husk as fuel. High thermal efficiency and even air distribution; suitable for small/medium farms.',
    static_dryer.search_text = 'static dryer | reversible airflow | 4–50 tons/batch | rice husk fuel | thermal efficiency | even airflow | small/medium scale'
MERGE (drying)-[:USES {source_id:'chunk-ch3-002'}]->(static_dryer)

MERGE (husk:Input:Searchable {
  entity_id:  'Rice Husk Fuel - Ch3',
  entity_type:'input',
  name:       'Rice Husk Fuel'
})
SET husk.chapter     = 'Ch3',
    husk.source_id   = 'chunk-ch3-002',
    husk.description = 'Low-cost, sustainable fuel source used by static reversible dryers for thermal energy.',
    husk.search_text = 'rice husk | fuel | sustainable | thermal energy'
MERGE (static_dryer)-[:POWERED_BY {source_id:'chunk-ch3-002'}]->(husk)

MERGE (capacity_static:Parameter:Searchable {
  entity_id:  'Batch Capacity - Static Dryer - Ch3',
  entity_type:'parameter',
  name:       'Batch Capacity — Static Dryer'
})
SET capacity_static.chapter     = 'Ch3',
    capacity_static.source_id   = 'chunk-ch3-002',
    capacity_static.description = 'Processes approximately 4–50 tons per drying batch; optimized for small and medium operations.',
    capacity_static.search_text = 'capacity | 4–50 tons | batch | static dryer'
MERGE (static_dryer)-[:CAPACITY {source_id:'chunk-ch3-002'}]->(capacity_static)

// === Two-Stage Drying System ===
WITH ch3, drying
MERGE (twostage_dryer:Technology:Searchable {
  entity_id:  'Two-Stage Drying System - Ch3',
  entity_type:'technology',
  name:       'Two-Stage Drying System'
})
SET twostage_dryer.chapter     = 'Ch3',
    twostage_dryer.source_id   = 'chunk-ch3-002',
    twostage_dryer.description = 'Combines fluidized bed drying with a circulating column dryer for high-throughput, industrial-scale drying with uniform quality.',
    twostage_dryer.search_text = 'two-stage drying | fluidized bed | circulating column dryer | industrial scale | uniform quality'
MERGE (drying)-[:USES {source_id:'chunk-ch3-002'}]->(twostage_dryer)

MERGE (fluidized:Component:Searchable {
  entity_id:  'Fluidized Bed Dryer - Ch3',
  entity_type:'component',
  name:       'Fluidized Bed Dryer'
})
SET fluidized.chapter     = 'Ch3',
    fluidized.source_id   = 'chunk-ch3-002',
    fluidized.description = 'Initial stage rapidly reduces high moisture using heated airflow.',
    fluidized.search_text = 'fluidized bed | initial stage | rapid moisture reduction'
MERGE (twostage_dryer)-[:INCLUDES {source_id:'chunk-ch3-002'}]->(fluidized)

MERGE (column:Component:Searchable {
  entity_id:  'Circulating Column Dryer - Ch3',
  entity_type:'component',
  name:       'Circulating Column Dryer'
})
SET column.chapter     = 'Ch3',
    column.source_id   = 'chunk-ch3-002',
    column.description = 'Final stage stabilizes moisture and improves uniformity in industrial rice drying.',
    column.search_text = 'circulating column dryer | final stage | stabilization | uniformity'
MERGE (twostage_dryer)-[:INCLUDES {source_id:'chunk-ch3-002'}]->(column)

MERGE (capacity_industrial:Parameter:Searchable {
  entity_id:  'Daily Capacity - Two-Stage Dryer - Ch3',
  entity_type:'parameter',
  name:       'Daily Capacity — Two-Stage Dryer'
})
SET capacity_industrial.chapter     = 'Ch3',
    capacity_industrial.source_id   = 'chunk-ch3-002',
    capacity_industrial.description = 'Industrial-scale drying capacity ~200–1,000 tons per day.',
    capacity_industrial.search_text = 'capacity | 200–1000 tons/day | industrial scale'
MERGE (twostage_dryer)-[:CAPACITY {source_id:'chunk-ch3-002'}]->(capacity_industrial)

// === Energy Efficiency and Airflow Mechanism ===
WITH ch3, drying
MERGE (efficiency:Concept:Searchable {
  entity_id:  'Energy-Efficient Drying - Ch3',
  entity_type:'concept',
  name:       'Energy-Efficient Drying'
})
SET efficiency.chapter     = 'Ch3',
    efficiency.source_id   = 'chunk-ch3-002',
    efficiency.description = 'Airflow system designs (e.g., Hình 13) that optimize energy use and throughput in modern dryers.',
    efficiency.search_text = 'energy efficiency | airflow | dryer design | throughput'
MERGE (drying)-[:ILLUSTRATED_BY {source_id:'chunk-ch3-002'}]->(efficiency)

// === Benefits of Proper Drying ===
WITH ch3, drying
MERGE (preserve:Benefit:Searchable {
  entity_id:  'Rice Quality Preservation - Ch3',
  entity_type:'benefit',
  name:       'Rice Quality Preservation'
})
SET preserve.chapter     = 'Ch3',
    preserve.source_id   = 'chunk-ch3-002',
    preserve.description = 'Maintains grain structure, prevents microbial spoilage, and ensures safe storage conditions.',
    preserve.search_text = 'quality preservation | grain structure | microbial spoilage | safe storage'
MERGE (drying)-[:ACHIEVES {source_id:'chunk-ch3-002'}]->(preserve)

MERGE (market:Benefit:Searchable {
  entity_id:  'Maximized Market Value - Ch3',
  entity_type:'benefit',
  name:       'Maximized Market Value'
})
SET market.chapter     = 'Ch3',
    market.source_id   = 'chunk-ch3-002',
    market.description = 'Proper drying enhances visual quality and market value for domestic and export markets.',
    market.search_text = 'market value | visual quality | domestic | export'
MERGE (drying)-[:INCREASES {source_id:'chunk-ch3-002'}]->(market)

MERGE (losses:Concept:Searchable {
  entity_id:  'Post-Harvest Loss Reduction - Ch3',
  entity_type:'concept',
  name:       'Post-Harvest Loss Reduction'
})
SET losses.chapter     = 'Ch3',
    losses.source_id   = 'chunk-ch3-002',
    losses.description = 'Quick, controlled drying reduces post-harvest losses due to spoilage or improper storage.',
    losses.search_text = 'loss reduction | spoilage | improper storage | drying speed | control'
MERGE (drying)-[:REDUCES {source_id:'chunk-ch3-002'}]->(losses)
"""
