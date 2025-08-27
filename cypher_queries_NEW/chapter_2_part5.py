cypher = """
// =======================================
// Chapter 2 (Part 5) — Fertilizer Management (Mekong Delta)
// Single-statement, idempotent upsert with :Searchable + search_text
// =======================================

// Ensure Chapter 2 exists (your existing ID)
MATCH (ch2:Chapter {entity_id: 'Cultivation Techniques - Ch2'})

// --- Fertilizer Management Root Node ---
MERGE (fert:Practice:Searchable {
  entity_id:  'Fertilizer Management - Ch2',
  entity_type:'practice',
  name:       'Fertilizer Management'
})
SET fert.chapter     = 'Ch2',
    fert.source_id   = 'chunk-ch2-005',
    fert.description = 'Fertilization strategy for Mekong Delta rice: SSNM (soil analysis every 5 years), organic + inorganic inputs, mechanized deep placement, season/soil-specific dosing; targets root health, yield, and input efficiency.',
    fert.search_text = 'fertilizer management | SSNM | site-specific nutrient management | soil analysis 5 years | organic 1.5–3 t/ha | lime 200–300 kg/ha pH 4.0–5.0 | lime 400–500 kg/ha pH <4.0 | NPK | DAP | KCl | urea | mechanized deep placement | reduce N 10–15% | timing 7–10, 18–22, 38–42 DAS | Mekong Delta'
MERGE (ch2)-[:COVERS {source_id:'chunk-ch2-005'}]->(fert)

// --- Site-Specific Nutrient Management ---
WITH fert
MERGE (ssnm:Technique:Searchable {
  entity_id:  'Site-Specific Nutrient Management',
  entity_type:'method',
  name:       'Site-Specific Nutrient Management (SSNM)'
})
SET ssnm.chapter     = 'Ch2',
    ssnm.source_id   = 'chunk-ch2-005',
    ssnm.description = 'Fertilizer strategy matched to plot and season; recalibrate with soil analysis every 5 years to address limiting nutrients and cut losses.',
    ssnm.search_text = 'SSNM | site-specific | soil analysis every 5 years | tailor to season | reduce loss | improve NUE'
MERGE (fert)-[:USES {source_id:'chunk-ch2-005'}]->(ssnm)

// --- Organic Fertilizer ---
WITH fert
MERGE (organic:Input:Searchable {
  entity_id:  'Organic Fertilizer',
  entity_type:'input',
  name:       'Organic Fertilizer'
})
SET organic.chapter     = 'Ch2',
    organic.source_id   = 'chunk-ch2-005',
    organic.description = 'Apply 1.5–3 tons/ha to enhance microbial activity and soil physical structure; supports resilience and yield.',
    organic.search_text = 'organic fertilizer | 1.5–3 t/ha | microbial activity | soil structure | resilience'
MERGE (fert)-[:USES {source_id:'chunk-ch2-005'}]->(organic)

// --- Lime Application by pH ---
WITH fert
MERGE (lime:Input:Searchable {
  entity_id:  'Lime',
  entity_type:'input',
  name:       'Lime (pH management)'
})
SET lime.chapter     = 'Ch2',
    lime.source_id   = 'chunk-ch2-005',
    lime.description = 'Neutralizes acidity: 200–300 kg/ha for pHₖCl 4.0–5.0; 400–500 kg/ha for pHₖCl < 4.0 (highly acidic/alum soils).',
    lime.search_text = 'lime | pH management | 200–300 kg/ha pH 4.0–5.0 | 400–500 kg/ha pH <4.0 | acid sulfate soils'
MERGE (fert)-[:USES {source_id:'chunk-ch2-005'}]->(lime)

// --- Soil-specific Fertilizer Recommendations (Winter–Spring) ---
WITH fert
UNWIND [
  {name:'Alluvial Soil',            Nmin:90, Nmax:100, Pmin:30, Pmax:40, Kmin:30, Kmax:40},
  {name:'Light Acid Sulfate Soil',  Nmin:80, Nmax:100, Pmin:40, Pmax:50, Kmin:25, Kmax:30},
  {name:'Medium Acid Sulfate Soil', Nmin:68, Nmax:80,  Pmin:50, Pmax:60, Kmin:25, Kmax:30}
] AS soil
MERGE (stype:SoilType:Searchable {
  entity_id:  soil.name,
  name:       soil.name
})
SET stype.chapter     = 'Ch2',
    stype.source_id   = 'chunk-ch2-005',
    stype.description = 'Winter–Spring (Đông Xuân) per-hectare recommendation for '+soil.name+': N '+soil.Nmin+'–'+soil.Nmax+' kg, P₂O₅ '+soil.Pmin+'–'+soil.Pmax+' kg, K₂O '+soil.Kmin+'–'+soil.Kmax+' kg.',
    stype.nitrogen_min = soil.Nmin,
    stype.nitrogen_max = soil.Nmax,
    stype.p2o5_min     = soil.Pmin,
    stype.p2o5_max     = soil.Pmax,
    stype.k2o_min      = soil.Kmin,
    stype.k2o_max      = soil.Kmax,
    stype.search_text  = soil.name+' | Winter–Spring | N '+soil.Nmin+'–'+soil.Nmax+' | P2O5 '+soil.Pmin+'–'+soil.Pmax+' | K2O '+soil.Kmin+'–'+soil.Kmax+' | fertilizer recommendation'
MERGE (fert)-[:HAS_RECOMMENDATION {source_id:'chunk-ch2-005'}]->(stype)

// --- Seasonal Adjustment ---
WITH fert
MERGE (adj:Guideline:Searchable {
  entity_id:  'Summer-Autumn Nitrogen Adjustment',
  entity_type:'guideline',
  name:       'Summer–Autumn / Autumn–Winter N Adjustment'
})
SET adj.chapter     = 'Ch2',
    adj.source_id   = 'chunk-ch2-005',
    adj.description = 'In Summer–Autumn and Autumn–Winter, reduce nitrogen by 15–20% vs Winter–Spring due to higher volatilization and changing crop demand.',
    adj.search_text = 'seasonal adjustment | Summer–Autumn | Autumn–Winter | reduce N 15–20% | volatilization | demand'
MERGE (fert)-[:ADJUSTS_FOR {source_id:'chunk-ch2-005'}]->(adj)

// --- Fertilizer Timing: 3 stages ---
WITH fert
UNWIND [
  {key:'7–10 DAS',  text:'Apply 40% of total N at 7–10 days after sowing to support seedling establishment.'},
  {key:'18–22 DAS', text:'Apply 40% N and 40% K₂O during tillering for vegetative growth.'},
  {key:'38–42 DAS', text:'Apply remaining 20% N and 60% K₂O for panicle formation and grain filling.'}
] AS stage
MERGE (timing:Timing:Searchable {
  entity_id:  'Fertilizer Timing - '+stage.key,
  entity_type:'timing',
  name:       'Fertilizer Timing '+stage.key
})
SET timing.chapter     = 'Ch2',
    timing.source_id   = 'chunk-ch2-005',
    timing.description = stage.text,
    timing.search_text = 'fertilizer timing | '+stage.key+' | '+stage.text
MERGE (fert)-[:TIMED_AT {source_id:'chunk-ch2-005'}]->(timing)

// --- Mechanized Fertilization Adjustments ---
WITH fert
MERGE (mech:Guideline:Searchable {
  entity_id:  'Mechanized Fertilizer Management',
  entity_type:'guideline',
  name:       'Mechanized Fertilizer Management'
})
SET mech.chapter     = 'Ch2',
    mech.source_id   = 'chunk-ch2-005',
    mech.description = 'With sowing machines that bury fertilizer, reduce N by 10–15% due to improved uptake; use 2–4 mm slow-dissolving granules to prevent dispenser clogging.',
    mech.search_text = 'mechanized fertilization | deep placement | reduce N 10–15% | slow-release 2–4 mm | avoid clogging | improved uptake'
MERGE (fert)-[:MODIFIED_BY {source_id:'chunk-ch2-005'}]->(mech)

// --- Mechanized Timing: 2 stages ---
WITH fert, mech
UNWIND [
  {key:'At Sowing', text:'Apply 70–80% of total fertilizer at sowing; bury with the machine (deep placement).'},
  {key:'38–42 DAS', text:'Top-dress remaining fertilizer to meet reproductive-stage demand.'}
] AS mstage
MERGE (mt:Timing:Searchable {
  entity_id:  'Mechanized Fertilizer Timing - '+mstage.key,
  entity_type:'timing',
  name:       'Mechanized Timing '+mstage.key
})
SET mt.chapter     = 'Ch2',
    mt.source_id   = 'chunk-ch2-005',
    mt.description = mstage.text,
    mt.search_text = 'mechanized timing | '+mstage.key+' | '+mstage.text
MERGE (mech)-[:TIMED_AT {source_id:'chunk-ch2-005'}]->(mt)

// --- Fertilizer Types Used ---
WITH fert
UNWIND [
  {id:'NPK',  text:'Balanced fertilizer containing nitrogen (N), phosphorus (P), and potassium (K).'},
  {id:'DAP',  text:'Diammonium phosphate — source of phosphorus and nitrogen.'},
  {id:'KCl',  text:'Potassium chloride — potassium source for strong stems and grain filling.'},
  {id:'Urea', text:'High-nitrogen fertilizer, mainly during vegetative phases.'}
] AS fertype
MERGE (ftype:Input:Searchable {
  entity_id:  fertype.id,
  entity_type:'input',
  name:       fertype.id
})
SET ftype.chapter     = 'Ch2',
    ftype.source_id   = 'chunk-ch2-005',
    ftype.description = fertype.text,
    ftype.search_text = fertype.id+' | '+fertype.text+' | fertilizer type'
MERGE (fert)-[:USES {source_id:'chunk-ch2-005'}]->(ftype)

// --- Monitoring Tool ---
WITH fert
MERGE (tool:Tool:Searchable {
  entity_id:  'Leaf Color Chart',
  entity_type:'tool',
  name:       'Leaf Color Chart'
})
SET tool.chapter     = 'Ch2',
    tool.source_id   = 'chunk-ch2-005',
    tool.description = 'Color scale used to guide real-time nitrogen application based on leaf greenness; supports SSNM and avoids over/under dosing.',
    tool.search_text = 'leaf color chart | LCC | nitrogen adjustment | SSNM | real-time dose | avoid over-fertilization'
MERGE (fert)-[:MONITORED_BY {source_id:'chunk-ch2-005'}]->(tool)
"""
