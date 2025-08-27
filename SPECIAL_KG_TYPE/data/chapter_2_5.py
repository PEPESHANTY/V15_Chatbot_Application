cypher = """

// =======================================
// Chapter 2 (Part 5) — Fertilizer Management (Mekong Delta)
// Single-statement, idempotent upsert with :Searchable + search_text
// + Guideline rules (soil/season/timing/mechanized/lime/organic)
// =======================================

MERGE (ch2:Chapter {entity_id:'Cultivation Techniques - Ch2'})

// --- Root practice node (:Searchable) ---
MERGE (fert:Practice:Searchable {
  entity_id:  'Fertilizer Management - Ch2',
  entity_type:'practice',
  name:       'Fertilizer Management'
})
SET fert.chapter     = 'Ch2',
    fert.source_id   = 'chunk-ch2-005',
    fert.description = 'Mekong Delta rice fertilization: SSNM (soil analysis every 5 years), organic + inorganic inputs, mechanized deep placement, soil/season-specific rates; targets root health, yield, and input efficiency.',
    fert.search_text = 'fertilizer management | Mekong Delta | SSNM | site-specific nutrient management | soil analysis 5 years | organic 1.5–3 t/ha | lime 200–300 kg/ha pH 4.0–5.0 | lime 400–500 kg/ha pH<4.0 | alluvial | acid sulfate | NPK | DAP | KCl | urea | mechanized deep placement | reduce N 10–15% | timing 7–10, 18–22, 38–42 DAS'
MERGE (ch2)-[:COVERS {source_id:'chunk-ch2-005'}]->(fert)

// --- SSNM (:Searchable) ---
WITH ch2, fert
MERGE (ssnm:Technique:Searchable {
  entity_id:  'Site-Specific Nutrient Management',
  entity_type:'method',
  name:       'Site-Specific Nutrient Management (SSNM)'
})
SET ssnm.chapter     = 'Ch2',
    ssnm.source_id   = 'chunk-ch2-005',
    ssnm.description = 'Match fertilizer to field and season; recalibrate with soil analysis every 5 years to address limiting nutrients and reduce losses.',
    ssnm.search_text = 'SSNM | site-specific | soil analysis every 5 years | tailor to season | reduce loss | improve NUE'
MERGE (fert)-[:USES {source_id:'chunk-ch2-005'}]->(ssnm)

// --- Organic fertilizer (:Searchable) ---
WITH ch2, fert
MERGE (organic:Input:Searchable {
  entity_id:  'Organic Fertilizer',
  entity_type:'input',
  name:       'Organic Fertilizer'
})
SET organic.chapter     = 'Ch2',
    organic.source_id   = 'chunk-ch2-005',
    organic.description = 'Apply 1.5–3 t/ha to enhance microbial activity and soil physical structure; supports resilience and yield.',
    organic.search_text = 'organic fertilizer | 1.5–3 t/ha | microbial activity | soil structure | resilience'
MERGE (fert)-[:USES {source_id:'chunk-ch2-005'}]->(organic)

// --- Lime (:Searchable) ---
WITH ch2, fert
MERGE (lime:Input:Searchable {
  entity_id:  'Lime',
  entity_type:'input',
  name:       'Lime (pH management)'
})
SET lime.chapter     = 'Ch2',
    lime.source_id   = 'chunk-ch2-005',
    lime.description = 'Neutralizes acidity: 200–300 kg/ha for pHₖCl 4.0–5.0; 400–500 kg/ha for pHₖCl < 4.0 (highly acidic/alum soils).',
    lime.search_text = 'lime | pH management | 200–300 kg/ha pH 4.0–5.0 | 400–500 kg/ha pH<4.0 | acid sulfate soils'
MERGE (fert)-[:USES {source_id:'chunk-ch2-005'}]->(lime)

// --- Utility data: Seasons & SoilTypes (not :Searchable) ---
WITH ch2, fert
UNWIND ['Winter–Spring','Summer–Autumn','Autumn–Winter'] AS sName
MERGE (:Season {name:sName})
WITH ch2, fert
UNWIND ['Alluvial Soil','Light Acid Sulfate Soil','Medium Acid Sulfate Soil'] AS stName
MERGE (:SoilType {name:stName})

// --- Soil-specific totals for Winter–Spring (Guideline + NutrientTotal) ---
WITH ch2, fert
UNWIND [
  {soil:'Alluvial Soil',            Nmin:90, Nmax:100, Pmin:30, Pmax:40, Kmin:30, Kmax:40},
  {soil:'Light Acid Sulfate Soil',  Nmin:80, Nmax:100, Pmin:40, Pmax:50, Kmin:25, Kmax:30},
  {soil:'Medium Acid Sulfate Soil', Nmin:68, Nmax:80,  Pmin:50, Pmax:60, Kmin:25, Kmax:30}
] AS rec
MERGE (ws:Season {name:'Winter–Spring'})
MERGE (stype:SoilType {name:rec.soil})
MERGE (g:Guideline:Searchable { entity_id:'G_WS_'+replace(rec.soil,' ','_'), entity_type:'guideline', name:'WS totals for '+rec.soil })
SET g.chapter='Ch2',
    g.source_id='chunk-ch2-005',
    g.description='Winter–Spring per-hectare totals for '+rec.soil+': N '+rec.Nmin+'–'+rec.Nmax+' kg, P₂O₅ '+rec.Pmin+'–'+rec.Pmax+' kg, K₂O '+rec.Kmin+'–'+rec.Kmax+' kg.',
    g.search_text='guideline | Winter–Spring | '+rec.soil+' | N '+rec.Nmin+'–'+rec.Nmax+' | P2O5 '+rec.Pmin+'–'+rec.Pmax+' | K2O '+rec.Kmin+'–'+rec.Kmax
MERGE (g)-[:APPLIES_WHEN]->(ws)
MERGE (g)-[:APPLIES_WHEN]->(stype)
MERGE (tot:NutrientTotal {id:'Total_'+g.entity_id})
SET tot.N_min=rec.Nmin, tot.N_max=rec.Nmax, tot.P2O5_min=rec.Pmin, tot.P2O5_max=rec.Pmax, tot.K2O_min=rec.Kmin, tot.K2O_max=rec.Kmax
MERGE (g)-[:RECOMMENDS]->(tot)
MERGE (fert)-[:HAS_RECOMMENDATION {source_id:'chunk-ch2-005'}]->(g)

// --- Conventional 3-split timings (Searchable Timing nodes) ---
WITH ch2, fert
UNWIND [
  {key:'7–10 DAS',  text:'Apply 40% of total N at 7–10 DAS to support seedling establishment.', fracN:0.40, fracK:0.00, method:'Broadcast'},
  {key:'18–22 DAS', text:'Apply 40% N and 40% K₂O during tillering for vegetative growth.',   fracN:0.40, fracK:0.40, method:'Topdress'},
  {key:'38–42 DAS', text:'Apply remaining 20% N and 60% K₂O for panicle formation & grain filling.', fracN:0.20, fracK:0.60, method:'Topdress'}
] AS s
MERGE (t:Timing:Searchable {
  entity_id:  'Fertilizer Timing - '+s.key,
  entity_type:'timing',
  name:       'Fertilizer Timing '+s.key
})
SET t.chapter='Ch2',
    t.source_id='chunk-ch2-005',
    t.description=s.text,
    t.search_text='fertilizer timing | '+s.key+' | '+s.text
MERGE (fert)-[:TIMED_AT {source_id:'chunk-ch2-005'}]->(t)

// Also attach the split apps to each WS guideline for clarity
WITH ch2, fert
UNWIND [
  {soil:'Alluvial Soil', key:'7–10 DAS',  fracN:0.40, fracK:0.00, method:'Broadcast'},
  {soil:'Alluvial Soil', key:'18–22 DAS', fracN:0.40, fracK:0.40, method:'Topdress'},
  {soil:'Alluvial Soil', key:'38–42 DAS', fracN:0.20, fracK:0.60, method:'Topdress'},
  {soil:'Light Acid Sulfate Soil', key:'7–10 DAS',  fracN:0.40, fracK:0.00, method:'Broadcast'},
  {soil:'Light Acid Sulfate Soil', key:'18–22 DAS', fracN:0.40, fracK:0.40, method:'Topdress'},
  {soil:'Light Acid Sulfate Soil', key:'38–42 DAS', fracN:0.20, fracK:0.60, method:'Topdress'},
  {soil:'Medium Acid Sulfate Soil', key:'7–10 DAS',  fracN:0.40, fracK:0.00, method:'Broadcast'},
  {soil:'Medium Acid Sulfate Soil', key:'18–22 DAS', fracN:0.40, fracK:0.40, method:'Topdress'},
  {soil:'Medium Acid Sulfate Soil', key:'38–42 DAS', fracN:0.20, fracK:0.60, method:'Topdress'}
] AS link
MATCH (g:Guideline {entity_id:'G_WS_'+replace(link.soil,' ','_')})
MATCH (t:Timing {name:'Fertilizer Timing '+link.key})
MERGE (app:FertilizerApplication {id: 'App_'+g.entity_id+'_'+replace(link.key,' ','_')})
SET app.fraction_N=link.fracN, app.fraction_K2O=link.fracK, app.method=link.method
MERGE (g)-[:RECOMMENDS]->(app)
MERGE (app)-[:AT]->(t)

// --- Seasonal N reduction guidelines (Searchable) ---
WITH ch2, fert
UNWIND ['Summer–Autumn','Autumn–Winter'] AS sName
MERGE (ssn:Season {name:sName})
MERGE (adj:Guideline:Searchable { entity_id:'G_'+replace(sName,' ','_')+'_N_Reduction', entity_type:'guideline', name:sName+' N reduction' })
SET adj.chapter='Ch2',
    adj.source_id='chunk-ch2-005',
    adj.description='Reduce N by 15–20% vs Winter–Spring due to higher volatilization and changing crop demand.',
    adj.search_text='seasonal adjustment | '+sName+' | reduce N 15–20% | volatilization | demand',
    adj.N_percent_min = -0.20,
    adj.N_percent_max = -0.15
MERGE (adj)-[:APPLIES_WHEN]->(ssn)
MERGE (fert)-[:ADJUSTS_FOR {source_id:'chunk-ch2-005'}]->(adj)

// --- Mechanized burial guideline + two-stage split (Searchable) ---
WITH ch2, fert
MERGE (mech:Guideline:Searchable {
  entity_id:  'G_Mechanized_Burial',
  entity_type:'guideline',
  name:       'Mechanized Fertilizer Management (Burial)'
})
SET mech.chapter     = 'Ch2',
    mech.source_id   = 'chunk-ch2-005',
    mech.description = 'Row/cluster sowing with fertilizer burial: reduce N by 10–15%; use 2–4 mm slow-dissolving granules; two-stage split (70–80% at sowing, remainder at 38–42 DAS).',
    mech.search_text = 'mechanized | fertilizer burial | reduce N 10–15% | 2–4 mm granules | two-stage split | 70–80% at sowing | 38–42 DAS',
    mech.N_percent_min = -0.15,
    mech.N_percent_max = -0.10,
    mech.mechanized = true
MERGE (fert)-[:MODIFIED_BY {source_id:'chunk-ch2-005'}]->(mech)
MERGE (tSow:Timing:Searchable {
  entity_id:'Mechanized Fertilizer Timing - At Sowing',
  entity_type:'timing',
  name:'Mechanized Timing At Sowing'
})
SET tSow.chapter='Ch2', tSow.source_id='chunk-ch2-005',
    tSow.description='Apply 70–80% of total fertilizer at sowing; bury with the machine (deep placement).',
    tSow.search_text='mechanized timing | At Sowing | 70–80% buried | deep placement'
MERGE (tLate:Timing:Searchable {
  entity_id:'Mechanized Fertilizer Timing - 38–42 DAS',
  entity_type:'timing',
  name:'Mechanized Timing 38–42 DAS'
})
SET tLate.chapter='Ch2', tLate.source_id='chunk-ch2-005',
    tLate.description='Top-dress remaining fertilizer to meet reproductive-stage demand.',
    tLate.search_text='mechanized timing | 38–42 DAS | topdress remainder'
MERGE (app1:FertilizerApplication {id:'App_Mech_Stage1'})
SET app1.stage_split='TwoStage', app1.stage1_fraction=0.75, app1.method='Buried', app1.placement_depth_cm=2, app1.granule_size_min_mm=2, app1.granule_size_max_mm=4
MERGE (app2:FertilizerApplication {id:'App_Mech_Stage2'})
SET app2.stage2_fraction=0.25, app2.method='Topdress'
MERGE (mech)-[:RECOMMENDS]->(app1)
MERGE (mech)-[:RECOMMENDS]->(app2)
MERGE (app1)-[:AT]->(tSow)
MERGE (app2)-[:AT]->(tLate)

// --- Fertilizer product types (:Searchable) ---
WITH ch2, fert
UNWIND [
  {id:'NPK',  text:'Balanced fertilizer with N, P, K.'},
  {id:'DAP',  text:'Diammonium phosphate — source of P and N.'},
  {id:'KCl',  text:'Potassium chloride — potassium source for strong stems and grain filling.'},
  {id:'Urea', text:'High-N fertilizer, mainly for vegetative phases.'}
] AS f
MERGE (ftype:Input:Searchable {
  entity_id:  f.id,
  entity_type:'input',
  name:       f.id
})
SET ftype.chapter     = 'Ch2',
    ftype.source_id   = 'chunk-ch2-005',
    ftype.description = f.text,
    ftype.search_text = f.id+' | '+f.text+' | fertilizer type'
MERGE (fert)-[:USES {source_id:'chunk-ch2-005'}]->(ftype)

// --- Monitoring tool (LCC) (:Searchable) ---
WITH ch2, fert
MERGE (tool:Tool:Searchable {
  entity_id:  'Leaf Color Chart',
  entity_type:'tool',
  name:       'Leaf Color Chart'
})
SET tool.chapter     = 'Ch2',
    tool.source_id   = 'chunk-ch2-005',
    tool.description = 'Leaf Color Chart (LCC) guides real-time N application based on leaf greenness; supports SSNM and avoids over/under dosing.',
    tool.search_text = 'leaf color chart | LCC | nitrogen adjustment | SSNM | real-time dose | avoid over-fertilization'
MERGE (fert)-[:MONITORED_BY {source_id:'chunk-ch2-005'}]->(tool)

// Done
RETURN 'ok' AS status;


"""