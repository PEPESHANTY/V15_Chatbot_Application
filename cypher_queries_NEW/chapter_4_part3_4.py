cypher = """
// ===============================================
// Chapter 4 — Part 3.4: Biological Straw Bedding
// ===============================================

// Root practice
MERGE (biobed:Practice:Searchable {
  entity_id:  'Biological Straw Bedding - Ch4',
  entity_type:'practice',
  name:       'Biological Straw Bedding'
})
SET biobed.chapter     = 'Ch4',
    biobed.source_id   = 'chunk-ch4-003',
    biobed.description = 'Using dry rice straw mixed with microbial inoculants and manure to create biological bedding for buffaloes and cows. Enhances hygiene and is recyclable into organic fertilizer.',
    biobed.search_text = 'biological bedding | straw bedding | GAP straw | microbial inoculant | manure | 20–30 cm layer | 50:50 mix | buffalo | cow | compost'
WITH biobed

// Link to Chapter 4
MATCH (ch4:Chapter {entity_id:'Straw Management - Ch4'})
MERGE (ch4)-[:COVERS {source_id:'chunk-ch4-003'}]->(biobed)
WITH biobed

// Required input: GAP-compliant dry straw
MERGE (straw:Input:Searchable {
  entity_id:  'Dry GAP Straw - Ch4',
  entity_type:'input',
  name:       'Dry GAP Straw'
})
SET straw.chapter     = 'Ch4',
    straw.source_id   = 'chunk-ch4-003',
    straw.description = 'Straw collected from GAP-managed fields; moisture <18% to resist mold and allow easier storage and handling.',
    straw.search_text = 'dry straw <18% moisture | GAP | clean straw | low mold risk | storage ready'
MERGE (biobed)-[:REQUIRES {source_id:'chunk-ch4-003'}]->(straw)
WITH biobed

// Additional components (inputs)
UNWIND [
  ['Microbial Inoculant - Ch4',       'Biological agents added to bedding to enhance microbial activity and decomposition.'],
  ['Cattle or Buffalo Manure - Ch4',  'Animal waste added to bedding to improve microbial fermentation and nutrient content.']
] AS comp
MERGE (c:Input:Searchable {
  entity_id:  comp[0],
  entity_type:'input',
  name:       comp[0]
})
SET c.chapter     = 'Ch4',
    c.source_id   = 'chunk-ch4-003',
    c.description = comp[1],
    c.search_text = 'bedding component | ' + comp[0] + ' | ' + comp[1]
MERGE (biobed)-[:COMBINED_WITH {source_id:'chunk-ch4-003'}]->(c)
WITH biobed

// Application step
MERGE (setup:Step:Searchable {
  entity_id:  'Bedding Preparation and Use - Ch4',
  entity_type:'step',
  name:       'Bedding Preparation and Use'
})
SET setup.chapter     = 'Ch4',
    setup.source_id   = 'chunk-ch4-003',
    setup.description = 'Shred straw; mix ~50% straw with ~50% organic matter (e.g., manure) and microbial inoculants. Apply in 20–30 cm layers across barn floors.',
    setup.search_text = 'prepare bedding | 50:50 straw-organic ratio | 20–30 cm layer | barn application | microbial inoculant'
MERGE (biobed)-[:HAS_STEP {source_id:'chunk-ch4-003'}]->(setup)
WITH biobed

// Benefit
MERGE (benefit1:Benefit:Searchable {
  entity_id:  'Improved Hygiene and Comfort - Ch4',
  entity_type:'benefit',
  name:       'Improved Hygiene and Comfort'
})
SET benefit1.chapter     = 'Ch4',
    benefit1.source_id   = 'chunk-ch4-003',
    benefit1.description = 'Biological bedding absorbs moisture, reduces odor, and improves animal comfort and health.',
    benefit1.search_text = 'hygiene | comfort | odor reduction | moisture absorption | animal health'
MERGE (biobed)-[:ACHIEVES {source_id:'chunk-ch4-003'}]->(benefit1)
WITH biobed

// Output
MERGE (output:Output:Searchable {
  entity_id:  'Organic Fertilizer from Biobed - Ch4',
  entity_type:'output',
  name:       'Organic Fertilizer from Biobed'
})
SET output.chapter     = 'Ch4',
    output.source_id   = 'chunk-ch4-003',
    output.description = 'After use, nutrient-rich bedding is composted into organic fertilizer, supporting circular agriculture.',
    output.search_text = 'compost | organic fertilizer | recycled bedding | circular agriculture'
MERGE (biobed)-[:PRODUCES {source_id:'chunk-ch4-003'}]->(output)
"""
