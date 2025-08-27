cypher = """
// =======================================
// Chapter 3 (Part 3) — Rice Storage Best Practices
// Single-statement, idempotent upsert with :Searchable + search_text
// =======================================

MATCH (ch3:Chapter {entity_id: 'Harvesting and Post-Harvest Management - Ch3'})

// === Storage Practice Node ===
MERGE (storage:Practice:Searchable {
  entity_id:  'Rice Storage - Ch3',
  entity_type:'practice',
  name:       'Rice Storage'
})
SET storage.chapter     = 'Ch3',
    storage.source_id   = 'chunk-ch3-003',
    storage.description = 'Proper storage minimizes post-harvest losses and preserves grain quality. Requires low moisture, clean grain, airtight/controlled conditions, and good ventilation.',
    storage.search_text = 'storage | low moisture | clean grain | airtight | sealed silo | ventilation | pallets | wall gap | stacking height | digital monitoring'
MERGE (ch3)-[:COVERS {source_id:'chunk-ch3-003'}]->(storage)

// === Moisture Requirements ===
WITH ch3, storage
MERGE (moisture_comm:Parameter:Searchable {
  entity_id:  'Storage Moisture Limit - Commercial Rice - Ch3',
  entity_type:'parameter',
  name:       'Storage Moisture Limit — Commercial Rice'
})
SET moisture_comm.chapter     = 'Ch3',
    moisture_comm.source_id   = 'chunk-ch3-003',
    moisture_comm.description = 'Commercial rice should be stored at ≤14% moisture to prevent spoilage.',
    moisture_comm.search_text = 'moisture limit | ≤14% | commercial rice | spoilage prevention'
MERGE (storage)-[:REQUIRES {source_id:'chunk-ch3-003'}]->(moisture_comm)

MERGE (moisture_seed:Parameter:Searchable {
  entity_id:  'Storage Moisture Limit - Seed Rice - Ch3',
  entity_type:'parameter',
  name:       'Storage Moisture Limit — Seed Rice'
})
SET moisture_seed.chapter     = 'Ch3',
    moisture_seed.source_id   = 'chunk-ch3-003',
    moisture_seed.description = 'Seed rice should be stored at ≤13.5% moisture to maintain viability.',
    moisture_seed.search_text = 'moisture limit | ≤13.5% | seed rice | viability'
MERGE (storage)-[:REQUIRES {source_id:'chunk-ch3-003'}]->(moisture_seed)

// === Grain Cleaning Requirement ===
WITH ch3, storage
MERGE (cleaning:Step:Searchable {
  entity_id:  'Grain Cleaning Before Storage - Ch3',
  entity_type:'step',
  name:       'Grain Cleaning Before Storage'
})
SET cleaning.chapter     = 'Ch3',
    cleaning.source_id   = 'chunk-ch3-003',
    cleaning.description = 'Thoroughly clean grains before storage to remove contaminants and reduce spoilage risk.',
    cleaning.search_text = 'cleaning | contaminants | pre-storage | spoilage reduction'
MERGE (storage)-[:INCLUDES {source_id:'chunk-ch3-003'}]->(cleaning)

// === Storage Methods & Technologies ===
WITH ch3, storage
MERGE (airtight:Method:Searchable {
  entity_id:  'Airtight Bag Storage - Ch3',
  entity_type:'method',
  name:       'Airtight Bag Storage'
})
SET airtight.chapter     = 'Ch3',
    airtight.source_id   = 'chunk-ch3-003',
    airtight.description = 'Use sealed bags (e.g., 50 kg or 5-ton Cocoon™ bags) to limit oxygen and pest intrusion.',
    airtight.search_text = 'airtight | sealed bags | 50 kg | 5-ton Cocoon | oxygen reduction | insect prevention'
MERGE (storage)-[:USES {source_id:'chunk-ch3-003'}]->(airtight)

MERGE (silo:Technology:Searchable {
  entity_id:  'Sealed Silo Storage - Ch3',
  entity_type:'technology',
  name:       'Sealed Silo Storage'
})
SET silo.chapter     = 'Ch3',
    silo.source_id   = 'chunk-ch3-003',
    silo.description = 'Forced-air or cooled silos enable long-term storage in Mekong Delta conditions.',
    silo.search_text = 'sealed silo | forced-air | cooled silo | long-term storage | ĐBSCL'
MERGE (storage)-[:USES {source_id:'chunk-ch3-003'}]->(silo)

MERGE (automation:Technology:Searchable {
  entity_id:  'Digital Monitoring Systems - Ch3',
  entity_type:'technology',
  name:       'Digital Monitoring Systems'
})
SET automation.chapter     = 'Ch3',
    automation.source_id   = 'chunk-ch3-003',
    automation.description = 'Automated sensors track temperature, humidity, and gas levels to maintain storage conditions.',
    automation.search_text = 'digital monitoring | sensors | temperature | humidity | gas | storage control'
MERGE (storage)-[:USES {source_id:'chunk-ch3-003'}]->(automation)

// === Pest & Fumigation Guidelines ===
WITH ch3, storage
MERGE (fumig:Guideline:Searchable {
  entity_id:  'Fumigation Policy - Ch3',
  entity_type:'guideline',
  name:       'Fumigation Policy'
})
SET fumig.chapter     = 'Ch3',
    fumig.source_id   = 'chunk-ch3-003',
    fumig.description = 'Minimize use of chemical fumigants; adhere to legal pesticide residue thresholds to ensure food safety.',
    fumig.search_text = 'fumigation | minimize chemicals | residue thresholds | food safety'
MERGE (storage)-[:FOLLOWS {source_id:'chunk-ch3-003'}]->(fumig)

// === Storage Facility Infrastructure Guidelines ===
WITH ch3, storage
MERGE (pallets:Guideline:Searchable {
  entity_id:  'Use of Pallets - Ch3',
  entity_type:'guideline',
  name:       'Use of Pallets'
})
SET pallets.chapter     = 'Ch3',
    pallets.source_id   = 'chunk-ch3-003',
    pallets.description = 'Store rice on wooden pallets to promote ventilation and avoid ground moisture.',
    pallets.search_text = 'pallets | off-ground | ventilation | ground moisture'
MERGE (storage)-[:COMPLIES_WITH {source_id:'chunk-ch3-003'}]->(pallets)

MERGE (walls:Guideline:Searchable {
  entity_id:  'Wall Gap Guideline - Ch3',
  entity_type:'guideline',
  name:       'Wall Gap Guideline'
})
SET walls.chapter     = 'Ch3',
    walls.source_id   = 'chunk-ch3-003',
    walls.description = 'Avoid placing rice bags directly against warehouse walls to reduce heat and moisture transfer.',
    walls.search_text = 'wall gap | heat transfer | moisture transfer | warehouse'
MERGE (storage)-[:COMPLIES_WITH {source_id:'chunk-ch3-003'}]->(walls)

MERGE (stacking:Guideline:Searchable {
  entity_id:  'Stacking Height Limit - Ch3',
  entity_type:'guideline',
  name:       'Stacking Height Limit'
})
SET stacking.chapter     = 'Ch3',
    stacking.source_id   = 'chunk-ch3-003',
    stacking.description = 'Do not exceed ~2.5 meters in height to maintain airflow and prevent compaction and mold.',
    stacking.search_text = 'stacking height | ≤2.5 m | airflow | compaction | mold'
MERGE (storage)-[:COMPLIES_WITH {source_id:'chunk-ch3-003'}]->(stacking)

MERGE (vent:Concept:Searchable {
  entity_id:  'Warehouse Ventilation - Ch3',
  entity_type:'concept',
  name:       'Warehouse Ventilation'
})
SET vent.chapter     = 'Ch3',
    vent.source_id   = 'chunk-ch3-003',
    vent.description = 'Proper airflow within storage reduces condensation and protects grain from mold and pests.',
    vent.search_text = 'ventilation | airflow | condensation | mold | pests'
MERGE (storage)-[:ENHANCES {source_id:'chunk-ch3-003'}]->(vent)

// === Final Benefits & Outcomes ===
WITH ch3, storage
MERGE (preservation:Benefit:Searchable {
  entity_id:  'Grain Quality Preservation - Ch3',
  entity_type:'benefit',
  name:       'Grain Quality Preservation'
})
SET preservation.chapter     = 'Ch3',
    preservation.source_id   = 'chunk-ch3-003',
    preservation.description = 'Clean, low-moisture, ventilated storage preserves rice quality over time and avoids spoilage.',
    preservation.search_text = 'quality preservation | low moisture | ventilation | avoid spoilage'
MERGE (storage)-[:ACHIEVES {source_id:'chunk-ch3-003'}]->(preservation)

MERGE (loss_prevent:Concept:Searchable {
  entity_id:  'Post-Harvest Loss Prevention - Ch3',
  entity_type:'concept',
  name:       'Post-Harvest Loss Prevention'
})
SET loss_prevent.chapter     = 'Ch3',
    loss_prevent.source_id   = 'chunk-ch3-003',
    loss_prevent.description = 'Best storage practices reduce losses from pests, molds, poor airflow, and chemical misuse.',
    loss_prevent.search_text = 'loss prevention | pests | mold | airflow | chemical misuse'
MERGE (storage)-[:REDUCES {source_id:'chunk-ch3-003'}]->(loss_prevent)

MERGE (safety:Concept:Searchable {
  entity_id:  'Food Safety Assurance - Ch3',
  entity_type:'concept',
  name:       'Food Safety Assurance'
})
SET safety.chapter     = 'Ch3',
    safety.source_id   = 'chunk-ch3-003',
    safety.description = 'Safe storage protects rice from residues and contamination, ensuring consumer safety.',
    safety.search_text = 'food safety | residues | contamination | consumer protection'
MERGE (storage)-[:ENSURES {source_id:'chunk-ch3-003'}]->(safety)
"""
