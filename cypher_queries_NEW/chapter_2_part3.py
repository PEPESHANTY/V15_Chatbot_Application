cypher = """
// =======================================
// Chapter 2 (Part 3) — Sowing (Mekong Delta)
// Single-statement, idempotent upsert with :Searchable + search_text
// =======================================

// Ensure Chapter 2 node exists (your ID)
MERGE (ch2:Chapter { entity_id: 'Cultivation Techniques - Ch2' })
SET ch2:Searchable,
    ch2.entity_type = coalesce(ch2.entity_type, 'chapter'),
    ch2.chapter     = 'Ch2',
    ch2.file_path   = coalesce(ch2.file_path, 'book_1.pdf')

// === Sowing Subsection under Chapter 2 ===
MERGE (sow:Practice:Searchable {
  entity_id:  'Sowing - Ch2',
  entity_type:'practice',
  name:       'Sowing'
})
SET sow.chapter     = 'Ch2',
    sow.source_id   = 'chunk-ch2-003',
    sow.description = 'Standardized mechanization protocol for rice sowing in the Mekong Delta using row and cluster machines; integrates spacing, shallow depth, and fertilizer co-placement to reduce seed/fertilizer use, lodging, disease, and post-harvest loss while improving yield and uniformity.',
    sow.search_text = 'sowing | mechanized sowing | row sowing | cluster sowing | spacing 20–30 cm | cluster 12–20 cm | depth 1–3 mm | ≤60 kg/ha row | ≤50 kg/ha cluster | fertilizer 3–5 cm deep | wide–narrow rows 35/15 cm | yield +5% vs broadcasting | lodging reduction | disease reduction | uniformity | Mekong Delta'
MERGE (ch2)-[:COVERS {source_id:'chunk-ch2-003'}]->(sow)

// === 3.1. Sowing Time ===
MERGE (time:Concept:Searchable {
  entity_id:  'Sowing Time',
  name:       'Sowing Time',
  entity_type:'concept'
})
SET time.chapter     = 'Ch2',
    time.source_id   = 'chunk-ch2-003',
    time.description = 'Follow official sowing schedules from local authorities; consult CS-MAP risk maps and forecasts to avoid drought, salinity, and flood risk.',
    time.search_text = 'sowing time | official schedule | CS-MAP | risk maps | drought | salinity | flood | forecast | timing guidance'
MERGE (sow)-[:INCLUDES {source_id:'chunk-ch2-003'}]->(time)

// === 3.2. Sowing Methods ===
WITH sow
UNWIND [
  {
    id:   'Row Sowing',
    name: 'Row Sowing',
    desc: 'Seeding in rows (sạ hàng) at 20–30 cm spacing, ≤60 kg/ha seed rate, 1–3 mm depth. Enhances placement accuracy; reduces seed and fertilizer use and disease risk.'
  },
  {
    id:   'Cluster Sowing',
    name: 'Cluster Sowing',
    desc: 'Cluster sowing (sạ cụm) with 20–30 cm between rows and 12–20 cm within clusters; ≤50 kg/ha. Improves stand uniformity and reduces post-harvest loss.'
  },
  {
    id:   'Wide–Narrow Row Technique',
    name: 'Wide–Narrow Row Technique',
    desc: 'Alternating 35 cm and 15 cm rows (border effect) increases light penetration, reduces disease, and can raise yield; compatible with fertilizer deep placement.'
  }
] AS method
MERGE (m:Technique:Searchable {
  entity_id:  method.id,
  name:       method.name,
  entity_type:'technique'
})
SET m.chapter     = 'Ch2',
    m.source_id   = 'chunk-ch2-003',
    m.description = method.desc,
    m.search_text = method.name+' | '+method.desc+' | row spacing 20–30 cm | cluster spacing 12–20 cm | depth 1–3 mm | ≤60 kg/ha | ≤50 kg/ha | wide 35 cm | narrow 15 cm | border effect'
MERGE (sow)-[:USES {source_id:'chunk-ch2-003'}]->(m)

// === Machinery Overview ===
MERGE (mach:Concept:Searchable {
  entity_id:  'Sowing Machines',
  name:       'Sowing Machines',
  entity_type:'concept'
})
SET mach.chapter     = 'Ch2',
    mach.source_id   = 'chunk-ch2-003',
    mach.description = 'Modern rice sowing machines used in the Mekong Delta: air-pressure row seeders, cluster seeders, and integrated seed+fertilizer sowers; support adjustable spacing and controlled seed rates.',
    mach.search_text = 'sowing machines | air-pressure row seeder | cluster seeder | integrated seed+fertilizer | adjustable spacing | controlled seed rate | mechanization'
MERGE (sow)-[:USES {source_id:'chunk-ch2-003'}]->(mach)

// === Individual Sowing Machines ===
WITH sow, mach
UNWIND [
  {
    id:   '6-Row Air Seeder',
    name: '6-Row Air Seeder',
    desc: 'Máy sạ hàng khí động 6 hàng: adjustable row spacing 20–25 cm; pneumatic sowing; 20–80 kg/ha seed rate; furrow 5–7 cm wide × ~5 cm deep; seed depth 1–3 mm; auto rate vs speed; ≥18 HP; ~3 ha/day capacity.'
  },
  {
    id:   '16-Row Air Seeder',
    name: '16-Row Air Seeder',
    desc: 'Máy sạ hàng khí động 16 hàng: 0.6–1.6 ha/hr; row spacing 20–25 cm; 30–80 kg/ha; furrow 5–7 cm × 5 cm; 1–3 mm seed depth; smart pneumatic feed; integrates land prep + leveling; ≥18 HP.'
  },
  {
    id:   'Cluster Seeder',
    name: 'Cluster Seeder',
    desc: 'Máy sạ cụm: row spacing 20–30 cm; 0–20 seeds/cluster; up to 120 kg/ha; 25 HP tractor; 0.3–1 ha/hr; can add fertilizer/pesticide modules.'
  },
  {
    id:   'Cluster Seeder + Fertilizer',
    name: 'Cluster Seeder + Fertilizer',
    desc: 'Máy sạ cụm kết hợp vùi phân: pneumatic seed + fertilizer co-placement at 3–5 cm depth; reduces N loss, labor; improves establishment and uniformity.'
  },
  {
    id:   'Wide–Narrow Seeder',
    name: 'Wide–Narrow Seeder',
    desc: 'Seeder for 35/15 cm alternating rows; boosts light penetration and nutrient efficiency; typically includes integrated fertilizer system.'
  },
  {
    id:   'Aerodynamic Cluster Seeder',
    name: 'Aerodynamic Cluster Seeder',
    desc: 'Aerodynamic cluster seeder: adjustable module spacing 20/25/30/40 cm; 5–7 sowing modules (10–14 rows); compressed air delivery; deep fertilizer placement; front leveling tools.'
  },
  {
    id:   'Mechanical Cluster Seeder',
    name: 'Mechanical Cluster Seeder',
    desc: 'Mechanical cluster seeder: modular; fits 2/4-wheel tractors or transplanters; rotary sowers + fertilizer shafts via PTO; customizable spacing; robust for varied field conditions.'
  }
] AS machine
MERGE (mm:Machine:Searchable {
  entity_id:  machine.id,
  name:       machine.name,
  entity_type:'machine'
})
SET mm.chapter     = 'Ch2',
    mm.source_id   = 'chunk-ch2-003',
    mm.description = machine.desc,
    mm.search_text = machine.name+' | '+machine.desc+' | spacing | seed rate | capacity | horsepower | pneumatic | PTO | fertilizer co-placement | furrow 5–7 cm | depth 1–3 mm'
MERGE (mach)-[:INCLUDES {source_id:'chunk-ch2-003'}]->(mm)

// === Benefits of Sowing Techniques ===
WITH sow
UNWIND [
  'Reduces seed and fertilizer consumption',
  'Minimizes lodging and disease',
  'Boosts yield by ~5% over broadcasting',
  'Improves post-harvest grain recovery',
  'Enhances uniformity and crop health'
] AS benefit
MERGE (b:Benefit:Searchable {
  entity_id:  benefit,
  name:       benefit,
  entity_type:'benefit'
})
SET b.chapter     = 'Ch2',
    b.source_id   = 'chunk-ch2-003',
    b.description = benefit,
    b.search_text = benefit+' | mechanized sowing benefit | efficiency | yield | lodging | disease | uniformity'
MERGE (sow)-[:ACHIEVES {source_id:'chunk-ch2-003'}]->(b)

// === Guidelines (Decision 396/QĐ-TT-VPPN, 2023-10-31) ===
MERGE (guide:Policy:Searchable {
  entity_id:  'Decision 396/QĐ-TT-VPPN',
  name:       'Decision 396/QĐ-TT-VPPN',
  entity_type:'policy'
})
SET guide.chapter     = 'Ch2',
    guide.source_id   = 'chunk-ch2-003',
    guide.description = 'Issued Oct 31, 2023 by the Department of Crop Production; establishes sowing machinery and protocol for mechanized rice sowing in the Mekong Delta to improve efficiency and reduce emissions.',
    guide.search_text = 'Decision 396/QĐ-TT-VPPN | 2023-10-31 | Department of Crop Production | sowing machinery | protocol | Mekong Delta | efficiency | emissions reduction'
MERGE (sow)-[:GUIDED_BY {source_id:'chunk-ch2-003'}]->(guide)
"""
