cypher = """
// =======================================
// Chapter 2 (Part 6) — Integrated Pest & Weed Management
// Single-statement, idempotent upsert with :Searchable + search_text
// =======================================

MATCH (ch2:Chapter {entity_id: 'Cultivation Techniques - Ch2'})

// === IPM Root Node ===
MERGE (ipm:Practice:Searchable {
  entity_id:  'Integrated Pest Management - Ch2',
  entity_type:'practice',
  name:       'Integrated Pest Management (IPM)'
})
SET ipm.chapter     = 'Ch2',
    ipm.source_id   = 'chunk-ch2-006',
    ipm.description = 'Eco-friendly, forecast- and threshold-based pest control under IPHM; prioritizes biologicals, rotation, drones, and strict pre-harvest intervals to avoid residues and resistance.',
    ipm.search_text = 'IPM | IPHM | predictive monitoring | thresholds | 4 Rights | rotate actives | withdrawal period | biological control | drones | resistance | Mekong Delta'
MERGE (ch2)-[:COVERS {source_id:'chunk-ch2-006'}]->(ipm)

// === Core IPM Principles ===
WITH ipm, ch2
UNWIND [
  {id:'Predictive Monitoring',      desc:'Early detection + action based on economic thresholds; avoids unnecessary sprays.'},
  {id:'4 Rights of Pesticide Use',  desc:'Right pesticide, right dose, right time, right method; reduces residues and resistance.'},
  {id:'Rotate Active Ingredients',  desc:'Alternate active ingredient groups to prevent resistance build-up.'},
  {id:'Pesticide Withdrawal Period',desc:'Follow pre-harvest interval (PHI) during reproductive stages to avoid harvest residues.'}
] AS principle
MERGE (p:Principle:Searchable {
  entity_id:  principle.id,
  entity_type:'principle',
  name:       principle.id
})
SET p.chapter     = 'Ch2',
    p.source_id   = 'chunk-ch2-006',
    p.description = principle.desc,
    p.search_text = principle.id+' | '+principle.desc
MERGE (ipm)-[:FOLLOWS {source_id:'chunk-ch2-006'}]->(p)

// === Spraying Thresholds ===
WITH ipm, ch2
MERGE (threshold:Guideline:Searchable {
  entity_id:  'Spraying Thresholds - Ch2',
  entity_type:'guideline',
  name:       'Spraying Thresholds'
})
SET threshold.chapter     = 'Ch2',
    threshold.source_id   = 'chunk-ch2-006',
    threshold.description = 'Spray only when disease infection >5–10% OR brown planthopper density >1,000–1,500/m² OR 2–3 insects per tiller.',
    threshold.search_text = 'thresholds | disease 5–10% | BPH 1000–1500/m² | 2–3 insects/tiller | economic threshold | avoid overuse'
MERGE (ipm)-[:TRIGGERS {source_id:'chunk-ch2-006'}]->(threshold)

// === IPM Tools & Inputs ===
WITH ipm, ch2
MERGE (bio:Input:Searchable {
  entity_id:  'Entomopathogenic Microbes',
  entity_type:'input',
  name:       'Entomopathogenic Microbes'
})
SET bio.chapter     = 'Ch2',
    bio.source_id   = 'chunk-ch2-006',
    bio.description = 'Biological agents (fungi, bacteria) for early outbreaks (e.g., brown planthopper, sheath blight).',
    bio.search_text = 'biological control | entomopathogenic fungi | bacteria | early outbreak | BPH | sheath blight'
MERGE (ipm)-[:USES {source_id:'chunk-ch2-006'}]->(bio)

WITH ipm, ch2
MERGE (drone:Tool:Searchable {
  entity_id:  'Agricultural Drone',
  entity_type:'tool',
  name:       'Agricultural Drone'
})
SET drone.chapter     = 'Ch2',
    drone.source_id   = 'chunk-ch2-006',
    drone.description = 'Precision spraying technology; reduces labor and applicator exposure and improves coverage uniformity.',
    drone.search_text = 'drone | UAV | precision spraying | safety | uniform coverage'
MERGE (ipm)-[:SUPPORTED_BY {source_id:'chunk-ch2-006'}]->(drone)

// === Major Insect Pest Control ===
WITH ipm, ch2
MERGE (insect_cat:Category:Searchable {
  entity_id:  'Insect Pests - Ch2',
  entity_type:'category',
  name:       'Insect Pests'
})
SET insect_cat.chapter     = 'Ch2',
    insect_cat.source_id   = 'chunk-ch2-006',
    insect_cat.description = 'Major insect pests targeted primarily during 35–65 days after sowing (NSS).',
    insect_cat.search_text = 'insect pests | 35–65 NSS | leaf folder | stem borer | brown planthopper'
MERGE (ipm)-[:TARGETS {source_id:'chunk-ch2-006'}]->(insect_cat)

WITH insect_cat, ipm, ch2
UNWIND [
  {id:'Leaf Folder',        desc:'Control with Chlorfluazuron + Emamectin benzoate (lepidopteran efficacy).'},
  {id:'Stem Borer',         desc:'Control with Chlorfluazuron + Emamectin benzoate (lepidopteran efficacy).'},
  {id:'Brown Planthopper',  desc:'Control with Petromethin or Diflubenzuron when thresholds are exceeded.'}
] AS pest
MERGE (p:Pest:Searchable {
  entity_id:  pest.id,
  entity_type:'pest',
  name:       pest.id
})
SET p.chapter     = 'Ch2',
    p.source_id   = 'chunk-ch2-006',
    p.description = pest.desc,
    p.search_text = pest.id+' | '+pest.desc+' | rice pest'
MERGE (insect_cat)-[:INCLUDES {source_id:'chunk-ch2-006'}]->(p)

// === Major Diseases ===
WITH ipm, ch2
MERGE (disease_cat:Category:Searchable {
  entity_id:  'Rice Diseases - Ch2',
  entity_type:'category',
  name:       'Rice Diseases'
})
SET disease_cat.chapter     = 'Ch2',
    disease_cat.source_id   = 'chunk-ch2-006',
    disease_cat.description = 'Focus 30–65 NSS; includes rice blast, sheath blight, and bacterial leaf blight.',
    disease_cat.search_text = 'diseases | 30–65 NSS | rice blast | sheath blight | bacterial leaf blight'
MERGE (ipm)-[:TARGETS {source_id:'chunk-ch2-006'}]->(disease_cat)

WITH disease_cat, ipm, ch2
UNWIND [
  {id:'Rice Blast',             desc:'Prevent/mitigate with Chitosan and Metalaxyl Propineb (biofungicides/resistance inducers).'},
  {id:'Sheath Blight',          desc:'Control with Propineb and Zinc fungicides.'},
  {id:'Bacterial Leaf Blight',  desc:'Control with Propineb and Zinc bactericides.'}
] AS disease
MERGE (d:Disease:Searchable {
  entity_id:  disease.id,
  entity_type:'disease',
  name:       disease.id
})
SET d.chapter     = 'Ch2',
    d.source_id   = 'chunk-ch2-006',
    d.description = disease.desc,
    d.search_text = disease.id+' | '+disease.desc+' | rice disease'
MERGE (disease_cat)-[:INCLUDES {source_id:'chunk-ch2-006'}]->(d)

// === Golden Apple Snail Management ===
WITH ipm, ch2
MERGE (snail:Pest:Searchable {
  entity_id:  'Golden Apple Snail',
  entity_type:'pest',
  name:       'Golden Apple Snail'
})
SET snail.chapter     = 'Ch2',
    snail.source_id   = 'chunk-ch2-006',
    snail.description = 'Seedling predator in flooded paddies; integrated control with manual, cultural, biological, and chemical methods.',
    snail.search_text = 'golden apple snail | seedling damage | integrated control | molluscicide | barriers | baits | ducks/geese'
MERGE (ipm)-[:TARGETS {source_id:'chunk-ch2-006'}]->(snail)

WITH snail, ipm, ch2
UNWIND [
  'Manual collection and burial of adults/eggs',
  'Use banana/taro/papaya leaves as bait',
  'Trap with wooden stakes or bamboo',
  'Install fine mesh at field inlets',
  'Dig trenches to concentrate snails',
  'Let ducks/geese graze in fields',
  'Use Niclosamide-based molluscicide'
] AS snail_method
MERGE (m:Technique:Searchable {
  entity_id:  'Snail Control - '+snail_method,
  entity_type:'technique',
  name:       'Snail Control: '+snail_method
})
SET m.chapter     = 'Ch2',
    m.source_id   = 'chunk-ch2-006',
    m.description = snail_method,
    m.search_text = 'snail control | '+snail_method
MERGE (snail)-[:MANAGED_BY {source_id:'chunk-ch2-006'}]->(m)

// === Field Rat Management ===
WITH ipm, ch2
MERGE (rat:Pest:Searchable {
  entity_id:  'Field Rat',
  entity_type:'pest',
  name:       'Field Rat'
})
SET rat.chapter     = 'Ch2',
    rat.source_id   = 'chunk-ch2-006',
    rat.description = 'Feeds on stems, grains, and seedlings; requires synchronized, cultural, and bait/trap controls.',
    rat.search_text = 'field rat | synchronized control | barriers | trap crop | burrow smoking | rodenticide bait'
MERGE (ipm)-[:TARGETS {source_id:'chunk-ch2-006'}]->(rat)

WITH rat, ipm, ch2
UNWIND [
  'Synchronized sowing and rat control',
  'Fencing and trap-crop systems',
  'Clearing vegetation + stubble burning',
  'Smoking burrows + manual traps',
  'Use rodenticides with food bait'
] AS rat_method
MERGE (rm:Technique:Searchable {
  entity_id:  'Rat Control - '+rat_method,
  entity_type:'technique',
  name:       'Rat Control: '+rat_method
})
SET rm.chapter     = 'Ch2',
    rm.source_id   = 'chunk-ch2-006',
    rm.description = rat_method,
    rm.search_text = 'rat control | '+rat_method
MERGE (rat)-[:MANAGED_BY {source_id:'chunk-ch2-006'}]->(rm)

// === Weed Management ===
WITH ipm, ch2
MERGE (weed:Practice:Searchable {
  entity_id:  'Weed Management - Ch2',
  entity_type:'practice',
  name:       'Weed Management'
})
SET weed.chapter     = 'Ch2',
    weed.source_id   = 'chunk-ch2-006',
    weed.description = 'Integrates pre-seeding land prep, certified seeds, herbicide rotation (pre- and post-emergence), and mechanical weeding for direct seeding systems.',
    weed.search_text = 'weed management | pre-seeding control | certified seed | herbicide rotation | pre-emergence | post-emergence | mechanical weeding'
MERGE (ch2)-[:COVERS {source_id:'chunk-ch2-006'}]->(weed)

WITH weed, ipm, ch2
UNWIND [
  {chem:'Pretilachlor',          desc:'Pre-emergence herbicide for early-stage weed suppression.'},
  {chem:'Butachlor',             desc:'Pre-emergence herbicide targeting germinating weed seeds.'},
  {chem:'Bispyribac sodium',     desc:'Post-emergence herbicide for grassy and broadleaf weeds.'},
  {chem:'Pyrazosulfuron ethyl',  desc:'Post-emergence selective weed control (ALS inhibitor).'}
] AS herb
MERGE (h:Chemical:Searchable {
  entity_id:  herb.chem,
  entity_type:'chemical',
  name:       herb.chem
})
SET h.chapter     = 'Ch2',
    h.source_id   = 'chunk-ch2-006',
    h.description = herb.desc,
    h.search_text = herb.chem+' | '+herb.desc+' | herbicide'
MERGE (weed)-[:USES {source_id:'chunk-ch2-006'}]->(h)

WITH weed, ipm, ch2
MERGE (weeder:Tool:Searchable {
  entity_id:  'Mechanical Weeder',
  entity_type:'tool',
  name:       'Mechanical Weeder'
})
SET weeder.chapter     = 'Ch2',
    weeder.source_id   = 'chunk-ch2-006',
    weeder.description = 'Used in direct seeding (cluster/row) systems to suppress weeds and aerate soil; reduces chemical reliance.',
    weeder.search_text = 'mechanical weeder | direct seeding | row/cluster | soil aeration | reduce herbicides'
MERGE (weed)-[:SUPPORTED_BY {source_id:'chunk-ch2-006'}]->(weeder)
"""
