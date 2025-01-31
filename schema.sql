CREATE TABLE IF NOT EXISTS "crpNPCCorporations" (
	"corporationID" INTEGER NOT NULL, 
	size CHAR(1), 
	extent CHAR(1), 
	"solarSystemID" INTEGER, 
	"investorID1" INTEGER, 
	"investorShares1" INTEGER, 
	"investorID2" INTEGER, 
	"investorShares2" INTEGER, 
	"investorID3" INTEGER, 
	"investorShares3" INTEGER, 
	"investorID4" INTEGER, 
	"investorShares4" INTEGER, 
	"friendID" INTEGER, 
	"enemyID" INTEGER, 
	"publicShares" INTEGER, 
	"initialPrice" INTEGER, 
	"minSecurity" FLOAT, 
	scattered BOOLEAN, 
	fringe INTEGER, 
	corridor INTEGER, 
	hub INTEGER, 
	border INTEGER, 
	"factionID" INTEGER, 
	"sizeFactor" FLOAT, 
	"stationCount" INTEGER, 
	"stationSystemCount" INTEGER, 
	description VARCHAR(4000), 
	"iconID" INTEGER, 
	PRIMARY KEY ("corporationID"), 
	CHECK (scattered IN (0, 1))
);
CREATE TABLE IF NOT EXISTS "staOperations" (
	"activityID" INTEGER, 
	"operationID" INTEGER NOT NULL, 
	"operationName" VARCHAR(100), 
	description VARCHAR(1000), 
	fringe INTEGER, 
	corridor INTEGER, 
	hub INTEGER, 
	border INTEGER, 
	ratio INTEGER, 
	"caldariStationTypeID" INTEGER, 
	"minmatarStationTypeID" INTEGER, 
	"amarrStationTypeID" INTEGER, 
	"gallenteStationTypeID" INTEGER, 
	"joveStationTypeID" INTEGER, 
	PRIMARY KEY ("operationID")
);
CREATE TABLE IF NOT EXISTS "invVolumes" (
	"typeID" INTEGER NOT NULL, 
	volume INTEGER, 
	PRIMARY KEY ("typeID")
);
CREATE TABLE IF NOT EXISTS "industryActivityProbabilities" (
	"typeID" INTEGER, 
	"activityID" INTEGER, 
	"productTypeID" INTEGER, 
	probability DECIMAL(3, 2)
);
CREATE INDEX "ix_industryActivityProbabilities_typeID" ON "industryActivityProbabilities" ("typeID");
CREATE INDEX "ix_industryActivityProbabilities_productTypeID" ON "industryActivityProbabilities" ("productTypeID");
CREATE TABLE IF NOT EXISTS "ramAssemblyLineStations" (
	"stationID" INTEGER NOT NULL, 
	"assemblyLineTypeID" INTEGER NOT NULL, 
	quantity INTEGER, 
	"stationTypeID" INTEGER, 
	"ownerID" INTEGER, 
	"solarSystemID" INTEGER, 
	"regionID" INTEGER, 
	PRIMARY KEY ("stationID", "assemblyLineTypeID")
);
CREATE INDEX "ix_ramAssemblyLineStations_ownerID" ON "ramAssemblyLineStations" ("ownerID");
CREATE INDEX "ix_ramAssemblyLineStations_solarSystemID" ON "ramAssemblyLineStations" ("solarSystemID");
CREATE INDEX "ix_ramAssemblyLineStations_regionID" ON "ramAssemblyLineStations" ("regionID");
CREATE TABLE IF NOT EXISTS "ramAssemblyLineTypes" (
	"assemblyLineTypeID" INTEGER NOT NULL, 
	"assemblyLineTypeName" VARCHAR(100), 
	description VARCHAR(1000), 
	"baseTimeMultiplier" FLOAT, 
	"baseMaterialMultiplier" FLOAT, 
	"baseCostMultiplier" FLOAT, 
	volume FLOAT, 
	"activityID" INTEGER, 
	"minCostPerHour" FLOAT, 
	PRIMARY KEY ("assemblyLineTypeID")
);
CREATE TABLE IF NOT EXISTS "invMarketGroups" (
	"marketGroupID" INTEGER NOT NULL, 
	"parentGroupID" INTEGER, 
	"marketGroupName" VARCHAR(100), 
	description VARCHAR(3000), 
	"iconID" INTEGER, 
	"hasTypes" BOOLEAN, 
	PRIMARY KEY ("marketGroupID"), 
	CHECK ("hasTypes" IN (0, 1))
);
CREATE TABLE IF NOT EXISTS "chrAttributes" (
	"attributeID" INTEGER NOT NULL, 
	"attributeName" VARCHAR(100), 
	description VARCHAR(1000), 
	"iconID" INTEGER, 
	"shortDescription" VARCHAR(500), 
	notes VARCHAR(500), 
	PRIMARY KEY ("attributeID")
);
CREATE TABLE IF NOT EXISTS "industryActivityProducts" (
	"typeID" INTEGER, 
	"activityID" INTEGER, 
	"productTypeID" INTEGER, 
	quantity INTEGER
);
CREATE INDEX "ix_industryActivityProducts_typeID" ON "industryActivityProducts" ("typeID");
CREATE INDEX "ix_industryActivityProducts_productTypeID" ON "industryActivityProducts" ("productTypeID");
CREATE TABLE IF NOT EXISTS "planetSchematicsPinMap" (
	"schematicID" INTEGER NOT NULL, 
	"pinTypeID" INTEGER NOT NULL, 
	PRIMARY KEY ("schematicID", "pinTypeID")
);
CREATE TABLE IF NOT EXISTS "mapRegionJumps" (
	"fromRegionID" INTEGER NOT NULL, 
	"toRegionID" INTEGER NOT NULL, 
	PRIMARY KEY ("fromRegionID", "toRegionID")
);
CREATE TABLE IF NOT EXISTS "skinMaterials" (
	"skinMaterialID" INTEGER NOT NULL, 
	"displayNameID" INTEGER, 
	"materialSetID" INTEGER, 
	PRIMARY KEY ("skinMaterialID")
);
CREATE TABLE IF NOT EXISTS "trnTranslationLanguages" (
	"numericLanguageID" INTEGER NOT NULL, 
	"languageID" VARCHAR(50), 
	"languageName" VARCHAR(200), 
	PRIMARY KEY ("numericLanguageID")
);
CREATE TABLE IF NOT EXISTS "trnTranslationColumns" (
	"tcGroupID" INTEGER, 
	"tcID" INTEGER NOT NULL, 
	"tableName" VARCHAR(256) NOT NULL, 
	"columnName" VARCHAR(128) NOT NULL, 
	"masterID" VARCHAR(128), 
	PRIMARY KEY ("tcID")
);
CREATE TABLE IF NOT EXISTS "eveIcons" (
	"iconID" INTEGER NOT NULL, 
	"iconFile" VARCHAR(500), 
	description TEXT, 
	PRIMARY KEY ("iconID")
);
CREATE TABLE IF NOT EXISTS "mapRegions" (
	"regionID" INTEGER NOT NULL, 
	"regionName" VARCHAR(100), 
	x FLOAT, 
	y FLOAT, 
	z FLOAT, 
	"xMin" FLOAT, 
	"xMax" FLOAT, 
	"yMin" FLOAT, 
	"yMax" FLOAT, 
	"zMin" FLOAT, 
	"zMax" FLOAT, 
	"factionID" INTEGER, 
	radius FLOAT, 
	PRIMARY KEY ("regionID")
);
CREATE TABLE IF NOT EXISTS "industryActivityRaces" (
	"typeID" INTEGER, 
	"activityID" INTEGER, 
	"productTypeID" INTEGER, 
	"raceID" INTEGER
);
CREATE INDEX "ix_industryActivityRaces_productTypeID" ON "industryActivityRaces" ("productTypeID");
CREATE INDEX "ix_industryActivityRaces_typeID" ON "industryActivityRaces" ("typeID");
CREATE TABLE skins (
	"skinID" INTEGER NOT NULL, 
	"internalName" VARCHAR(70), 
	"skinMaterialID" INTEGER, 
	PRIMARY KEY ("skinID")
);
CREATE TABLE IF NOT EXISTS "invTypeReactions" (
	"reactionTypeID" INTEGER NOT NULL, 
	input BOOLEAN NOT NULL, 
	"typeID" INTEGER NOT NULL, 
	quantity INTEGER, 
	PRIMARY KEY ("reactionTypeID", input, "typeID"), 
	CHECK (input IN (0, 1))
);
CREATE TABLE IF NOT EXISTS "eveUnits" (
	"unitID" INTEGER NOT NULL, 
	"unitName" VARCHAR(100), 
	"displayName" VARCHAR(50), 
	description VARCHAR(1000), 
	PRIMARY KEY ("unitID")
);
CREATE TABLE IF NOT EXISTS "agtAgentTypes" (
	"agentTypeID" INTEGER NOT NULL, 
	"agentType" VARCHAR(50), 
	PRIMARY KEY ("agentTypeID")
);
CREATE TABLE IF NOT EXISTS "planetSchematicsTypeMap" (
	"schematicID" INTEGER NOT NULL, 
	"typeID" INTEGER NOT NULL, 
	quantity INTEGER, 
	"isInput" BOOLEAN, 
	PRIMARY KEY ("schematicID", "typeID"), 
	CHECK ("isInput" IN (0, 1))
);
CREATE TABLE IF NOT EXISTS "ramInstallationTypeContents" (
	"installationTypeID" INTEGER NOT NULL, 
	"assemblyLineTypeID" INTEGER NOT NULL, 
	quantity INTEGER, 
	PRIMARY KEY ("installationTypeID", "assemblyLineTypeID")
);
CREATE TABLE IF NOT EXISTS "invUniqueNames" (
	"itemID" INTEGER NOT NULL, 
	"itemName" VARCHAR(200) NOT NULL, 
	"groupID" INTEGER, 
	PRIMARY KEY ("itemID")
);
CREATE INDEX "invUniqueNames_IX_GroupName" ON "invUniqueNames" ("groupID", "itemName");
CREATE UNIQUE INDEX "ix_invUniqueNames_itemName" ON "invUniqueNames" ("itemName");
CREATE TABLE IF NOT EXISTS "chrAncestries" (
	"ancestryID" INTEGER NOT NULL, 
	"ancestryName" VARCHAR(100), 
	"bloodlineID" INTEGER, 
	description VARCHAR(1000), 
	perception INTEGER, 
	willpower INTEGER, 
	charisma INTEGER, 
	memory INTEGER, 
	intelligence INTEGER, 
	"iconID" INTEGER, 
	"shortDescription" VARCHAR(500), 
	PRIMARY KEY ("ancestryID")
);
CREATE TABLE IF NOT EXISTS "mapLocationScenes" (
	"locationID" INTEGER NOT NULL, 
	"graphicID" INTEGER, 
	PRIMARY KEY ("locationID")
);
CREATE TABLE IF NOT EXISTS "invTypes" (
	"typeID" INTEGER NOT NULL, 
	"groupID" INTEGER, 
	"typeName" VARCHAR(100), 
	description TEXT, 
	mass FLOAT, 
	volume FLOAT, 
	capacity FLOAT, 
	"portionSize" INTEGER, 
	"raceID" INTEGER, 
	"basePrice" DECIMAL(19, 4), 
	published BOOLEAN, 
	"marketGroupID" INTEGER, 
	"iconID" INTEGER, 
	"soundID" INTEGER, 
	"graphicID" INTEGER, 
	PRIMARY KEY ("typeID"), 
	CHECK (published IN (0, 1))
);
CREATE INDEX "ix_invTypes_groupID" ON "invTypes" ("groupID");
CREATE TABLE IF NOT EXISTS "industryActivity" (
	"typeID" INTEGER NOT NULL, 
	"activityID" INTEGER NOT NULL, 
	time INTEGER, 
	PRIMARY KEY ("typeID", "activityID")
);
CREATE INDEX "ix_industryActivity_activityID" ON "industryActivity" ("activityID");
CREATE TABLE IF NOT EXISTS "invControlTowerResources" (
	"controlTowerTypeID" INTEGER NOT NULL, 
	"resourceTypeID" INTEGER NOT NULL, 
	purpose INTEGER, 
	quantity INTEGER, 
	"minSecurityLevel" FLOAT, 
	"factionID" INTEGER, 
	PRIMARY KEY ("controlTowerTypeID", "resourceTypeID")
);
CREATE TABLE IF NOT EXISTS "mapJumps" (
	"stargateID" INTEGER NOT NULL, 
	"destinationID" INTEGER, 
	PRIMARY KEY ("stargateID")
);
CREATE TABLE IF NOT EXISTS "certCerts" (
	"certID" INTEGER NOT NULL, 
	description TEXT, 
	"groupID" INTEGER, 
	name VARCHAR(255), 
	PRIMARY KEY ("certID")
);
CREATE TABLE IF NOT EXISTS "industryBlueprints" (
	"typeID" INTEGER NOT NULL, 
	"maxProductionLimit" INTEGER, 
	PRIMARY KEY ("typeID")
);
CREATE TABLE IF NOT EXISTS "invTypeMaterials" (
	"typeID" INTEGER NOT NULL, 
	"materialTypeID" INTEGER NOT NULL, 
	quantity INTEGER NOT NULL, 
	PRIMARY KEY ("typeID", "materialTypeID")
);
CREATE TABLE IF NOT EXISTS "ramAssemblyLineTypeDetailPerGroup" (
	"assemblyLineTypeID" INTEGER NOT NULL, 
	"groupID" INTEGER NOT NULL, 
	"timeMultiplier" FLOAT, 
	"materialMultiplier" FLOAT, 
	"costMultiplier" FLOAT, 
	PRIMARY KEY ("assemblyLineTypeID", "groupID")
);
CREATE TABLE IF NOT EXISTS "trnTranslations" (
	"tcID" INTEGER NOT NULL, 
	"keyID" INTEGER NOT NULL, 
	"languageID" VARCHAR(50) NOT NULL, 
	text TEXT NOT NULL, 
	PRIMARY KEY ("tcID", "keyID", "languageID")
);
CREATE TABLE IF NOT EXISTS "dgmAttributeTypes" (
	"attributeID" INTEGER NOT NULL, 
	"attributeName" VARCHAR(100), 
	description VARCHAR(1000), 
	"iconID" INTEGER, 
	"defaultValue" FLOAT, 
	published BOOLEAN, 
	"displayName" VARCHAR(150), 
	"unitID" INTEGER, 
	stackable BOOLEAN, 
	"highIsGood" BOOLEAN, 
	"categoryID" INTEGER, 
	PRIMARY KEY ("attributeID"), 
	CHECK (published IN (0, 1)), 
	CHECK (stackable IN (0, 1)), 
	CHECK ("highIsGood" IN (0, 1))
);
CREATE TABLE IF NOT EXISTS "agtResearchAgents" (
	"agentID" INTEGER NOT NULL, 
	"typeID" INTEGER NOT NULL, 
	PRIMARY KEY ("agentID", "typeID")
);
CREATE INDEX "ix_agtResearchAgents_typeID" ON "agtResearchAgents" ("typeID");
CREATE TABLE IF NOT EXISTS "mapSolarSystemJumps" (
	"fromRegionID" INTEGER, 
	"fromConstellationID" INTEGER, 
	"fromSolarSystemID" INTEGER NOT NULL, 
	"toSolarSystemID" INTEGER NOT NULL, 
	"toConstellationID" INTEGER, 
	"toRegionID" INTEGER, 
	PRIMARY KEY ("fromSolarSystemID", "toSolarSystemID")
);
CREATE TABLE IF NOT EXISTS "mapCelestialStatistics" (
	"celestialID" INTEGER NOT NULL, 
	temperature FLOAT, 
	"spectralClass" VARCHAR(10), 
	luminosity FLOAT, 
	age FLOAT, 
	life FLOAT, 
	"orbitRadius" FLOAT, 
	eccentricity FLOAT, 
	"massDust" FLOAT, 
	"massGas" FLOAT, 
	fragmented BOOLEAN, 
	density FLOAT, 
	"surfaceGravity" FLOAT, 
	"escapeVelocity" FLOAT, 
	"orbitPeriod" FLOAT, 
	"rotationRate" FLOAT, 
	locked BOOLEAN, 
	pressure FLOAT, 
	radius FLOAT, 
	mass INTEGER, 
	PRIMARY KEY ("celestialID"), 
	CHECK (fragmented IN (0, 1)), 
	CHECK (locked IN (0, 1))
);
CREATE TABLE IF NOT EXISTS "mapConstellationJumps" (
	"fromRegionID" INTEGER, 
	"fromConstellationID" INTEGER NOT NULL, 
	"toConstellationID" INTEGER NOT NULL, 
	"toRegionID" INTEGER, 
	PRIMARY KEY ("fromConstellationID", "toConstellationID")
);
CREATE TABLE IF NOT EXISTS "staServices" (
	"serviceID" INTEGER NOT NULL, 
	"serviceName" VARCHAR(100), 
	description VARCHAR(1000), 
	PRIMARY KEY ("serviceID")
);
CREATE TABLE IF NOT EXISTS "warCombatZoneSystems" (
	"solarSystemID" INTEGER NOT NULL, 
	"combatZoneID" INTEGER, 
	PRIMARY KEY ("solarSystemID")
);
CREATE TABLE IF NOT EXISTS "industryActivityMaterials" (
	"typeID" INTEGER, 
	"activityID" INTEGER, 
	"materialTypeID" INTEGER, 
	quantity INTEGER
);
CREATE INDEX "industryActivityMaterials_idx1" ON "industryActivityMaterials" ("typeID", "activityID");
CREATE INDEX "ix_industryActivityMaterials_typeID" ON "industryActivityMaterials" ("typeID");
CREATE TABLE IF NOT EXISTS "mapLandmarks" (
	"landmarkID" INTEGER NOT NULL, 
	"landmarkName" VARCHAR(100), 
	description TEXT, 
	"locationID" INTEGER, 
	x FLOAT, 
	y FLOAT, 
	z FLOAT, 
	"iconID" INTEGER, 
	PRIMARY KEY ("landmarkID")
);
CREATE TABLE IF NOT EXISTS "invFlags" (
	"flagID" INTEGER NOT NULL, 
	"flagName" VARCHAR(200), 
	"flagText" VARCHAR(100), 
	"orderID" INTEGER, 
	PRIMARY KEY ("flagID")
);
CREATE TABLE IF NOT EXISTS "mapSolarSystems" (
	"regionID" INTEGER, 
	"constellationID" INTEGER, 
	"solarSystemID" INTEGER NOT NULL, 
	"solarSystemName" VARCHAR(100), 
	x FLOAT, 
	y FLOAT, 
	z FLOAT, 
	"xMin" FLOAT, 
	"xMax" FLOAT, 
	"yMin" FLOAT, 
	"yMax" FLOAT, 
	"zMin" FLOAT, 
	"zMax" FLOAT, 
	luminosity FLOAT, 
	border BOOLEAN, 
	fringe BOOLEAN, 
	corridor BOOLEAN, 
	hub BOOLEAN, 
	international BOOLEAN, 
	regional BOOLEAN, 
	constellation BOOLEAN, 
	security FLOAT, 
	"factionID" INTEGER, 
	radius FLOAT, 
	"sunTypeID" INTEGER, 
	"securityClass" VARCHAR(2), 
	PRIMARY KEY ("solarSystemID"), 
	CHECK (border IN (0, 1)), 
	CHECK (fringe IN (0, 1)), 
	CHECK (corridor IN (0, 1)), 
	CHECK (hub IN (0, 1)), 
	CHECK (international IN (0, 1)), 
	CHECK (regional IN (0, 1)), 
	CHECK (constellation IN (0, 1))
);
CREATE INDEX "ix_mapSolarSystems_constellationID" ON "mapSolarSystems" ("constellationID");
CREATE INDEX "ix_mapSolarSystems_regionID" ON "mapSolarSystems" ("regionID");
CREATE INDEX "ix_mapSolarSystems_security" ON "mapSolarSystems" (security);
CREATE TABLE IF NOT EXISTS "invContrabandTypes" (
	"factionID" INTEGER NOT NULL, 
	"typeID" INTEGER NOT NULL, 
	"standingLoss" FLOAT, 
	"confiscateMinSec" FLOAT, 
	"fineByValue" FLOAT, 
	"attackMinSec" FLOAT, 
	PRIMARY KEY ("factionID", "typeID")
);
CREATE INDEX "ix_invContrabandTypes_typeID" ON "invContrabandTypes" ("typeID");
CREATE TABLE IF NOT EXISTS "invControlTowerResourcePurposes" (
	purpose INTEGER NOT NULL, 
	"purposeText" VARCHAR(100), 
	PRIMARY KEY (purpose)
);
CREATE TABLE IF NOT EXISTS "staStationTypes" (
	"stationTypeID" INTEGER NOT NULL, 
	"dockEntryX" FLOAT, 
	"dockEntryY" FLOAT, 
	"dockEntryZ" FLOAT, 
	"dockOrientationX" FLOAT, 
	"dockOrientationY" FLOAT, 
	"dockOrientationZ" FLOAT, 
	"operationID" INTEGER, 
	"officeSlots" INTEGER, 
	"reprocessingEfficiency" FLOAT, 
	conquerable BOOLEAN, 
	PRIMARY KEY ("stationTypeID"), 
	CHECK (conquerable IN (0, 1))
);
CREATE TABLE IF NOT EXISTS "invTraits" (
	"traitID" INTEGER NOT NULL, 
	"typeID" INTEGER, 
	"skillID" INTEGER, 
	bonus FLOAT, 
	"bonusText" TEXT, 
	"unitID" INTEGER, 
	PRIMARY KEY ("traitID")
);
CREATE TABLE IF NOT EXISTS "invPositions" (
	"itemID" INTEGER NOT NULL, 
	x FLOAT NOT NULL, 
	y FLOAT NOT NULL, 
	z FLOAT NOT NULL, 
	yaw FLOAT, 
	pitch FLOAT, 
	roll FLOAT, 
	PRIMARY KEY ("itemID")
);
CREATE TABLE IF NOT EXISTS "certSkills" (
	"certID" INTEGER, 
	"skillID" INTEGER, 
	"certLevelInt" INTEGER, 
	"skillLevel" INTEGER, 
	"certLevelText" VARCHAR(8)
);
CREATE INDEX "ix_certSkills_skillID" ON "certSkills" ("skillID");
CREATE TABLE IF NOT EXISTS "skinLicense" (
	"licenseTypeID" INTEGER NOT NULL, 
	duration INTEGER, 
	"skinID" INTEGER, 
	PRIMARY KEY ("licenseTypeID")
);
CREATE TABLE IF NOT EXISTS "dgmTypeAttributes" (
	"typeID" INTEGER NOT NULL, 
	"attributeID" INTEGER NOT NULL, 
	"valueInt" INTEGER, 
	"valueFloat" FLOAT, 
	PRIMARY KEY ("typeID", "attributeID")
);
CREATE INDEX "ix_dgmTypeAttributes_attributeID" ON "dgmTypeAttributes" ("attributeID");
CREATE TABLE IF NOT EXISTS "mapConstellations" (
	"regionID" INTEGER, 
	"constellationID" INTEGER NOT NULL, 
	"constellationName" VARCHAR(100), 
	x FLOAT, 
	y FLOAT, 
	z FLOAT, 
	"xMin" FLOAT, 
	"xMax" FLOAT, 
	"yMin" FLOAT, 
	"yMax" FLOAT, 
	"zMin" FLOAT, 
	"zMax" FLOAT, 
	"factionID" INTEGER, 
	radius FLOAT, 
	PRIMARY KEY ("constellationID")
);
CREATE TABLE IF NOT EXISTS "crpNPCCorporationDivisions" (
	"corporationID" INTEGER NOT NULL, 
	"divisionID" INTEGER NOT NULL, 
	size INTEGER, 
	PRIMARY KEY ("corporationID", "divisionID")
);
CREATE TABLE IF NOT EXISTS "dgmAttributeCategories" (
	"categoryID" INTEGER NOT NULL, 
	"categoryName" VARCHAR(50), 
	"categoryDescription" VARCHAR(200), 
	PRIMARY KEY ("categoryID")
);
CREATE TABLE IF NOT EXISTS "translationTables" (
	"sourceTable" VARCHAR(200) NOT NULL, 
	"destinationTable" VARCHAR(200), 
	"translatedKey" VARCHAR(200) NOT NULL, 
	"tcGroupID" INTEGER, 
	"tcID" INTEGER, 
	PRIMARY KEY ("sourceTable", "translatedKey")
);
CREATE TABLE IF NOT EXISTS "planetSchematics" (
	"schematicID" INTEGER NOT NULL, 
	"schematicName" VARCHAR(255), 
	"cycleTime" INTEGER, 
	PRIMARY KEY ("schematicID")
);
CREATE TABLE IF NOT EXISTS "invMetaTypes" (
	"typeID" INTEGER NOT NULL, 
	"parentTypeID" INTEGER, 
	"metaGroupID" INTEGER, 
	PRIMARY KEY ("typeID")
);
CREATE TABLE IF NOT EXISTS "certMasteries" (
	"typeID" INTEGER, 
	"masteryLevel" INTEGER, 
	"certID" INTEGER
);
CREATE TABLE IF NOT EXISTS "crpNPCCorporationResearchFields" (
	"skillID" INTEGER NOT NULL, 
	"corporationID" INTEGER NOT NULL, 
	PRIMARY KEY ("skillID", "corporationID")
);
CREATE TABLE IF NOT EXISTS "crpNPCDivisions" (
	"divisionID" INTEGER NOT NULL, 
	"divisionName" VARCHAR(100), 
	description VARCHAR(1000), 
	"leaderType" VARCHAR(100), 
	PRIMARY KEY ("divisionID")
);
CREATE TABLE IF NOT EXISTS "dgmTypeEffects" (
	"typeID" INTEGER NOT NULL, 
	"effectID" INTEGER NOT NULL, 
	"isDefault" BOOLEAN, 
	PRIMARY KEY ("typeID", "effectID"), 
	CHECK ("isDefault" IN (0, 1))
);
CREATE TABLE IF NOT EXISTS "invNames" (
	"itemID" INTEGER NOT NULL, 
	"itemName" VARCHAR(200) NOT NULL, 
	PRIMARY KEY ("itemID")
);
CREATE TABLE IF NOT EXISTS "mapDenormalize" (
	"itemID" INTEGER NOT NULL, 
	"typeID" INTEGER, 
	"groupID" INTEGER, 
	"solarSystemID" INTEGER, 
	"constellationID" INTEGER, 
	"regionID" INTEGER, 
	"orbitID" INTEGER, 
	x FLOAT, 
	y FLOAT, 
	z FLOAT, 
	radius FLOAT, 
	"itemName" VARCHAR(100), 
	security FLOAT, 
	"celestialIndex" INTEGER, 
	"orbitIndex" INTEGER, 
	PRIMARY KEY ("itemID")
);
CREATE INDEX "ix_mapDenormalize_regionID" ON "mapDenormalize" ("regionID");
CREATE INDEX "ix_mapDenormalize_solarSystemID" ON "mapDenormalize" ("solarSystemID");
CREATE INDEX "ix_mapDenormalize_orbitID" ON "mapDenormalize" ("orbitID");
CREATE INDEX "mapDenormalize_IX_groupSystem" ON "mapDenormalize" ("groupID", "solarSystemID");
CREATE INDEX "mapDenormalize_IX_groupConstellation" ON "mapDenormalize" ("groupID", "constellationID");
CREATE INDEX "ix_mapDenormalize_constellationID" ON "mapDenormalize" ("constellationID");
CREATE INDEX "mapDenormalize_IX_groupRegion" ON "mapDenormalize" ("groupID", "regionID");
CREATE INDEX "ix_mapDenormalize_typeID" ON "mapDenormalize" ("typeID");
CREATE TABLE IF NOT EXISTS "chrRaces" (
	"raceID" INTEGER NOT NULL, 
	"raceName" VARCHAR(100), 
	description VARCHAR(1000), 
	"iconID" INTEGER, 
	"shortDescription" VARCHAR(500), 
	PRIMARY KEY ("raceID")
);
CREATE TABLE IF NOT EXISTS "crpActivities" (
	"activityID" INTEGER NOT NULL, 
	"activityName" VARCHAR(100), 
	description VARCHAR(1000), 
	PRIMARY KEY ("activityID")
);
CREATE TABLE IF NOT EXISTS "chrFactions" (
	"factionID" INTEGER NOT NULL, 
	"factionName" VARCHAR(100), 
	description VARCHAR(1000), 
	"raceIDs" INTEGER, 
	"solarSystemID" INTEGER, 
	"corporationID" INTEGER, 
	"sizeFactor" FLOAT, 
	"stationCount" INTEGER, 
	"stationSystemCount" INTEGER, 
	"militiaCorporationID" INTEGER, 
	"iconID" INTEGER, 
	PRIMARY KEY ("factionID")
);
CREATE TABLE IF NOT EXISTS "eveGraphics" (
	"graphicID" INTEGER NOT NULL, 
	"sofFactionName" VARCHAR(100), 
	"graphicFile" VARCHAR(100), 
	"sofHullName" VARCHAR(100), 
	"sofRaceName" VARCHAR(100), 
	description TEXT, 
	PRIMARY KEY ("graphicID")
);
CREATE TABLE IF NOT EXISTS "invCategories" (
	"categoryID" INTEGER NOT NULL, 
	"categoryName" VARCHAR(100), 
	"iconID" INTEGER, 
	published BOOLEAN, 
	PRIMARY KEY ("categoryID"), 
	CHECK (published IN (0, 1))
);
CREATE TABLE IF NOT EXISTS "staStations" (
	"stationID" BIGINT NOT NULL, 
	security FLOAT, 
	"dockingCostPerVolume" FLOAT, 
	"maxShipVolumeDockable" FLOAT, 
	"officeRentalCost" INTEGER, 
	"operationID" INTEGER, 
	"stationTypeID" INTEGER, 
	"corporationID" INTEGER, 
	"solarSystemID" INTEGER, 
	"constellationID" INTEGER, 
	"regionID" INTEGER, 
	"stationName" VARCHAR(100), 
	x FLOAT, 
	y FLOAT, 
	z FLOAT, 
	"reprocessingEfficiency" FLOAT, 
	"reprocessingStationsTake" FLOAT, 
	"reprocessingHangarFlag" INTEGER, 
	PRIMARY KEY ("stationID")
);
CREATE INDEX "ix_staStations_solarSystemID" ON "staStations" ("solarSystemID");
CREATE INDEX "ix_staStations_constellationID" ON "staStations" ("constellationID");
CREATE INDEX "ix_staStations_stationTypeID" ON "staStations" ("stationTypeID");
CREATE INDEX "ix_staStations_corporationID" ON "staStations" ("corporationID");
CREATE INDEX "ix_staStations_regionID" ON "staStations" ("regionID");
CREATE INDEX "ix_staStations_operationID" ON "staStations" ("operationID");
CREATE TABLE IF NOT EXISTS "mapLocationWormholeClasses" (
	"locationID" INTEGER NOT NULL, 
	"wormholeClassID" INTEGER, 
	PRIMARY KEY ("locationID")
);
CREATE TABLE IF NOT EXISTS "invItems" (
	"itemID" INTEGER NOT NULL, 
	"typeID" INTEGER NOT NULL, 
	"ownerID" INTEGER NOT NULL, 
	"locationID" INTEGER NOT NULL, 
	"flagID" INTEGER NOT NULL, 
	quantity INTEGER NOT NULL, 
	PRIMARY KEY ("itemID")
);
CREATE INDEX "ix_invItems_locationID" ON "invItems" ("locationID");
CREATE INDEX "items_IX_OwnerLocation" ON "invItems" ("ownerID", "locationID");
CREATE TABLE IF NOT EXISTS "mapUniverse" (
	"universeID" INTEGER NOT NULL, 
	"universeName" VARCHAR(100), 
	x FLOAT, 
	y FLOAT, 
	z FLOAT, 
	"xMin" FLOAT, 
	"xMax" FLOAT, 
	"yMin" FLOAT, 
	"yMax" FLOAT, 
	"zMin" FLOAT, 
	"zMax" FLOAT, 
	radius FLOAT, 
	PRIMARY KEY ("universeID")
);
CREATE TABLE IF NOT EXISTS "skinShip" (
	"skinID" INTEGER, 
	"typeID" INTEGER
);
CREATE INDEX "ix_skinShip_skinID" ON "skinShip" ("skinID");
CREATE INDEX "ix_skinShip_typeID" ON "skinShip" ("typeID");
CREATE TABLE IF NOT EXISTS "crpNPCCorporationTrades" (
	"corporationID" INTEGER NOT NULL, 
	"typeID" INTEGER NOT NULL, 
	PRIMARY KEY ("corporationID", "typeID")
);
CREATE TABLE IF NOT EXISTS "chrBloodlines" (
	"bloodlineID" INTEGER NOT NULL, 
	"bloodlineName" VARCHAR(100), 
	"raceID" INTEGER, 
	description VARCHAR(1000), 
	"maleDescription" VARCHAR(1000), 
	"femaleDescription" VARCHAR(1000), 
	"shipTypeID" INTEGER, 
	"corporationID" INTEGER, 
	perception INTEGER, 
	willpower INTEGER, 
	charisma INTEGER, 
	memory INTEGER, 
	intelligence INTEGER, 
	"iconID" INTEGER, 
	"shortDescription" VARCHAR(500), 
	"shortMaleDescription" VARCHAR(500), 
	"shortFemaleDescription" VARCHAR(500), 
	PRIMARY KEY ("bloodlineID")
);
CREATE TABLE IF NOT EXISTS "warCombatZones" (
	"combatZoneID" INTEGER NOT NULL, 
	"combatZoneName" VARCHAR(100), 
	"factionID" INTEGER, 
	"centerSystemID" INTEGER, 
	description VARCHAR(500), 
	PRIMARY KEY ("combatZoneID")
);
CREATE TABLE IF NOT EXISTS "invMetaGroups" (
	"metaGroupID" INTEGER NOT NULL, 
	"metaGroupName" VARCHAR(100), 
	description VARCHAR(1000), 
	"iconID" INTEGER, 
	PRIMARY KEY ("metaGroupID")
);
CREATE TABLE IF NOT EXISTS "industryActivitySkills" (
	"typeID" INTEGER, 
	"activityID" INTEGER, 
	"skillID" INTEGER, 
	level INTEGER
);
CREATE INDEX "ix_industryActivitySkills_skillID" ON "industryActivitySkills" ("skillID");
CREATE INDEX "ix_industryActivitySkills_typeID" ON "industryActivitySkills" ("typeID");
CREATE INDEX "industryActivitySkills_idx1" ON "industryActivitySkills" ("typeID", "activityID");
CREATE TABLE IF NOT EXISTS "staOperationServices" (
	"operationID" INTEGER NOT NULL, 
	"serviceID" INTEGER NOT NULL, 
	PRIMARY KEY ("operationID", "serviceID")
);
CREATE TABLE IF NOT EXISTS "dgmEffects" (
	"effectID" INTEGER NOT NULL, 
	"effectName" VARCHAR(400), 
	"effectCategory" INTEGER, 
	"preExpression" INTEGER, 
	"postExpression" INTEGER, 
	description VARCHAR(1000), 
	guid VARCHAR(60), 
	"iconID" INTEGER, 
	"isOffensive" BOOLEAN, 
	"isAssistance" BOOLEAN, 
	"durationAttributeID" INTEGER, 
	"trackingSpeedAttributeID" INTEGER, 
	"dischargeAttributeID" INTEGER, 
	"rangeAttributeID" INTEGER, 
	"falloffAttributeID" INTEGER, 
	"disallowAutoRepeat" BOOLEAN, 
	published BOOLEAN, 
	"displayName" VARCHAR(100), 
	"isWarpSafe" BOOLEAN, 
	"rangeChance" BOOLEAN, 
	"electronicChance" BOOLEAN, 
	"propulsionChance" BOOLEAN, 
	distribution INTEGER, 
	"sfxName" VARCHAR(20), 
	"npcUsageChanceAttributeID" INTEGER, 
	"npcActivationChanceAttributeID" INTEGER, 
	"fittingUsageChanceAttributeID" INTEGER, 
	"modifierInfo" TEXT, 
	PRIMARY KEY ("effectID"), 
	CHECK ("isOffensive" IN (0, 1)), 
	CHECK ("isAssistance" IN (0, 1)), 
	CHECK ("disallowAutoRepeat" IN (0, 1)), 
	CHECK (published IN (0, 1)), 
	CHECK ("isWarpSafe" IN (0, 1)), 
	CHECK ("rangeChance" IN (0, 1)), 
	CHECK ("electronicChance" IN (0, 1)), 
	CHECK ("propulsionChance" IN (0, 1))
);
CREATE TABLE IF NOT EXISTS "ramAssemblyLineTypeDetailPerCategory" (
	"assemblyLineTypeID" INTEGER NOT NULL, 
	"categoryID" INTEGER NOT NULL, 
	"timeMultiplier" FLOAT, 
	"materialMultiplier" FLOAT, 
	"costMultiplier" FLOAT, 
	PRIMARY KEY ("assemblyLineTypeID", "categoryID")
);
CREATE TABLE IF NOT EXISTS "dgmExpressions" (
	"expressionID" INTEGER NOT NULL, 
	"operandID" INTEGER, 
	arg1 INTEGER, 
	arg2 INTEGER, 
	"expressionValue" VARCHAR(100), 
	description VARCHAR(1000), 
	"expressionName" VARCHAR(500), 
	"expressionTypeID" INTEGER, 
	"expressionGroupID" INTEGER, 
	"expressionAttributeID" INTEGER, 
	PRIMARY KEY ("expressionID")
);
CREATE TABLE IF NOT EXISTS "ramActivities" (
	"activityID" INTEGER NOT NULL, 
	"activityName" VARCHAR(100), 
	"iconNo" VARCHAR(5), 
	description VARCHAR(1000), 
	published BOOLEAN, 
	PRIMARY KEY ("activityID"), 
	CHECK (published IN (0, 1))
);
CREATE TABLE IF NOT EXISTS "agtAgents" (
	"agentID" INTEGER NOT NULL, 
	"divisionID" INTEGER, 
	"corporationID" INTEGER, 
	"locationID" INTEGER, 
	level INTEGER, 
	quality INTEGER, 
	"agentTypeID" INTEGER, 
	"isLocator" BOOLEAN, 
	PRIMARY KEY ("agentID"), 
	CHECK ("isLocator" IN (0, 1))
);
CREATE INDEX "ix_agtAgents_corporationID" ON "agtAgents" ("corporationID");
CREATE INDEX "ix_agtAgents_locationID" ON "agtAgents" ("locationID");
CREATE TABLE IF NOT EXISTS "invGroups" (
	"groupID" INTEGER NOT NULL, 
	"categoryID" INTEGER, 
	"groupName" VARCHAR(100), 
	"iconID" INTEGER, 
	"useBasePrice" BOOLEAN, 
	anchored BOOLEAN, 
	anchorable BOOLEAN, 
	"fittableNonSingleton" BOOLEAN, 
	published BOOLEAN, 
	PRIMARY KEY ("groupID"), 
	CHECK ("useBasePrice" IN (0, 1)), 
	CHECK (anchored IN (0, 1)), 
	CHECK (anchorable IN (0, 1)), 
	CHECK ("fittableNonSingleton" IN (0, 1)), 
	CHECK (published IN (0, 1))
);
CREATE INDEX "ix_invGroups_categoryID" ON "invGroups" ("categoryID");
