cypher= """


// === Chapter 4 – Part 3.2: Mushroom Cultivation ===
MERGE (mushroom:Practice {
  entity_id: "Straw Mushroom Cultivation - Ch4",
  entity_type: "practice",
  description: "Low-cost outdoor and indoor cultivation of straw mushrooms using clean rice straw and composted substrate with fungal spawn. Supports circular agriculture and income diversification.",
  source_id: "chunk-ch4-003"
})
WITH mushroom

MATCH (ch4:Chapter {entity_id: "Straw Management - Ch4"})
MERGE (ch4)-[:COVERS]->(mushroom)
WITH mushroom

// === Subtypes: Outdoor and Indoor ===
UNWIND [
  ["Outdoor Straw Mushroom Cultivation - Ch4", "Outdoor cultivation using lime-treated straw soaked in CaO solution, fermented on bamboo racks under tarp, with manual watering and two harvest flushes."],
  ["Indoor Straw Mushroom Cultivation - Ch4", "Indoor tiered-rack cultivation with sanitized straw, temperature-humidity control, artificial light, and nutrient additives for optimized yield."]
] AS type
MERGE (sub:Method {
  entity_id: type[0],
  entity_type: "method",
  description: type[1],
  source_id: "chunk-ch4-003"
})
MERGE (mushroom)-[:USES_METHOD]->(sub)
WITH mushroom

// === Shared Inputs and Spawn ===
MERGE (straw:Input {
  entity_id: "Clean Rice Straw - Ch4",
  entity_type: "input",
  description: "Disease-free, pesticide-free straw in bundles or rolls; soaked in lime or enriched solutions before composting.",
  source_id: "chunk-ch4-003"
})
MERGE (spawn:Input {
  entity_id: "Mushroom Spawn - Ch4",
  entity_type: "input",
  description: "High-quality straw-based mycelium mixed with cow manure, worm compost, banana stem powder, or HVP/HQ.",
  source_id: "chunk-ch4-003"
})
MERGE (mushroom)-[:USES]->(straw)
MERGE (mushroom)-[:USES]->(spawn)
WITH mushroom

// === Outdoor Cultivation Steps ===
UNWIND [
  ["Site Preparation - Outdoor - Ch4", "Flat, moist, shaded site like paddy or raised beds; lime-treated (5kg CaCO3 per 100m2)."],
  ["Straw Soaking - Outdoor - Ch4", "Soak straw in 5kg CaO per 1m3 water for 5–10 mins; drain to reach pH 13–14."],
  ["Composting - Outdoor - Ch4", "Pile on bamboo frames 10–20cm high, covered with tarp; turn on day 7 and 17, maintain 70°C core temp."],
  ["Bed Formation - Outdoor - Ch4", "Form 35cm wide, 35–40cm tall beds; use 4kg straw + 160g spawn + 1–2kg top straw."],
  ["Moisture Management - Outdoor - Ch4", "Cover with mesh + straw, water daily 4PM; ventilate with tarp during rain."],
  ["Fruiting & Harvesting - Outdoor - Ch4", "Pinheads on day 9–10; harvest twice daily from day 12; two flushes with 5-day interval."],
  ["Spent Straw Compost - Outdoor - Ch4", "Used straw decomposed into organic matter for reuse as compost."]
] AS step
MERGE (s:Step {
  entity_id: step[0],
  entity_type: "step",
  description: step[1],
  source_id: "chunk-ch4-003"
})
MERGE (mushroom)-[:HAS_STEP]->(s)
WITH mushroom

// === Indoor Cultivation Steps ===
UNWIND [
  ["Infrastructure Setup - Indoor - Ch4", "Construct ventilated mushroom house with racks (2–4 tiers, 0.5m apart), netted walls, tarp roof, on dry soil or concrete."],
  ["Straw Soaking - Indoor - Ch4", "Soak clean straw in 5kg CaO + 1kg superphosphate + 0.5kg KCl per 1m3 water for 5–10 mins; drain well."],
  ["Composting & Turning - Indoor - Ch4", "Pile soaked straw on bamboo or soil, cover with tarp, turn on day 7 and 17, maintain 70°C."],
  ["Spawn Enrichment - Indoor - Ch4", "Mix spawn with cow dung, worm compost, HVP/HQ; finely chopped and distributed uniformly."],
  ["Rack Setup & Inoculation - Indoor - Ch4", "Distribute straw on racks, apply spawn (200g/m2), incubate 3 days, add 2kg/m2 worm compost."],
  ["Fruiting Management - Indoor - Ch4", "Keep RH 50–70% initially, then 80–100%; temp 25–30°C; mist spray if dry; expose to 12h light."],
  ["Sodium Acetate Spray - Indoor - Ch4", "Spray 0.05% sodium acetate (1L/m2) to stimulate fruiting."],
  ["Harvesting - Indoor - Ch4", "Harvest twice daily from day 12; flush 1 lasts 4 days; flush 2 after 3–5 days; convert straw to compost."]
] AS indoor_step
MERGE (i:Step {
  entity_id: indoor_step[0],
  entity_type: "step",
  description: indoor_step[1],
  source_id: "chunk-ch4-003"
})
MERGE (mushroom)-[:HAS_STEP]->(i)
WITH mushroom

// === Compost Output ===
MERGE (compost:Output {
  entity_id: "Organic Compost from Spent Straw - Ch4",
  entity_type: "output",
  description: "After harvesting, used straw is recycled as giá thể hữu cơ rơm — organic compost that enhances soil health.",
  source_id: "chunk-ch4-003"
})
MERGE (mushroom)-[:PRODUCES]->(compost)


"""