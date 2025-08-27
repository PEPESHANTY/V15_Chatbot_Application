// === Chapter 1 Central Node ===
MERGE (ch1:Chapter {
  entity_id: 'Purpose and Scope of Use - Ch1',
  entity_type: 'chapter',
  description: 'Overview of the One Million Hectares Project for high-quality, low-emission rice farming. Introduces technical domains, practices, and stakeholders.',
  created_at: timestamp(),
  file_path: 'book_1.pdf',
  source_id: 'chunk-ch1-001'
})
WITH ch1

// === Main Project Node ===
MERGE (proj:Project {
  entity_id: 'One Million Hectares Project',
  entity_type: 'project',
  description: 'Vietnamese government-backed project to develop 1 million hectares of climate-smart rice production by 2030.',
  source_id: 'chunk-ch1-001'
})
MERGE (proj)-[:APPROVED_BY {
  description: 'Approved under Decision No. 1490/QĐ-TTg by Prime Minister on Nov 27, 2023'
}]->(:Organization {
  entity_id: 'Vietnamese Government',
  entity_type: 'organization',
  name: 'Vietnamese Government'
})
MERGE (ch1)-[:FOCUSES_ON]->(proj)
WITH ch1, proj

// === Supporting Organizations ===
MERGE (irri:Organization {
  entity_id: 'International Rice Research Institute',
  entity_type: 'organization',
  name: 'International Rice Research Institute',
  description: 'Global rice research body supporting the handbook with technical input.',
  source_id: 'chunk-ch1-001'
})
MERGE (ch1)-[:SUPPORTED_BY]->(irri)

MERGE (dept:Organization {
  entity_id: 'Department of Crop Production',
  entity_type: 'organization',
  name: 'Department of Crop Production',
  description: 'Vietnam's Department of Crop Production that issued this guideline.',
  source_id: 'chunk-ch1-001'
})
MERGE (dept)-[:ISSUED]->(ch1)
WITH ch1, proj

// === Stakeholders ===
UNWIND [
  {id: 'Individual Farmers', desc: 'Smallholder rice growers'},
  {id: 'Agricultural Cooperatives', desc: 'Farmer-managed cooperatives'},
  {id: 'Farm Operators', desc: 'Professional rice farm managers'},
  {id: 'Agribusiness Enterprises', desc: 'Commercial rice value chain actors'}
] AS stakeholder
MERGE (s:StakeholderGroup {
  entity_id: stakeholder.id,
  entity_type: 'stakeholder',
  name: stakeholder.id,
  description: stakeholder.desc,
  source_id: 'chunk-ch1-001'
})
MERGE (ch1)-[:TARGETS]->(s)
WITH ch1, proj

// === Application Region ===
MERGE (region:Region {
  entity_id: 'Mekong Delta',
  name: 'Mekong Delta',
  description: 'Main target region for implementation of high-quality, low-emission rice systems.',
  source_id: 'chunk-ch1-001'
})
MERGE (proj)-[:IMPLEMENTED_IN {
  description: 'The One Million Hectares Project is implemented in this region.',
  weight: 9.0,
  source_id: 'chunk-ch1-001'
}]->(region)
WITH ch1

// === Technical Domains Introduced ===
UNWIND [
  'Cultivation Techniques',
  'Harvesting and Post-Harvest Management',
  'Straw Management'
] AS domain
MERGE (d:Practice {
  entity_id: domain,
  entity_type: 'domain',
  name: domain,
  description: 'Technical domain addressed in this chapter.',
  source_id: 'chunk-ch1-001'
})
MERGE (ch1)-[:COVERS]->(d)
WITH ch1

// === Core Practices Introduced ===
MERGE (land:Practice {
  entity_id: 'Land Preparation',
  description: 'Mechanized leveling and field prep based on cropping system.',
  source_id: 'chunk-ch1-001'
})
MERGE (water:Practice {
  entity_id: 'Water Management',
  description: 'Uses AWD to reduce GHG emissions; avoid stagnation > 30 days.',
  source_id: 'chunk-ch1-001'
})
MERGE (sowing:Practice {
  entity_id: 'Sowing Techniques',
  description: 'Broadcast or cluster sowing integrated with fertilizer placement.',
  source_id: 'chunk-ch1-001'
})
MERGE (fert:Practice {
  entity_id: 'Fertilization',
  description: 'Balanced fertilizer use aligned with crop needs, promotes organic fertilizer.',
  source_id: 'chunk-ch1-001'
})
MERGE (ipm:Practice {
  entity_id: 'Integrated Pest Management',
  description: '4 Rights principle + biological agents, avoid toxic pesticides.',
  source_id: 'chunk-ch1-001'
})
MERGE (harvest:Practice {
  entity_id: 'Harvesting and Post-Harvest Handling',
  description: 'Timely harvest using combine harvesters; modern drying/storage.',
  source_id: 'chunk-ch1-001'
})
MERGE (straw:Practice {
  entity_id: 'Straw Management',
  description: 'Incorporate straw with Trichoderma; reuse for compost, mushrooms, feed.',
  source_id: 'chunk-ch1-001'
})
FOREACH (p IN [land, water, sowing, fert, ipm, harvest, straw] |
  MERGE (ch1)-[:COVERS]->(p)
)
WITH ch1, water, straw, harvest, land, ipm

// === AWD inside Water Management ===
MERGE (awd:Acronym {
  entity_id: 'AWD',
  name: 'Alternate Wetting and Drying',
  description: 'Water-saving irrigation technique that reduces methane emissions.',
  source_id: 'chunk-ch1-001'
})
MERGE (awd)-[:USED_IN {
  description: 'AWD is a core method under water management for emission reduction.',
  source_id: 'chunk-ch1-001'
}]->(water)
WITH ch1, water, straw, harvest, land, ipm

// === Mechanization Concept ===
MERGE (mach:Concept {
  entity_id: 'Mechanization',
  description: 'Use of machines in leveling, sowing, and harvesting to lower emissions.',
  source_id: 'chunk-ch1-001'
})
MERGE (mach)-[:REDUCES]->(straw)
MERGE (mach)-[:REDUCES]->(water)
MERGE (mach)-[:USED_IN]->(harvest)
MERGE (mach)-[:USED_IN]->(land)
WITH ch1, straw, ipm, water

// === IPM Relationships ===
MERGE (bio:Input {
  entity_id: 'Biological Agents',
  name: 'Biological Agents',
  description: 'Eco-friendly pest controls like fungi, bacteria, parasitoids.',
  source_id: 'chunk-ch1-001'
})
MERGE (ipm)-[:USES]->(bio)

MERGE (tox:Chemical {
  entity_id: 'Toxic Synthetic Pesticides',
  description: 'Hazardous chemicals avoided in IPM.',
  source_id: 'chunk-ch1-001'
})
MERGE (ipm)-[:AVOIDS]->(tox)
WITH straw, water

// === Straw Use Cases ===
UNWIND [
  ['Mushroom Cultivation', 'Reuses straw as substrate in mushroom farming.'],
  ['Cattle Feed', 'Straw used as livestock feed, especially for buffaloes and cows.'],
  ['Organic Fertilizer', 'Straw composted into soil-enhancing fertilizer.']
] AS use
MERGE (u:UseCase {
  entity_id: use[0],
  name: use[0],
  description: use[1],
  source_id: 'chunk-ch1-001'
})
MERGE (straw)-[:REUSED_AS]->(u)
WITH straw, water

// === GHG Emissions ===
MERGE (ghg:Concept {
  entity_id: 'Greenhouse Gas Emissions',
  name: 'Greenhouse Gas Emissions',
  description: 'Methane and other emissions from rice fields targeted for reduction.',
  source_id: 'chunk-ch1-001'
})
MERGE (water)-[:REDUCES]->(ghg)
MERGE (straw)-[:REDUCES]->(ghg)
