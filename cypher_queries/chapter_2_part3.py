cypher= """

// === Sowing Subsection under Chapter 2 ===
MERGE (sow:Practice {
  entity_id: "Sowing - Ch2",
  entity_type: "practice",
  description: "Standardized mechanization protocol for rice sowing using row and cluster machines in the Mekong Delta.",
  source_id: "chunk-ch2-003"
})

MERGE (ch2:Chapter {
  entity_id: "Cultivation Techniques - Ch2"
})
MERGE (ch2)-[:COVERS]->(sow)
WITH sow

// === 3.1. Sowing Time ===
MERGE (time:Concept {
  entity_id: "Sowing Time",
  description: "Official sowing schedules are advised by local authorities; farmers should consult CS-MAP risk maps and forecasts to avoid drought, salinity, and flood risk.",
  source_id: "chunk-ch2-003"
})
MERGE (sow)-[:INCLUDES]->(time)
WITH sow

// === 3.2. Sowing Methods ===
UNWIND [
  {
    id: "Row Sowing",
    desc: "Seeding in rows (sạ hàng) at 20–30 cm spacing, ≤ 60 kg/ha seed rate, 1–3 mm depth. Enhances accuracy, reduces seed, fertilizer use and disease."
  },
  {
    id: "Cluster Sowing",
    desc: "Cluster sowing (sạ cụm) with spacing 20–30 cm between rows, 12–20 cm intra-cluster. ≤ 50 kg/ha seed rate. Reduces post-harvest loss."
  },
  {
    id: "Wide–Narrow Row Technique",
    desc: "Alternates 35 cm and 15 cm rows for improved sunlight, lower disease, increased yield."
  }
] AS method
MERGE (m:Technique {
  entity_id: method.id,
  description: method.desc,
  source_id: "chunk-ch2-003"
})
MERGE (sow)-[:USES]->(m)
WITH sow

// === Machinery Overview ===
MERGE (mach:Concept {
  entity_id: "Sowing Machines",
  description: "Modern rice sowing machines used in the Mekong Delta include row, cluster, and integrated sowers.",
  source_id: "chunk-ch2-003"
})
MERGE (sow)-[:USES]->(mach)
WITH sow

// === Individual Sowing Machines ===
UNWIND [
  {
    id: "6-Row Air Seeder",
    desc: "Máy sạ hàng khí động 6 hàng. Adjustable row spacing (20–25 cm), pneumatic sowing, 20–80 kg/ha seed rate, 3 ha/day field capacity."
  },
  {
    id: "16-Row Air Seeder",
    desc: "Máy sạ hàng khí động 16 hàng. 0.6–1.6 ha/hr capacity, pneumatic smart seeding, 30–80 kg/ha seed rate. Integrated land prep + leveling."
  },
  {
    id: "Cluster Seeder",
    desc: "Máy sạ cụm. Row spacing 20–30 cm, 0–20 seeds/cluster, 120 kg/ha max, works with 25 HP tractor, fertilizer/pesticide capable."
  },
  {
    id: "Cluster Seeder + Fertilizer",
    desc: "Máy sạ cụm kết hợp vùi phân. Pneumatic seed + fertilizer placement at 3–5 cm depth, reduces N loss, labor, boosts establishment."
  },
  {
    id: "Wide–Narrow Seeder",
    desc: "Alternates 35/15 cm rows; boosts light, reduces disease, improves nutrient efficiency. Integrated fertilizing system."
  },
  {
    id: "Aerodynamic Cluster Seeder",
    desc: "Adjustable spacing (20–40 cm), 5–7 sowing modules, compressed air system, precision placement, deep fertilizer sowing."
  },
  {
    id: "Mechanical Cluster Seeder",
    desc: "Modular machine fits 2, 4, or transplanter-based tractors. Rotary sowers + fertilizer shafts powered by PTO. Highly customizable."
  }
] AS machine
MERGE (m:Machine {
  entity_id: machine.id,
  description: machine.desc,
  source_id: "chunk-ch2-003"
})
MERGE (mach)-[:INCLUDES]->(m)
WITH sow

// === Benefits of Sowing Techniques ===
UNWIND [
  "Reduces seed and fertilizer consumption",
  "Minimizes lodging and disease",
  "Boosts yield by ~5% over broadcasting",
  "Improves post-harvest grain recovery",
  "Enhances uniformity and crop health"
] AS benefit
MERGE (b:Benefit {
  entity_id: benefit,
  description: benefit,
  source_id: "chunk-ch2-003"
})
MERGE (sow)-[:ACHIEVES]->(b)

// === Guidelines ===
MERGE (guide:Policy {
  entity_id: "Decision 396/QĐ-TT-VPPN",
  description: "Issued October 31, 2023 by Department of Crop Production. Establishes sowing machinery and protocol in Mekong Delta.",
  source_id: "chunk-ch2-003"
})
MERGE (sow)-[:GUIDED_BY]->(guide)

"""