cypher = """
// ===============================
// Chapter 2 — Cultivation Techniques (Ch2)
// Single-statement, idempotent upsert with :Searchable + search_text
// ===============================

MERGE (ch2:Chapter:Searchable {entity_id:'Ch2', entity_type:'chapter'})
SET ch2.name='Cultivation Techniques — Chapter 2 (Mekong Delta)',
    ch2.chapter='Ch2',
    ch2.file_path='book_1.pdf',
    ch2.source_id='chunk-ch2-001',
    ch2.summary='Integrated stages for sustainable rice cultivation: land preparation, sowing, water (AWD), fertilization (SSNM), IPM, harvesting.',
    ch2.keywords=['cultivation','land preparation','laser leveling','rotary tillage','AWD','SSNM','IPM','mechanization','combine harvester','drainage furrows'],
    ch2.description='Chapter 2 details synchronized cultivation techniques for high-efficiency, low-emission rice: avoid >30 days waterlogging pre-tillage; laser leveling to ≤5 cm (≤3 cm for precision); sow ≤70 kg/ha using row/cluster seeders with fertilizer dispensers; fertilize via SSNM with soil analysis every 5 years; manage water via AWD; apply IPM (4 Rights); harvest by combine at ~85–90% maturity.',
    ch2.search_text=ch2.name+' | '+ch2.summary+' | '+ch2.description+' | Mekong Delta | synchronized | resource-efficient | low emission | green growth | rotary tillage 7–15 cm | phoi ai 15–30 days | drainage furrows 6–9 m | ≤5 cm | ≤3 cm | ≤70 kg/ha | SSNM soil analysis 5 years | AWD methane reduction | IPM 4 Rights | combine harvester 85–90%'

// ---------- High-level project (safe MERGE) ----------
MERGE (proj:Project:Searchable {entity_id:'One Million Hectares Project', entity_type:'project'})
SET proj.name='One Million Hectares Project (High-Quality, Low-Emission Rice, Mekong Delta, by 2030)',
    proj.summary='National project for 1M hectares of high-quality, low-emission rice aligned with green growth.',
    proj.description='Government-backed program enabling climate-smart rice via standards for land prep, sowing, irrigation (AWD), fertilization (SSNM), IPM, mechanized harvesting.',
    proj.search_text=proj.name+' | '+proj.summary+' | '+proj.description+' | 2030 | decision 1490 | climate-smart rice | Mekong Delta'
MERGE (ch2)-[:FOCUSES_ON]->(proj)

// ===============================
// Land Preparation (core practice)
// ===============================
MERGE (lp:Practice:Searchable {entity_id:'Land Preparation - Ch2', entity_type:'practice', name:'Land Preparation'})
SET lp.chapter='Ch2',
    lp.description='Pre-sowing preparation: weed suppression, field sanitation, wet/dry rotary tillage (7–15 cm), sun-drying (phơi ải) 15–30 days, drainage furrows, and precision laser leveling to ≤5 cm (≤3 cm for high precision). Foundation for mechanized, low-emission farming.',
    lp.keywords=['weed control','field sanitation','rotary tillage','sun-drying','laser leveling','drainage'],
    lp.search_text=lp.name+' | wet tillage | dry tillage | rotary blades C/L/LC | 7–15 cm depth | phoi ai 15–30 days | drainage furrows 6–9 m | <=5 cm | <=3 cm | mechanized sowing readiness | pathogen reduction'
MERGE (ch2)-[:COVERS]->(lp)

// Guideline document + issuer
MERGE (guideline:Document:Searchable {entity_id:'Decision 73/QĐ-TT-VPPN', entity_type:'document'})
SET guideline.name='Common Soil Preparation Procedure in the Mekong Delta',
    guideline.chapter='Ch2',
    guideline.description='Official guideline for soil preparation in the Mekong Delta, issued Apr 25, 2022 by the Department of Crop Production.',
    guideline.search_text=guideline.name+' | soil preparation | Mekong Delta | 2022-04-25 | Department of Crop Production | Decision 73/QĐ-TT-VPPN'
MERGE (lp)-[:GUIDED_BY]->(guideline)
MERGE (dept:Organization:Searchable {entity_id:'Department of Crop Production', entity_type:'organization', name:'Department of Crop Production'})
SET dept.chapter='Ch2',
    dept.description='Issuing authority for soil preparation guideline; national steward for rice production standards.',
    dept.search_text=dept.name+' | issuer | soil preparation guideline | Mekong Delta | Decision 73/QĐ-TT-VPPN'
MERGE (dept)-[:ISSUED]->(guideline)

// Laser land leveling
MERGE (laser:Technology:Searchable {entity_id:'Laser Land Leveling - Ch2', entity_type:'technology', name:'Laser Land Leveling'})
SET laser.chapter='Ch2',
    laser.description='Automated blade control using laser transmitter/receiver + hydraulic adjustment on 4-wheel tractor; maintains uniform surface with ≤5 cm (≤3 cm per spec), improves water distribution, reduces input loss, supports uniform maturity.',
    laser.search_text=laser.name+' | transmitter | receiver | hydraulic control | electronic control box | 4-wheel tractor | <=5 cm | <=3 cm | uniform irrigation | seed/fertilizer efficiency | higher yield | lower labor'
MERGE (lp)-[:USES]->(laser)
WITH lp, laser
MERGE (comp:Equipment:Searchable {entity_id:'Laser Leveling System Components - Ch2', entity_type:'equipment', name:'Laser Leveling System Components'})
SET comp.chapter='Ch2',
    comp.description='Laser transmitter (tripod), receiver (on implement), electronic control box, hydraulic cylinder controlling leveling blade.',
    comp.search_text=comp.name+' | transmitter | receiver | control box | hydraulic cylinder | leveling blade | tractor-mounted'
MERGE (laser)-[:COMPRISES]->(comp)

// Rotary tillage
MERGE (tillage:Practice:Searchable {entity_id:'Rotary Tillage - Ch2', entity_type:'practice', name:'Rotary Tillage'})
SET tillage.chapter='Ch2',
    tillage.description='Wet tillage pass 1 (loosen soil, incorporate residue), wet pass 2 (refine seedbed), and dry tillage for aeration/crumb structure; rotary blades (C/L/LC) at 7–15 cm; 4-wheel tractors with cage wheels in flooded fields.',
    tillage.search_text=tillage.name+' | wet tillage pass 1 | wet tillage pass 2 | dry tillage | rotary blades C L LC | 7–15 cm | 4-wheel tractor | cage wheels | residue incorporation | aeration | seedbed quality'
MERGE (lp)-[:INCLUDES]->(tillage)
WITH lp, tillage
MERGE (tractor:Equipment:Searchable {entity_id:'4-Wheel Tractor with Cage Wheels - Ch2', entity_type:'equipment', name:'4-Wheel Tractor with Cage Wheels'})
SET tractor.chapter='Ch2',
    tractor.description='Tractor fitted with cage wheels to increase traction during wet tillage; supports rotary implements.',
    tractor.search_text=tractor.name+' | traction | flooded field | rotary tillage | mechanization'
MERGE (tillage)-[:USES]->(tractor)

// Sun-drying & sanitation
MERGE (sun_drying:Practice:Searchable {entity_id:'Soil Sun-Drying - Ch2', entity_type:'practice', name:'Soil Sun-Drying (Phơi ải)'})
SET sun_drying.chapter='Ch2',
    sun_drying.description='Expose soil 15–30 days to sunlight to decompose residues (incl. with Trichoderma), suppress pathogens/pests, and improve aeration/structure ahead of sowing.',
    sun_drying.search_text='phoi ai | sun-drying 15–30 days | residue decomposition | Trichoderma | pathogen suppression | aeration | structure | sowing readiness'
MERGE (lp)-[:INCLUDES]->(sun_drying)

MERGE (sanitation:Practice:Searchable {entity_id:'Field Sanitation - Ch2', entity_type:'practice', name:'Field Sanitation'})
SET sanitation.chapter='Ch2',
    sanitation.description='Clean borders, reinforce dikes, finely till, disrupt golden apple snail life cycle; drain field 6–12 h before sowing.',
    sanitation.search_text='field sanitation | border cleaning | dike reinforcement | fine tillage | drain 6–12 h pre-sowing | golden apple snail'
MERGE (lp)-[:INCLUDES]->(sanitation)

// Drainage furrows
MERGE (furrows:Practice:Searchable {entity_id:'Water Drainage Furrows - Ch2', entity_type:'practice', name:'Water Drainage Furrows'})
SET furrows.chapter='Ch2',
    furrows.description='Create drainage furrows 6–9 m apart; 20–30 cm wide; 15–20 cm deep to improve drainage, aeration, and leach salts/acidity; crucial for uniform stands.',
    furrows.search_text='drainage furrows | 6–9 m spacing | 20–30 cm width | 15–20 cm depth | aeration | salt leaching | uniform germination'
MERGE (lp)-[:INCLUDES]->(furrows)

// Six soil preparation methods
WITH lp
UNWIND [
  {id:'Soil Prep Method #1 - Ch2', desc:'Sanitation → wet tillage ×2 with 7–10 day soak between → mechanical leveling; decomposes OM and softens soil for a fine seedbed.'},
  {id:'Soil Prep Method #2 - Ch2', desc:'Sanitation → wet tillage ×1 → soak 7–10 days → pump water → tractor leveling; suited where natural retention is low.'},
  {id:'Soil Prep Method #3 - Ch2', desc:'Use roller axle (trục băng bánh lồng) to compact/level → soak >3 weeks → pump water → final leveling; for compacted/uncultivated land.'},
  {id:'Soil Prep Method #4 - Ch2', desc:'Sanitation → harrow (cày chảo) → sun/air exposure (phơi ải) → pump water → wet tillage → leveling.'},
  {id:'Soil Prep Method #5 - Ch2', desc:'Sanitation → harrow → dry tillage → air exposure → pump water → leveling; best for hardened/crusted topsoil.'},
  {id:'Soil Prep Method #6 - Ch2', desc:'Like #5 but skip final wet tillage: air exposure → pump water → leveling; faster where equipment/time is limited.'}
] AS m
MERGE (method:Method:Searchable {entity_id:m.id, entity_type:'method', name:m.id})
SET method.chapter='Ch2',
    method.description=m.desc,
    method.search_text=method.name+' | '+m.desc+' | soil condition | season | water availability | mechanization'
MERGE (lp)-[:USES_METHOD]->(method)

// Final leveling
MERGE (leveling:Practice:Searchable {entity_id:'Final Field Leveling - Ch2', entity_type:'practice', name:'Final Field Leveling'})
SET leveling.chapter='Ch2',
    leveling.description='Final surface leveling (trục, trạc) by 2-wheel or 4-wheel tractors for flat surface with ≤5 cm height variation; prevents pooling/dry patches.',
    leveling.search_text='final leveling | truc | trac | 2-wheel | 4-wheel | <=5 cm | flat surface | irrigation uniformity | nutrient evenness'
MERGE (lp)-[:FOLLOWS_WITH]->(leveling)

// Golden apple snail threat
MERGE (snail:Threat:Searchable {entity_id:'Golden Apple Snail', entity_type:'pest', name:'Golden Apple Snail'})
SET snail.chapter='Ch2',
    snail.description='Invasive paddy snail; manage via drainage, sun-drying, egg removal, and mechanical disruption during tillage.',
    snail.search_text='golden apple snail | invasive pest | egg removal | drainage | sun-drying | mechanical disruption'
MERGE (lp)-[:TARGETS]->(snail)

// Emission reduction concept
MERGE (emissions:Concept:Searchable {entity_id:'GHG Emission Reduction', entity_type:'concept', name:'GHG Emission Reduction'})
SET emissions.chapter='Ch2',
    emissions.description='Land-prep choices (reduced prolonged waterlogging, proper residue handling) and AWD cut methane; mechanization improves efficiency.',
    emissions.search_text='methane reduction | AWD | residue management | waterlogging | mechanization | emission reduction'
MERGE (lp)-[:CONTRIBUTES_TO]->(emissions)

// ===============================
// Downstream stages referenced by Chapter 2 text
// (sowing, fertilization SSNM, water mgmt AWD, IPM, harvesting)
// ===============================
MERGE (sow:Practice:Searchable {entity_id:'Sowing Techniques - Ch2', entity_type:'practice', name:'Sowing Techniques'})
SET sow.chapter='Ch2',
    sow.description='Sow at ≤70 kg/ha using row or cluster seeders integrated with fertilizer dispensers; improves placement and reduces crowding/disease.',
    sow.search_text='sowing <=70 kg/ha | row seeder | cluster seeder | fertilizer deep placement | NUE | reduce crowding | disease pressure'
MERGE (ch2)-[:COVERS]->(sow)
MERGE (seeder:Equipment:Searchable {entity_id:'Row/Cluster Seeder with Fertilizer Dispenser - Ch2', entity_type:'equipment', name:'Row/Cluster Seeder + Fertilizer Dispenser'})
SET seeder.chapter='Ch2',
    seeder.description='Mechanized seeders that place seed and fertilizer in-row/cluster for efficiency and emission reduction.',
    seeder.search_text='mechanized seeder | row | cluster | fertilizer placement | labor saving | uniform stand'
MERGE (sow)-[:USES]->(seeder)

MERGE (fert:Practice:Searchable {entity_id:'Fertilization (SSNM) - Ch2', entity_type:'practice', name:'Fertilization (SSNM)'})
SET fert.chapter='Ch2',
    fert.description='Site-Specific Nutrient Management tailored to plot needs; soil analysis every 5 years guides balanced applications to boost yield and cut runoff.',
    fert.search_text='SSNM | site-specific nutrient management | soil analysis every 5 years | balanced NPK | runoff reduction | yield'
MERGE (ch2)-[:COVERS]->(fert)

MERGE (water:Practice:Searchable {entity_id:'Water Management (AWD) - Ch2', entity_type:'practice', name:'Water Management (AWD)'})
SET water.chapter='Ch2',
    water.description='Alternate Wetting and Drying with periodic non-flooded intervals; avoid >30 days continuous waterlogging pre-tillage; saves water and reduces methane.',
    water.search_text='AWD | alternate wetting and drying | avoid >30 days waterlogging | methane reduction | water saving'
MERGE (ch2)-[:COVERS]->(water)
MERGE (awd:Acronym:Searchable {entity_id:'AWD', entity_type:'acronym', name:'Alternate Wetting and Drying'})
SET awd.description='Irrigation technique with controlled drying cycles to cut methane and save water.',
    awd.search_text='AWD | irrigation | drying cycles | methane | water saving'
MERGE (awd)-[:USED_IN]->(water)

MERGE (ipm:Practice:Searchable {entity_id:'Integrated Pest Management - Ch2', entity_type:'practice', name:'Integrated Pest Management'})
SET ipm.chapter='Ch2',
    ipm.description='Monitor pests, prefer biological control, and follow the 4 Rights for pesticides (right product/time/dose/method) to avoid residues.',
    ipm.search_text='IPM | biological control | monitoring | 4 Rights | residue avoidance'
MERGE (ch2)-[:COVERS]->(ipm)

MERGE (harvest:Practice:Searchable {entity_id:'Harvesting - Ch2', entity_type:'practice', name:'Harvesting'})
SET harvest.chapter='Ch2',
    harvest.description='Harvest 100% mechanized using combine harvesters when grains reach ~85–90% maturity to minimize losses and optimize quality.',
    harvest.search_text='combine harvester | 100% mechanized | 85–90% maturity | loss reduction | quality'
MERGE (ch2)-[:COVERS]->(harvest)
MERGE (comb:Equipment:Searchable {entity_id:'Combine Harvester - Ch2', entity_type:'equipment', name:'Combine Harvester'})
SET comb.chapter='Ch2',
    comb.description='Modern combines reduce labor and post-harvest loss; support timely harvest at 85–90% maturity.',
    comb.search_text='combine | mechanization | loss reduction | maturity 85–90%'
MERGE (harvest)-[:USES]->(comb)

// Helpful cross-link to GHG
MERGE (ghg:Concept:Searchable {entity_id:'Greenhouse Gas Emissions', entity_type:'concept', name:'Greenhouse Gas Emissions'})
SET ghg.description='Methane and associated GHGs from paddy fields targeted by AWD and residue/water management.'
MERGE (water)-[:REDUCES]->(ghg)
"""
