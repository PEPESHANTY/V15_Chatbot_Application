cypher = """
MERGE (ch1:Chapter:Searchable {entity_id:'Ch1', entity_type:'chapter'})
SET ch1.name='Technical Guidelines for High-Quality and Low-Emission Rice Production — Chapter 1: Purpose & Scope',
    ch1.chapter='Ch1',
    ch1.file_path='book_1.pdf',
    ch1.source_id='chunk-ch1-001',
    ch1.summary='Purpose and scope of the handbook under the One Million Hectares Project (Decision 1490/QĐ-TTg, 27 Nov 2023).',
    ch1.description='Chapter 1 frames the handbook within the national One Million Hectares Project for high-quality, low-emission rice in the Mekong Delta. It consolidates technical standards across cultivation, harvesting, post-harvest handling, and circular straw management, with support from IRRI and based on Vietnam 2022/2023 guidelines, mechanization protocols, research, field-tested practices, and expert inputs. It clarifies target users (farmers, cooperatives, farm operators, agribusiness) and the main application area (specialized high-quality rice zones in the Mekong Delta), with adoption elsewhere where appropriate.',
    ch1.keywords=['One Million Hectares','Mekong Delta','Green Growth','Low emission','IRRI','Technical guidelines','Purpose','Scope'],
    ch1.search_text=ch1.name+' | '+ch1.summary+' | '+ch1.description+' | One Million Hectares | Mekong Delta | green growth | low emission | cultivation | harvesting | post-harvest | straw management'
WITH ch1
MERGE (proj:Project:Searchable {entity_id:'One Million Hectares Project', entity_type:'project'})
SET proj.name='One Million Hectares Project (High-Quality, Low-Emission Rice, Mekong Delta, by 2030)',
    proj.chapter='Ch1',
    proj.decision='1490/QĐ-TTg',
    proj.decision_date=date('2023-11-27'),
    proj.summary='National project to develop one million hectares of high-quality, low-emission rice by 2030.',
    proj.description='Approved by the Prime Minister under Decision 1490/QĐ-TTg (27 Nov 2023). Aligns rice production with green growth via standards for water (AWD), mechanized sowing, balanced fertilization, IPM, and circular straw management.',
    proj.keywords=['1M ha','Green growth','Low emission','Decision 1490/QĐ-TTg','2030','Mekong Delta'],
    proj.search_text=proj.name+' | '+proj.summary+' | '+proj.description+' | decision 1490 | 2030 | low emission | Mekong Delta'
WITH ch1, proj
MERGE (gov:Organization:Searchable {entity_id:'Vietnam Government', entity_type:'organization', name:'Vietnam Government'})
SET gov.chapter='Ch1',
    gov.summary='Approving authority for the One Million Hectares Project.',
    gov.description='Central government authority that approved Decision 1490/QĐ-TTg enabling the national project.',
    gov.search_text=gov.name+' | approving authority | Decision 1490 | One Million Hectares Project'
WITH ch1, proj, gov
MERGE (irri:Organization:Searchable {entity_id:'International Rice Research Institute', entity_type:'organization', name:'International Rice Research Institute'})
SET irri.chapter='Ch1',
    irri.summary='Technical supporter of the handbook.',
    irri.description='IRRI provided technical support on cultivation standards, water-saving (AWD), mechanized sowing, and low-emission practices for the Mekong Delta.',
    irri.search_text=irri.name+' | IRRI | technical support | AWD | mechanization | low emission'
WITH ch1, proj, gov, irri
MERGE (dept:Organization:Searchable {entity_id:'Department of Crop Production', entity_type:'organization', name:'Department of Crop Production'})
SET dept.chapter='Ch1',
    dept.summary='Issued the technical handbook.',
    dept.description='The Department of Crop Production issued the Technical Guidelines to operationalize the One Million Hectares Project.',
    dept.search_text=dept.name+' | handbook issuer | technical guidelines | One Million Hectares'
WITH ch1, proj, gov, irri, dept
MERGE (proj)-[:APPROVED_BY {description:'Approved under Decision 1490/QĐ-TTg on 2023-11-27'}]->(gov)
MERGE (dept)-[:ISSUED]->(ch1)
MERGE (irri)-[:SUPPORTED]->(ch1)
MERGE (ch1)-[:FOCUSES_ON]->(proj)
WITH ch1
UNWIND [
  {id:'Individual Farmers',        desc:'Smallholder rice growers who adopt field practices.'},
  {id:'Agricultural Cooperatives', desc:'Groups coordinating inputs, machinery, aggregation, and training.'},
  {id:'Farm Operators',            desc:'Professional operators managing larger areas or providing services.'},
  {id:'Agribusiness Enterprises',  desc:'Commercial value-chain actors in mechanization, logistics, processing, markets.'}
] AS stakeholder
MERGE (s:StakeholderGroup:Searchable {entity_id:stakeholder.id, entity_type:'stakeholder', name:stakeholder.id})
SET s.chapter='Ch1',
    s.description=stakeholder.desc,
    s.search_text=s.name+' | '+s.description+' | stakeholder | users | adoption'
MERGE (ch1)-[:TARGETS]->(s)
WITH ch1
MERGE (region:Region:Searchable {entity_id:'Mekong Delta', name:'Mekong Delta'})
SET region.chapter='Ch1',
    region.description='Primary application area: specialized high-quality rice zones in the Mekong Delta. Adoption elsewhere where appropriate.',
    region.search_text=region.name+' | specialized high-quality rice zones | Mekong Delta | application area'
WITH ch1, region
UNWIND ['Cultivation Techniques','Harvesting and Post-Harvest Management','Straw Management'] AS domain
MERGE (d:Practice:Searchable {entity_id:domain, entity_type:'domain', name:domain})
SET d.chapter='Ch1',
    d.description='Technical domain addressed in Chapter 1.',
    d.search_text=d.name+' | technical domain | Chapter 1 | guidelines'
MERGE (ch1)-[:COVERS]->(d)
WITH ch1
MERGE (land:Practice:Searchable {entity_id:'Land Preparation', name:'Land Preparation'})
SET land.chapter='Ch1',
    land.description='Mechanized (e.g., laser) leveling and field preparation tailored to cropping systems; supports uniform germination, AWD readiness, and mechanized sowing.',
    land.search_text=land.name+' | mechanized leveling | laser leveling | AWD readiness | uniform germination | cropping system'
WITH ch1, land
MERGE (water:Practice:Searchable {entity_id:'Water Management', name:'Water Management'})
SET water.chapter='Ch1',
    water.description='Alternate Wetting and Drying (AWD) with decision support (water tubes/gauges). Limit continuous water stagnation to fewer than 30 days post-sowing to cut methane and save water.',
    water.search_text=water.name+' | AWD | Alternate Wetting and Drying | methane reduction | water saving | <30 days stagnation | tubes | gauges'
WITH ch1, land, water
MERGE (sowing:Practice:Searchable {entity_id:'Sowing Techniques', name:'Sowing Techniques'})
SET sowing.chapter='Ch1',
    sowing.description='Mechanized broadcast or cluster sowing integrated with fertilizer deep placement/side-banding to improve nutrient use efficiency and reduce emissions.',
    sowing.search_text=sowing.name+' | mechanized broadcast | cluster sowing | fertilizer placement | deep placement | side-banding | NUE'
WITH ch1, land, water, sowing
MERGE (fert:Practice:Searchable {entity_id:'Fertilization', name:'Fertilization'})
SET fert.chapter='Ch1',
    fert.description='Balanced, season-aligned NPK and supplements; emphasize organic and environmentally friendly fertilizers to improve soil health and reduce emissions.',
    fert.search_text=fert.name+' | balanced NPK | organic fertilizers | soil health | low emission | season-aligned'
WITH ch1, land, water, sowing, fert
MERGE (ipm:Practice:Searchable {entity_id:'Integrated Pest Management', name:'Integrated Pest Management'})
SET ipm.chapter='Ch1',
    ipm.description='Follow the 4 Rights: right time, right product, right dosage, right method. Encourage biological agents; minimize toxic synthetic pesticides; aim for zero pesticide residues at harvest.',
    ipm.search_text=ipm.name+' | IPM | 4 Rights | biological control | zero residue | minimize toxic pesticides'
WITH ch1, land, water, sowing, fert, ipm
MERGE (harvest:Practice:Searchable {entity_id:'Harvesting and Post-Harvest Handling', name:'Harvesting and Post-Harvest Handling'})
SET harvest.chapter='Ch1',
    harvest.description='Harvest at optimal maturity using combine harvesters. Use efficient drying, storage, and transport to reduce energy use and post-harvest losses.',
    harvest.search_text=harvest.name+' | combine harvester | drying | storage | transport | loss reduction | energy efficiency'
WITH ch1, land, water, sowing, fert, ipm, harvest
MERGE (straw:Practice:Searchable {entity_id:'Straw Management', name:'Straw Management'})
SET straw.chapter='Ch1',
    straw.description='Shred and incorporate straw with Trichoderma-based composting agents when feasible. Reuse collected straw for mushroom cultivation, cattle feed, organic fertilizer, and other high-value products; avoid burning or burying raw straw.',
    straw.search_text=straw.name+' | straw incorporation | Trichoderma | mushroom cultivation | cattle feed | organic fertilizer | circular model | avoid burning'
WITH ch1, water, straw
MERGE (awd:Acronym:Searchable {entity_id:'AWD', name:'Alternate Wetting and Drying'})
SET awd.chapter='Ch1',
    awd.description='Water-saving irrigation technique that reduces methane emissions by allowing non-flooded periods.',
    awd.search_text=awd.name+' | AWD | water-saving | methane reduction | irrigation'
WITH ch1, water, straw, awd
MERGE (mach:Concept:Searchable {entity_id:'Mechanization', name:'Mechanization'})
SET mach.chapter='Ch1',
    mach.description='Use of machinery in leveling, sowing, and harvesting to improve efficiency and reduce emissions.',
    mach.search_text=mach.name+' | leveling | sowing | harvesting | efficiency | low emission'
WITH ch1, water, straw, awd, mach
MERGE (bio:Input:Searchable {entity_id:'Biological Agents', name:'Biological Agents'})
SET bio.chapter='Ch1',
    bio.description='Eco-friendly pest control agents (e.g., fungi, bacteria, parasitoids) preferred in IPM.',
    bio.search_text=bio.name+' | biological control | eco-friendly | IPM'
WITH ch1, water, straw, awd, mach, bio
MERGE (tox:Chemical:Searchable {entity_id:'Toxic Synthetic Pesticides', name:'Toxic Synthetic Pesticides'})
SET tox.chapter='Ch1',
    tox.description='Hazardous pesticides minimized under IPM and avoided where possible.',
    tox.search_text=tox.name+' | avoid | hazardous | IPM'
WITH ch1, water, straw, awd, mach, bio, tox
MERGE (ghg:Concept:Searchable {entity_id:'Greenhouse Gas Emissions', name:'Greenhouse Gas Emissions'})
SET ghg.chapter='Ch1',
    ghg.description='Methane and other emissions from rice fields targeted for reduction through AWD and straw circularity.',
    ghg.search_text=ghg.name+' | methane | emission reduction | rice fields'
WITH ch1, water, straw, awd, mach, bio, tox, ghg
UNWIND [
  ['Mushroom Cultivation','Reuse straw as substrate for mushroom production.'],
  ['Cattle Feed','Use straw as livestock feed for ruminants.'],
  ['Organic Fertilizer','Compost straw into soil-enhancing organic fertilizer.'],
  ['Other High-Value Uses','Other economic and environmental value applications.']
] AS use
MERGE (u:UseCase:Searchable {entity_id:use[0], name:use[0]})
SET u.chapter='Ch1',
    u.description=use[1],
    u.search_text=u.name+' | straw reuse | circular economy'
WITH ch1, water, straw, awd, mach, bio, tox, ghg
MERGE (ch1)-[:COVERS]->(:Practice {entity_id:'Cultivation Techniques'})
MERGE (ch1)-[:COVERS]->(:Practice {entity_id:'Harvesting and Post-Harvest Management'})
MERGE (ch1)-[:COVERS]->(:Practice {entity_id:'Straw Management'})
MERGE (awd)-[:USED_IN {description:'Core method under water management for emission reduction'}]->(water)
MERGE (mach)-[:REDUCES]->(straw)
MERGE (mach)-[:REDUCES]->(water)
MERGE (mach)-[:USED_IN]->(land)
MERGE (mach)-[:USED_IN]->(harvest)
MERGE (ipm)-[:USES]->(bio)
MERGE (ipm)-[:AVOIDS]->(tox)
MERGE (water)-[:REDUCES]->(ghg)
MERGE (straw)-[:REDUCES]->(ghg)
MERGE (straw)-[:REUSED_AS]->(:UseCase {entity_id:'Mushroom Cultivation'})
MERGE (straw)-[:REUSED_AS]->(:UseCase {entity_id:'Cattle Feed'})
MERGE (straw)-[:REUSED_AS]->(:UseCase {entity_id:'Organic Fertilizer'})
MERGE (straw)-[:REUSED_AS]->(:UseCase {entity_id:'Other High-Value Uses'})
"""

