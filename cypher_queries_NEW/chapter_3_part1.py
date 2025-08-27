cypher = """
// =======================================
// Chapter 3 (Part 1) — Harvesting & Post-Harvest Overview
// Single-statement, idempotent upsert with :Searchable + search_text
// =======================================

// === Chapter 3 Central Node ===
MERGE (ch3:Chapter:Searchable {
  entity_id:  'Harvesting and Post-Harvest Management - Ch3',
  entity_type:'chapter',
  name:       'Chapter 3 — Harvesting & Post-Harvest Management'
})
SET ch3.chapter     = 'Ch3',
    ch3.file_path   = 'book_1.pdf',
    ch3.source_id   = 'chunk-ch3-001',
    ch3.created_at  = coalesce(ch3.created_at, timestamp()),
    ch3.summary     = 'Chapter 3 focuses on timely harvesting and post-harvest handling (threshing, drying, storage, milling) to reduce losses, keep quality, and sustain market value.',
    ch3.description = 'Emphasizes harvesting at 85–90% golden grains, mechanized combine harvesting, rapid energy-efficient drying (incl. solar), sealed storage (silos/containers), and proper milling. Notes >10% GHG reduction and higher farmer income with improved post-harvest practices.',
    ch3.search_text = 'Chapter 3 | harvesting | post-harvest | threshing | drying | storage | milling | 85–90% golden grains | combine harvester | energy-efficient drying | solar drying | sealed storage | silos | EasyHarvest | loss reduction | GHG reduction'

// === Main Harvesting Practice ===
WITH ch3
MERGE (harvest:Practice:Searchable {
  entity_id:  'Harvesting - Ch3',
  entity_type:'practice',
  name:       'Harvesting'
})
SET harvest.chapter     = 'Ch3',
    harvest.source_id   = 'chunk-ch3-001',
    harvest.description = 'Critical phase executed when ~85–90% of grains are golden/straw-colored to maximize yield and quality; delays cause shattering and pest losses.',
    harvest.search_text = 'harvest | 85–90% golden grains | optimal harvest time | shattering loss | pest loss | mechanization | combine'
MERGE (ch3)-[:COVERS {source_id:'chunk-ch3-001'}]->(harvest)

// === Optimal Timing Parameter ===
WITH ch3, harvest
MERGE (timing:Parameter:Searchable {
  entity_id:  'Optimal Harvest Timing - Ch3',
  entity_type:'parameter',
  name:       'Optimal Harvest Timing'
})
SET timing.chapter     = 'Ch3',
    timing.source_id   = 'chunk-ch3-001',
    timing.description = 'Harvest when approximately 85–90% of grains have turned golden/straw-colored (full physiological maturity, maximum grain weight and quality).',
    timing.search_text = 'optimal timing | 85–90% golden | maturity | grain weight | grain quality'
MERGE (harvest)-[:REQUIRES {source_id:'chunk-ch3-001'}]->(timing)

// === Combine Harvester Technology ===
WITH ch3, harvest
MERGE (combine:Technology:Searchable {
  entity_id:  'Combine Harvester - Ch3',
  entity_type:'technology',
  name:       'Combine Harvester'
})
SET combine.chapter     = 'Ch3',
    combine.source_id   = 'chunk-ch3-001',
    combine.description = 'Performs cutting, threshing, cleaning, and bagging in one pass; boosts timeliness and reduces labor and losses versus manual methods.',
    combine.search_text = 'combine harvester | cut | thresh | clean | bag | timeliness | labor | loss reduction'
MERGE (harvest)-[:USES {source_id:'chunk-ch3-001'}]->(combine)

// === Mechanization Benefit ===
WITH ch3, harvest, combine
MERGE (mech:Concept:Searchable {
  entity_id:  'Mechanized Harvesting Efficiency - Ch3',
  entity_type:'concept',
  name:       'Mechanized Harvesting Efficiency'
})
SET mech.chapter     = 'Ch3',
    mech.source_id   = 'chunk-ch3-001',
    mech.description = 'Mechanized harvesting improves timeliness, reduces grain loss, and enables rapid field turnover in multi-season systems.',
    mech.search_text = 'mechanization | timeliness | field turnover | loss reduction | multi-season'
MERGE (combine)-[:IMPROVES {source_id:'chunk-ch3-001'}]->(mech)
MERGE (harvest)-[:ENHANCES {source_id:'chunk-ch3-001'}]->(mech)

// === Post-Harvest Loss Reduction ===
WITH ch3, harvest
MERGE (loss:Concept:Searchable {
  entity_id:  'Post-Harvest Loss Reduction - Ch3',
  entity_type:'concept',
  name:       'Post-Harvest Loss Reduction'
})
SET loss.chapter     = 'Ch3',
    loss.source_id   = 'chunk-ch3-001',
    loss.description = 'Timely, mechanized harvest and proper handling reduce losses from shattering, pests, delays, and inefficient manual practices.',
    loss.search_text = 'loss reduction | shattering | pests | delays | manual vs mechanized'
MERGE (harvest)-[:REDUCES {source_id:'chunk-ch3-001'}]->(loss)

// === Sustainability Outcome ===
WITH ch3, harvest
MERGE (sustain:Concept:Searchable {
  entity_id:  'Sustainability Gains - Ch3',
  entity_type:'concept',
  name:       'Sustainability Gains'
})
SET sustain.chapter     = 'Ch3',
    sustain.source_id   = 'chunk-ch3-001',
    sustain.description = 'Improved harvest and post-harvest practices can lower GHG emissions by >10% and raise farmer income, supporting sustainable rice value chains.',
    sustain.search_text = 'sustainability | GHG reduction >10% | income | value chain'
MERGE (harvest)-[:CONTRIBUTES_TO {source_id:'chunk-ch3-001'}]->(sustain)

// === Post-Harvest Chain: Drying → Storage → Milling ===
WITH ch3, harvest
MERGE (drying:Process:Searchable {
  entity_id:  'Drying - Ch3',
  entity_type:'process',
  name:       'Grain Drying'
})
SET drying.chapter     = 'Ch3',
    drying.source_id   = 'chunk-ch3-001',
    drying.description = 'Rapid, energy-efficient multi-stage drying (incl. solar options) to lower moisture without damaging grain structure.',
    drying.search_text = 'drying | multi-stage | energy-efficient | solar drying | moisture reduction | quality preservation'
MERGE (ch3)-[:COVERS {source_id:'chunk-ch3-001'}]->(drying)
MERGE (harvest)-[:FEEDS_INTO {source_id:'chunk-ch3-001'}]->(drying)

WITH ch3, drying
MERGE (storage:Process:Searchable {
  entity_id:  'Storage - Ch3',
  entity_type:'process',
  name:       'Storage'
})
SET storage.chapter     = 'Ch3',
    storage.source_id   = 'chunk-ch3-001',
    storage.description = 'Sealed, moisture-proof containers/silos or industrial storage to prevent pests, molds, and environmental spoilage.',
    storage.search_text = 'storage | sealed | moisture-proof | silos | pest/mold prevention | shelf life'
MERGE (ch3)-[:COVERS {source_id:'chunk-ch3-001'}]->(storage)
MERGE (drying)-[:FEEDS_INTO {source_id:'chunk-ch3-001'}]->(storage)

WITH ch3, drying, storage
MERGE (milling:Process:Searchable {
  entity_id:  'Milling - Ch3',
  entity_type:'process',
  name:       'Milling'
})
SET milling.chapter     = 'Ch3',
    milling.source_id   = 'chunk-ch3-001',
    milling.description = 'Processes dried, stored paddy into market-ready rice while preserving quality and value.',
    milling.search_text = 'milling | post-harvest processing | market-ready | quality retention'
MERGE (ch3)-[:COVERS {source_id:'chunk-ch3-001'}]->(milling)
MERGE (storage)-[:FEEDS_INTO {source_id:'chunk-ch3-001'}]->(milling)

// === Smart Post-Harvest Tool (EasyHarvest) ===
WITH ch3, drying, storage, milling
MERGE (easy:Tool:Searchable {
  entity_id:  'EasyHarvest - Ch3',
  entity_type:'tool',
  name:       'EasyHarvest'
})
SET easy.chapter     = 'Ch3',
    easy.source_id   = 'chunk-ch3-001',
    easy.description = 'Smart tool referenced for optimizing drying, storage, and milling workflows to reduce losses and maintain quality.',
    easy.search_text = 'EasyHarvest | smart post-harvest | optimize drying | storage | milling | loss reduction | quality'
MERGE (easy)-[:OPTIMIZES {source_id:'chunk-ch3-001'}]->(drying)
MERGE (easy)-[:OPTIMIZES {source_id:'chunk-ch3-001'}]->(storage)
MERGE (easy)-[:OPTIMIZES {source_id:'chunk-ch3-001'}]->(milling)
"""
