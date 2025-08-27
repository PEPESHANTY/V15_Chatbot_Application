cypher= """
// === Seed Preparation Section ===
MATCH (ch2:Chapter {entity_id: "Cultivation Techniques - Ch2"})

MERGE (seed:Practice {
  entity_id: "Seed Preparation - Ch2",
  entity_type: "practice",
  name: "Seed Preparation",
  description: "Comprehensive seed preparation protocol for Mekong Delta rice farming, based on Decision No. 73/QĐ-TT-VPPN. Includes certified seed use, optimal seeding rates, soaking protocols, germination staging, and mechanization alignment.",
  source_id: "chunk-ch2-002"
})
MERGE (ch2)-[:COVERS {
  description: "Chapter 2 includes seed preparation as a critical practice before sowing.",
  source_id: "chunk-ch2-002"
}]->(seed)

// Certified Seeds
MERGE (cert:Concept {
  entity_id: "Certified Seed - Ch2",
  name: "Certified Seed",
  entity_type: "input",
  description: "Government-approved seeds that ensure varietal purity and strong establishment.",
  source_id: "chunk-ch2-002"
})
MERGE (seed)-[:REQUIRES]->(cert)

// Seeding Rate
MERGE (rate:Parameter {
  entity_id: "Seeding Rate - Ch2",
  name: "Seeding Rate Limit",
  entity_type: "parameter",
  description: "Do not exceed 70 kg/ha to avoid overcrowding, optimize costs, and ensure uniform stand.",
  source_id: "chunk-ch2-002"
})
MERGE (seed)-[:FOLLOWS]->(rate)

// Germination Length
MERGE (germ:Concept {
  entity_id: "Germination Length - Ch2",
  name: "Ideal Germination Length",
  entity_type: "parameter",
  description: "Seed sprouting should reach 0.5–1.0 mm to be suitable for mechanized sowing.",
  source_id: "chunk-ch2-002"
})
MERGE (seed)-[:TARGETS]->(germ)

// Sunlight Pre-treatment
MERGE (sun:Step {
  entity_id: "Sun Exposure - Ch2",
  name: "Sunlight Exposure",
  entity_type: "step",
  description: "Expose seeds to sunlight for 2–3 hours prior to soaking to boost germination response.",
  source_id: "chunk-ch2-002"
})
MERGE (seed)-[:INCLUDES]->(sun)

// Soaking & Incubation
MERGE (soak:Process {
  entity_id: "Soaking and Incubation - Ch2",
  name: "Seed Soaking and Incubation",
  entity_type: "method",
  description: "Soak for 24–48h (change after 12h), incubate at 30–35°C for 12–24h until root tip emerges. Prevent souring, remove unfilled seeds.",
  source_id: "chunk-ch2-002"
})
MERGE (seed)-[:USES]->(soak)

// Holding sprouted seeds
MERGE (hold:Condition {
  entity_id: "Sprout Holding - Ch2",
  name: "Sprout Holding Conditions",
  entity_type: "condition",
  description: "Spread in cool, shaded areas if sowing delayed, to prevent elongation and entanglement.",
  source_id: "chunk-ch2-002"
})
MERGE (seed)-[:REQUIRES]->(hold)

// Sowing Depth
MERGE (depth:Parameter {
  entity_id: "Sowing Depth - Ch2",
  name: "Sowing Depth",
  entity_type: "parameter",
  description: "Maintain shallow depth of 1–3 mm for seed-to-soil contact and fast emergence.",
  source_id: "chunk-ch2-002"
})
MERGE (seed)-[:USES]->(depth)

// Sowing Spacing
MERGE (space:Parameter {
  entity_id: "Row and Cluster Spacing - Ch2",
  name: "Sowing Spacing",
  entity_type: "parameter",
  description: "Row sowing: 20–30 cm; Cluster sowing: 12–20 cm between and within clusters.",
  source_id: "chunk-ch2-002"
})
MERGE (seed)-[:REQUIRES]->(space)

// Fertilizer Integration
MERGE (fert:Input {
  entity_id: "Fertilizer Placement - Ch2",
  name: "Fertilizer Incorporation",
  entity_type: "input",
  description: "Apply fertilizer at 3.0–4.0 cm depth during sowing to improve nutrient uptake.",
  source_id: "chunk-ch2-002"
})
MERGE (seed)-[:INTEGRATES_WITH]->(fert)

// Seed Rate Formula
MERGE (formula:Formula {
  entity_id: "Seed Rate Formula - Ch2",
  name: "Seed Quantity Adjustment Formula",
  entity_type: "calculation",
  description: "Adjusted rate = base x (1 + %non-germinated + %mechanical loss). Ex: 115% for 90% germination.",
  source_id: "chunk-ch2-002"
})
MERGE (seed)-[:CALCULATES_USING]->(formula)

// Seeder Equipment
MERGE (machine:Tool {
  entity_id: "Rice Seeder - Ch2",
  name: "Seeder Machine",
  entity_type: "tool",
  description: "Machines like row or cluster seeders are used for consistent, mechanized seed placement.",
  source_id: "chunk-ch2-002"
})
MERGE (seed)-[:REQUIRES_TOOL]->(machine)
"""
