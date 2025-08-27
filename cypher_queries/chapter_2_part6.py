cypher= """

// === Chapter 2: Integrated Pest and Weed Management ===
MATCH (ch2:Chapter {entity_id: "Cultivation Techniques - Ch2"})

// === IPM Root Node ===
MERGE (ipm:Practice {
  entity_id: "Integrated Pest Management - Ch2",
  entity_type: "practice",
  source_id: "chunk-ch2-006",
  description: "Eco-friendly, forecast-based pest control within Integrated Plant Health Management (IPHM); prioritizes biologicals, thresholds, drones, and rotation to combat resistance."
})
MERGE (ch2)-[:COVERS]->(ipm)
WITH ch2, ipm

// === Core IPM Principles ===
WITH ch2, ipm
UNWIND [
  ["Predictive Monitoring", "Early detection and action based on pest thresholds; avoids overuse."],
  ["4 Rights of Pesticide Use", "Right pesticide, dose, time, method. Avoids resistance and residues."],
  ["Rotate Active Ingredients", "Alternate active compounds to prevent pest resistance."],
  ["Pesticide Withdrawal Period", "Follow pre-harvest interval during reproduction to avoid residues."]
] AS principle
MERGE (p:Principle {
  entity_id: principle[0],
  description: principle[1],
  source_id: "chunk-ch2-006"
})
MERGE (ipm)-[:FOLLOWS]->(p)
WITH ch2, ipm

// === Spraying Thresholds ===
MERGE (threshold:Guideline {
  entity_id: "Spraying Thresholds - Ch2",
  description: "Only spray if disease infection >5–10% or brown planthoppers >1000–1500/m² or 2–3 insects per tiller.",
  source_id: "chunk-ch2-006"
})
MERGE (ipm)-[:TRIGGERS]->(threshold)
WITH ch2, ipm

// === IPM Tools & Inputs ===
MERGE (bio:Input {
  entity_id: "Entomopathogenic Microbes",
  description: "Microbial agents (fungi, bacteria) used in early outbreaks of pests like brown planthopper and sheath blight.",
  source_id: "chunk-ch2-006"
})
MERGE (ipm)-[:USES]->(bio)

MERGE (drone:Tool {
  entity_id: "Agricultural Drone",
  description: "Technology for precise pesticide spraying, reduces labor and exposure.",
  source_id: "chunk-ch2-006"
})
MERGE (ipm)-[:SUPPORTED_BY]->(drone)
WITH ch2, ipm

// === Major Insect Pest Control ===
MERGE (insect_cat:Category {
  entity_id: "Insect Pests - Ch2",
  description: "Major pests targeted between 35–65 days after sowing (NSS).",
  source_id: "chunk-ch2-006"
})
MERGE (ipm)-[:TARGETS]->(insect_cat)
WITH ch2, ipm, insect_cat
UNWIND [
  ["Leaf Folder", "Controlled with Chlorfluazuron + Emamectin benzoate"],
  ["Stem Borer", "Controlled with Chlorfluazuron + Emamectin benzoate"],
  ["Brown Planthopper", "Controlled with Petromethin or Diflubenzuron"]
] AS pest
MERGE (p:Pest {
  entity_id: pest[0],
  description: pest[1],
  source_id: "chunk-ch2-006"
})
MERGE (insect_cat)-[:INCLUDES]->(p)
WITH ch2, ipm

// === Major Diseases ===
MERGE (disease_cat:Category {
  entity_id: "Rice Diseases - Ch2",
  description: "Includes rice blast, sheath blight, and bacterial leaf blight. Focus between 30–65 NSS.",
  source_id: "chunk-ch2-006"
})
MERGE (ipm)-[:TARGETS]->(disease_cat)
WITH ch2, ipm, disease_cat
UNWIND [
  ["Rice Blast", "Prevented using Chitosan and Metalaxyl Propineb (biofungicides/resistance inducers)."],
  ["Sheath Blight", "Controlled with Propineb and Zinc fungicides."],
  ["Bacterial Leaf Blight", "Controlled with Propineb and Zinc bactericides."]
] AS disease
MERGE (d:Disease {
  entity_id: disease[0],
  description: disease[1],
  source_id: "chunk-ch2-006"
})
MERGE (disease_cat)-[:INCLUDES]->(d)
WITH ch2, ipm

// === Golden Apple Snail Management ===
MERGE (snail:Pest {
  entity_id: "Golden Apple Snail",
  description: "Eats seedlings. Managed by manual, bait, barrier, and molluscicide methods.",
  source_id: "chunk-ch2-006"
})
MERGE (ipm)-[:TARGETS]->(snail)
WITH ch2, ipm, snail
UNWIND [
  "Manual collection and burial of adults/eggs",
  "Use banana/taro/papaya leaves as bait",
  "Trap with wooden stakes or bamboo",
  "Install fine mesh at field inlets",
  "Dig trenches to concentrate snails",
  "Let ducks/geese graze in fields",
  "Use Niclosamide-based molluscicide"
] AS snail_method
MERGE (m:Technique {
  entity_id: "Snail Control - " + snail_method,
  description: snail_method,
  source_id: "chunk-ch2-006"
})
MERGE (snail)-[:MANAGED_BY]->(m)
WITH ch2, ipm

// === Field Rat Management ===
MERGE (rat:Pest {
  entity_id: "Field Rat",
  description: "Feeds on rice plants. Requires synchronized and biological control.",
  source_id: "chunk-ch2-006"
})
MERGE (ipm)-[:TARGETS]->(rat)
WITH ch2, rat
UNWIND [
  "Synchronized sowing and rat control",
  "Fencing and trap-crop systems",
  "Clearing vegetation + stubble burning",
  "Smoking burrows + manual traps",
  "Use rodenticides with food bait"
] AS rat_method
MERGE (rm:Technique {
  entity_id: "Rat Control - " + rat_method,
  description: rat_method,
  source_id: "chunk-ch2-006"
})
MERGE (rat)-[:MANAGED_BY]->(rm)
WITH ch2

// === Weed Management ===
MERGE (weed:Practice {
  entity_id: "Weed Management - Ch2",
  entity_type: "practice",
  description: "Integrates pre-seeding land prep, certified seed, herbicide rotation, and mechanical weeding.",
  source_id: "chunk-ch2-006"
})
MERGE (ch2)-[:COVERS]->(weed)
WITH ch2, weed
UNWIND [
  ["Pretilachlor", "Pre-emergence herbicide for early-stage weed suppression."],
  ["Butachlor", "Kills germinating weed seeds pre-emergence."],
  ["Bispyribac sodium", "Post-emergence herbicide for grassy and broadleaf weeds."],
  ["Pyrazosulfuron ethyl", "Post-emergence selective weed control."]
] AS herb
MERGE (h:Chemical {
  entity_id: herb[0],
  description: herb[1],
  source_id: "chunk-ch2-006"
})
MERGE (weed)-[:USES]->(h)

MERGE (weeder:Tool {
  entity_id: "Mechanical Weeder",
  description: "Used in direct sowing systems (cluster/row) to suppress weeds and aerate soil.",
  source_id: "chunk-ch2-006"
})
MERGE (weed)-[:SUPPORTED_BY]->(weeder)


"""