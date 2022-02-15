# SQL queries

This docs logs the queries made in SQL to a local CAZyme database, in the search for suitable model CAZymes.

The local CAZyme database was created uing [`cazy_webscraper`](https://hobnobmancer.github.io/cazy_webscraper/). All bacterial proteins were retrieved from CAZy, and protein data (IDs, names, EC numbers and PDBs) were retrieved from UniProt for the following CAZy families: GH1, GH2, GH3, GH11, GH26, GH30, GH43, GH51, GH52, GH54, GH116, and GH120.

## 1. Number of bacterial proteins in specific CAZy families

**There are 40090 bacterial proteins in GH3.**

This query was performed against a local CAZyme database containing only proteins derived from bacteria.

```sql
SELECT COUNT(Genbanks.genbank_id)
FROM Genbanks
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
WHERE CazyFamilies.family = 'GH3'
```

To make the same query against a local CAZyme database with proteins derived from different taxonomic kingdoms, use the following query.

```sql
SELECT COUNT(Genbanks.genbank_id)
FROM Genbanks
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
INNER JOIN Kingdoms ON Taxs.kingdom_id = Kingdoms.kingdom_id
WHERE CazyFamilies.family = 'GH3' AND
	Kingdoms.kingdom = 'Bacteria'
```

From here on, we presume a local CAZyme database containing only bacterial proteins is used. If not, add the following lines to the command:

```sql
INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
INNER JOIN Kingdoms ON Taxs.kingdom_id = Kingdoms.kingdom_id
WHERE Kingdoms.kingdom = 'Bacteria'
```

To number of bacterial proteins across all CAZy families of interest was retrieved using the following command:
```sql
SELECT COUNT(DISTINCT Genbanks.genbank_accession)
FROM Genbanks
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
WHERE CazyFamilies.family = 'GH1' OR
CazyFamilies.family = 'GH2' OR
CazyFamilies.family = 'GH3' OR
CazyFamilies.family = 'GH11' OR
CazyFamilies.family = 'GH26' OR
CazyFamilies.family = 'GH30' OR
CazyFamilies.family = 'GH43' OR
CazyFamilies.family = 'GH51' OR
CazyFamilies.family = 'GH52' OR
CazyFamilies.family = 'GH54' OR
CazyFamilies.family = 'GH116' OR
CazyFamilies.family = 'GH120'
```
This identified **a** bacterial proteins as belonging to at least on of the CAZy families of interest.

## 2. Number of proteins annotated with the EC number EC 3.2.1.37

```sql
SELECT COUNT(DISTINCT Genbanks.genbank_accession)
FROM Genbanks
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
WHERE Ecs.ec_number = '3.2.1.37'
```

This identified CAZy contained **560** bacterial proteins annotated with the EC number 3.2.1.37.

The following command was used to identify the CAZy families to which these proteins belonged.

```sql
SELECT DISTINCT Genbanks.genbank_accession, CazyFamilies.family
FROM Genbanks
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
WHERE Ecs.ec_number = '3.2.1.37'
```

**75** of the protein belonged to GH3.

All EC 3.2.1.37 proteins were included across 13 families:  
**GHs:**  
- GH3
- GH5
- GH43
- GH51
- GH52
- GH54
- GH120  

**CMBs:**
- CBM2
- CBM5
- CBM6
- CBM13
- CBM22
- CBM42

The output from this query can be found [here](https://github.com/HobnobMancer/Foltanyi_et_al_2022/blob/master/sql_queries/query_2_ec_3-2-1-37_families.csv).

## 3. Get PDB accessions

The following command was used to retrieved the PDB accessions of all proteins annotated with the EC number 3.2.1.37.

```sql
SELECT DISTINCT Genbanks.genbank_accession, CazyFamilies.family, Pdbs.pdb_accession
FROM Genbanks
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
INNER JOIN Pdbs ON Genbanks.genbank_id = Pdbs.genbank_id
WHERE Ecs.ec_number = '3.2.1.37'
```

However, this returned 0 rows from the database. No bacterial proteins with the EC number 3.2.1.37 were associated with a PDB accession in UniProt.

Similarly, the following command was used to retrieve the PDB accessions of all proteins in The families containing proteins with the EC number 3.2.1.37.

```sql
SELECT DISTINCT Genbanks.genbank_accession, CazyFamilies.family, Pdbs.pdb_accession
FROM Genbanks
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
INNER JOIN Pdbs ON Genbanks.genbank_id = Pdbs.genbank_id
WHERE CazyFamilies.family = 'GH3' OR 
	CazyFamilies.family = 'GH5' OR
	CazyFamilies.family = 'GH43' OR
	CazyFamilies.family = 'GH51' OR
	CazyFamilies.family = 'GH52' OR
	CazyFamilies.family = 'GH54' OR
	CazyFamilies.family = 'GH120'
```

This returned **26 bacterial proteins** with PDB accessions listed in UniProt, all of which belonged ot GH3.

## 4. Protein name

Many CAZymes are not annotated with an EC number, but they are frequently given a named based upon their activity. Therefore, the local CAZyme database was queried for CAZymes 
containing any of the following phrases in their names:
- 'beta-xylosidase'
- 'Beta-xylosidase'
- 'beta-D-xylosidase'
- 'Beta-D-xylosidase'
- 'beta xylosidase'
- 'Beta xylosidase'
- 'beta D-xylosidase'
- 'Beta D-xylosidase'

This was achieved using the following command:

```sql
SELECT COUNT(DISTINCT Genbanks.genbank_accession)
FROM Genbanks
INNER JOIN Uniprots ON Genbanks.genbank_id = Uniprots.genbank_id
WHERE Uniprots.uniprot_name LIKE '%beta-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%beta-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%Beta-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%beta-D-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%Beta-D-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%beta xylosidase%' OR
  Uniprots.uniprot_name LIKE '%Beta xylosidase%' OR
  Uniprots.uniprot_name LIKE '%beta D-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%Beta D-xylosidase%'
```

This identified **145 bacterial proteins** in the database contained a variation of beta-xylosidase in their protein name.

The CAZy families of these proteins were identified using the following command:

```sql
SELECT DISTINCT Genbanks.genbank_accession, CazyFamilies.family
FROM Genbanks
INNER JOIN Uniprots ON Genbanks.genbank_id = Uniprots.genbank_id
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
WHERE Uniprots.uniprot_name LIKE '%beta-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%beta-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%Beta-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%beta-D-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%Beta-D-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%beta xylosidase%' OR
  Uniprots.uniprot_name LIKE '%Beta xylosidase%' OR
  Uniprots.uniprot_name LIKE '%beta D-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%Beta D-xylosidase%'
```

The output from this query can be found [here](https://github.com/HobnobMancer/Foltanyi_et_al_2022/blob/master/sql_queries/query_3_protein_names.csv).

All these proteins belonged to CAZy family GH3. Some proteins contained an additional CBM6 domain.

## 5. PDB accessions of beta-xylosidases

The following command was used to identify which proteins with a variation of the term 'beta-xylosidase' in their name were associated with PDB accessions in UniProt.

```sql
SELECT DISTINCT Genbanks.genbank_accession, CazyFamilies.family, Pdbs.pdb_accession
FROM Genbanks
INNER JOIN Uniprots ON Genbanks.genbank_id = Uniprots.genbank_id
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
INNER JOIN Pdbs ON Genbanks.genbank_id = Pdbs.genbank_id
WHERE Uniprots.uniprot_name LIKE '%beta-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%beta-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%Beta-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%beta-D-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%Beta-D-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%beta xylosidase%' OR
  Uniprots.uniprot_name LIKE '%Beta xylosidase%' OR
  Uniprots.uniprot_name LIKE '%beta D-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%Beta D-xylosidase%'
```

This returned 0 proteins.

## 6. EC and protein name overlap

The following command was used to identify which proteins were annotated with the EC number 3.2.1.37 *and* contained a variation of the term 'beta-xylosidase' in their protein name.

```sql
SELECT DISTINCT Genbanks.genbank_accession, Uniprots.uniprot_name, Ecs.ec_number
FROM Genbanks
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
INNER JOIN Uniprots ON Genbanks.genbank_id = Uniprots.genbank_id
WHERE Ecs.ec_number = '3.2.1.37' AND (
  Uniprots.uniprot_name LIKE '%beta-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%Beta-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%beta-D-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%Beta-D-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%beta xylosidase%' OR
  Uniprots.uniprot_name LIKE '%Beta xylosidase%' OR
  Uniprots.uniprot_name LIKE '%beta D-xylosidase%' OR
  Uniprots.uniprot_name LIKE '%Beta D-xylosidase%'
)
```

This returned 65 proteins, the results of which can be found [here](https://github.com/HobnobMancer/Foltanyi_et_al_2022/blob/master/sql_queries/query_6_name_ec.csv).

Therefore, 10 proteins annotated with the EC number 3.2.1.37 do not contain any variation of the term 'beta-xylosidase' in their protein name retrieved from UniProt. Also, 80 proteins containing a variation of the term 'beta-xylosidase' in their protein name are not annotated with the EC number 3.2.1.37. This does not take into account proteins annotated with an incomplete EC number which then later maybe completed to 3.2.1.37, i.e. their may currently be annotated with the EC number 3.2.1.-.

7. GenBank accessions with EC number and/or Name

The following SQL command was used to retrieve the GenBank accession of all proteins in the local bacterial CAZyme database with the EC number 3.2.1.37 *or* whose name contained any variation of the term 'beta-xylosidase':

```sql
WITH Ec_Query (ec_gbk_acc) AS (
	SELECT DISTINCT Genbanks.genbank_accession
	FROM Genbanks
	INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
	INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
	WHERE Ecs.ec_number = '3.2.1.37'
), Name_Query (name_gbk_acc) AS (
	SELECT DISTINCT Genbanks.genbank_accession
	FROM Genbanks
	INNER JOIN Uniprots ON Genbanks.genbank_id = Uniprots.genbank_id
	WHERE Uniprots.uniprot_name LIKE '%beta-xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%Beta-xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%beta-D-xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%Beta-D-xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%beta xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%Beta xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%beta D-xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%Beta D-xylosidase%'
)
SELECT DISTINCT Genbanks.genbank_accession
FROM Genbanks
LEFT JOIN Ec_Query ON Genbanks.genbank_accession = Ec_Query.ec_gbk_acc
LEFT JOIN Name_Query ON Genbanks.genbank_accession = Name_Query.name_gbk_acc
WHERE (Genbanks.genbank_accession IN Ec_Query) OR (Genbanks.genbank_accession IN Name_Query)
```

This retrieved **155 unique GenBank accessions**.

The following command was used to retrieve the GenBank accession of all proteins in the local bacterial CAZyme database with the EC number 3.2.1.37 *and* whose name contained any variation of the term 'beta-xylosidase':

```sql
WITH Ec_Query (ec_gbk_acc) AS (
	SELECT DISTINCT Genbanks.genbank_accession
	FROM Genbanks
	INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
	INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
	WHERE Ecs.ec_number = '3.2.1.37'
), Name_Query (name_gbk_acc) AS (
	SELECT DISTINCT Genbanks.genbank_accession
	FROM Genbanks
	INNER JOIN Uniprots ON Genbanks.genbank_id = Uniprots.genbank_id
	WHERE Uniprots.uniprot_name LIKE '%beta-xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%Beta-xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%beta-D-xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%Beta-D-xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%beta xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%Beta xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%beta D-xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%Beta D-xylosidase%'
)
SELECT DISTINCT Genbanks.genbank_accession
FROM Genbanks
LEFT JOIN Ec_Query ON Genbanks.genbank_accession = Ec_Query.ec_gbk_acc
LEFT JOIN Name_Query ON Genbanks.genbank_accession = Name_Query.name_gbk_acc
WHERE (Genbanks.genbank_accession IN Ec_Query) AND (Genbanks.genbank_accession IN Name_Query)
```

This retrieved **65 unique GenBank accessions**.

In total **220 unique GenBank accessions** were retrieved. The final list of GenBank accessions can be found [here](https://github.com/HobnobMancer/Foltanyi_et_al_2022/blob/master/data/ec_name_genbank_accessions.txt).

The GenBank accessions of the remaining GH3 proteins not included in the list of 220 EC number and/or named identified proteins were retrieved using the following command:

```sql
WITH Ec_Query (ec_gbk_acc) AS (
	SELECT DISTINCT Genbanks.genbank_accession
	FROM Genbanks
	INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
	INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
	WHERE Ecs.ec_number = '3.2.1.37'
), Name_Query (name_gbk_acc) AS (
	SELECT DISTINCT Genbanks.genbank_accession
	FROM Genbanks
	INNER JOIN Uniprots ON Genbanks.genbank_id = Uniprots.genbank_id
	WHERE Uniprots.uniprot_name LIKE '%beta-xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%Beta-xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%beta-D-xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%Beta-D-xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%beta xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%Beta xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%beta D-xylosidase%' OR
	  Uniprots.uniprot_name LIKE '%Beta D-xylosidase%'
)
SELECT DISTINCT Genbanks.genbank_accession
FROM Genbanks
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
LEFT JOIN Ec_Query ON Genbanks.genbank_accession = Ec_Query.ec_gbk_acc
LEFT JOIN Name_Query ON Genbanks.genbank_accession = Name_Query.name_gbk_acc
WHERE (Genbanks.genbank_accession NOT IN Ec_Query) AND (Genbanks.genbank_accession NOT IN Name_Query) AND (CazyFamilies.family = 'GH3')
```

This retrieved **39,935 unique GenBank accessions**. The list of these GenBank accessions can be found [here](https://github.com/HobnobMancer/Foltanyi_et_al_2022/blob/master/data/remaining_gh3.txt).

8. Retrieve PDB accessions for proteins in the final expanded protein pool

```sql
SELECT DISTINCT Genbanks.genbank_accession, Pdbs.pdb_accession
FROM Genbanks
INNER JOIN Pdbs ON Genbanks.genbank_id = Pdbs.genbank_id
WHERE Genbanks.genbank_accession = 'CCG44311.1' OR
Genbanks.genbank_accession = 'ARP42883.1' OR
Genbanks.genbank_accession = 'BAM46395.1' OR
Genbanks.genbank_accession = 'SQI53914.1' OR
Genbanks.genbank_accession = 'AFL93485.1' OR
Genbanks.genbank_accession = 'BAC15081.1' OR
Genbanks.genbank_accession = 'ABO67122.1' OR
Genbanks.genbank_accession = 'ALI16361.1' OR
Genbanks.genbank_accession = 'ADU28836.1' OR
Genbanks.genbank_accession = 'AWI11220.1' OR
Genbanks.genbank_accession = 'ACS99429.1' OR
Genbanks.genbank_accession = 'ARK32088.1' OR
Genbanks.genbank_accession = 'AGE22437.1' OR
Genbanks.genbank_accession = 'AAB41091.1' OR
Genbanks.genbank_accession = 'AAC27699.1' OR
Genbanks.genbank_accession = 'AFJ62036.1' OR
Genbanks.genbank_accession = 'QTG86872.1' OR
Genbanks.genbank_accession = 'AEP86745.1' OR
Genbanks.genbank_accession = 'QQZ02561.1' OR
Genbanks.genbank_accession = 'QRE01774.1' OR
Genbanks.genbank_accession = 'QCO69166.1' OR
Genbanks.genbank_accession = 'CDG29680.1' OR
Genbanks.genbank_accession = 'AAC97375.1' OR
Genbanks.genbank_accession = 'CAA29235.1' OR
Genbanks.genbank_accession = 'QEK65184.1' OR
Genbanks.genbank_accession = 'AFM43655.1' OR
Genbanks.genbank_accession = 'CAB13642.2' OR
Genbanks.genbank_accession = 'ARW39074.1' OR
Genbanks.genbank_accession = 'QTN97354.1' OR
Genbanks.genbank_accession = 'AYN44931.1' OR
Genbanks.genbank_accession = 'SQI91192.1' OR
Genbanks.genbank_accession = 'VEC60993.1' OR
Genbanks.genbank_accession = 'AAK05603.1' OR
Genbanks.genbank_accession = 'VEA69500.1' OR
Genbanks.genbank_accession = 'VEI66908.1' OR
Genbanks.genbank_accession = 'AOT56963.1' OR
Genbanks.genbank_accession = 'ASW23510.1' OR
Genbanks.genbank_accession = 'CBK69950.1' OR
Genbanks.genbank_accession = 'QIF87838.1' OR
Genbanks.genbank_accession = 'SQJ12668.1' OR
Genbanks.genbank_accession = 'CAE1148859.1' OR
Genbanks.genbank_accession = 'QCZ47082.1' OR
Genbanks.genbank_accession = 'SFZ86993.1' OR
Genbanks.genbank_accession = 'ALE36853.1' OR
Genbanks.genbank_accession = 'ADB09236.1' OR
Genbanks.genbank_accession = 'ACL29336.1' OR
Genbanks.genbank_accession = 'AEK29976.1' OR
Genbanks.genbank_accession = 'QOV58171.1' OR
Genbanks.genbank_accession = 'BBQ91616.1' OR
Genbanks.genbank_accession = 'QNT21370.1' OR
Genbanks.genbank_accession = 'VEI47713.1' OR
Genbanks.genbank_accession = 'VDZ59395.1' OR
Genbanks.genbank_accession = 'QBZ05673.1' OR
Genbanks.genbank_accession = 'ALI32240.1' OR
Genbanks.genbank_accession = 'ABX75762.2' OR
Genbanks.genbank_accession = 'QDI10504.1' OR
Genbanks.genbank_accession = 'VTP65858.1' OR
Genbanks.genbank_accession = 'ACA81905.1' OR
Genbanks.genbank_accession = 'QCZ54377.1' OR
Genbanks.genbank_accession = 'CBL13352.1' OR
Genbanks.genbank_accession = 'CBL10126.1' OR
Genbanks.genbank_accession = 'ACI06688.1' OR
Genbanks.genbank_accession = 'QHB62214.1' OR
Genbanks.genbank_accession = 'QJR15254.1' OR
Genbanks.genbank_accession = 'APG91432.1' OR
Genbanks.genbank_accession = 'ACS56603.1' OR
Genbanks.genbank_accession = 'AEG04639.1' OR
Genbanks.genbank_accession = 'ARM12734.1' OR
Genbanks.genbank_accession = 'QJR11213.1' OR
Genbanks.genbank_accession = 'AVA21776.1' OR
Genbanks.genbank_accession = 'AKI02785.1' OR
Genbanks.genbank_accession = 'AGS22247.1' OR
Genbanks.genbank_accession = 'ACE91508.1' OR
Genbanks.genbank_accession = 'APO67964.1' OR
Genbanks.genbank_accession = 'AUW42963.1' OR
Genbanks.genbank_accession = 'ANL22220.1' OR
Genbanks.genbank_accession = 'APO75144.1' OR
Genbanks.genbank_accession = 'ACP25531.1' OR
Genbanks.genbank_accession = 'ARM88787.1' OR
Genbanks.genbank_accession = 'ABC91230.1' OR
Genbanks.genbank_accession = 'AFL52732.1' OR
Genbanks.genbank_accession = 'AIC27686.1' OR
Genbanks.genbank_accession = 'AJD41574.1' OR
Genbanks.genbank_accession = 'APG84786.1' OR
Genbanks.genbank_accession = 'CAC46496.1' OR
Genbanks.genbank_accession = 'CCF19678.1' OR
Genbanks.genbank_accession = 'ARO30532.1' OR
Genbanks.genbank_accession = 'CDM57808.1' OR
Genbanks.genbank_accession = 'CCE96199.1' OR
Genbanks.genbank_accession = 'AJC79690.1' OR
Genbanks.genbank_accession = 'AUX76693.1' OR
Genbanks.genbank_accession = 'QFU07763.1' OR
Genbanks.genbank_accession = 'AGK03522.1' OR
Genbanks.genbank_accession = 'CCC57797.1' OR
Genbanks.genbank_accession = 'AMY08894.1' OR
Genbanks.genbank_accession = 'AMP81963.1' OR
Genbanks.genbank_accession = 'ALJ61528.1' OR
Genbanks.genbank_accession = 'AUX41205.1' OR
Genbanks.genbank_accession = 'QDI10558.1' OR
Genbanks.genbank_accession = 'CUH92713.1' OR
Genbanks.genbank_accession = 'QFT14636.1' OR
Genbanks.genbank_accession = 'BAD63094.1' OR
Genbanks.genbank_accession = 'ADV48176.1' OR
Genbanks.genbank_accession = 'ADY12355.1' OR
Genbanks.genbank_accession = 'ADU12331.1' OR
Genbanks.genbank_accession = 'SNV05241.1' OR
Genbanks.genbank_accession = 'AEF28829.1' OR
Genbanks.genbank_accession = 'VED48126.1' OR
Genbanks.genbank_accession = 'ADG11745.1' OR
Genbanks.genbank_accession = 'CUU51066.1' OR
Genbanks.genbank_accession = 'ACX65516.1' OR
Genbanks.genbank_accession = 'VDR25565.1' OR
Genbanks.genbank_accession = 'VTP63163.1' OR
Genbanks.genbank_accession = 'AJQ94568.1' OR
Genbanks.genbank_accession = 'CAZ98034.1' OR
Genbanks.genbank_accession = 'ADD27067.1' OR
Genbanks.genbank_accession = 'AAC73374.1' OR
Genbanks.genbank_accession = 'CBV41044.1' OR
Genbanks.genbank_accession = 'ADI00326.1' OR
Genbanks.genbank_accession = 'BAB07402.1' OR
Genbanks.genbank_accession = 'BAI98601.1' OR
Genbanks.genbank_accession = 'ACL94505.1' OR
Genbanks.genbank_accession = 'AFZ78871.1' OR
Genbanks.genbank_accession = 'ADN02785.1' OR
Genbanks.genbank_accession = 'AGF56005.1' OR
Genbanks.genbank_accession = 'AYJ44889.1' OR
Genbanks.genbank_accession = 'AEB06675.1' OR
Genbanks.genbank_accession = 'AHC15870.1' OR
Genbanks.genbank_accession = 'VED54572.1' OR
Genbanks.genbank_accession = 'AUX30763.1' OR
Genbanks.genbank_accession = 'AOS44921.1' OR
Genbanks.genbank_accession = 'QFT33870.1' OR
Genbanks.genbank_accession = 'AEG27967.1' OR
Genbanks.genbank_accession = 'CAN90282.1' OR
Genbanks.genbank_accession = 'CQR56345.1' OR
Genbanks.genbank_accession = 'AHY96139.1' OR
Genbanks.genbank_accession = 'QLV57883.1' OR
Genbanks.genbank_accession = 'BAE76055.1' OR
Genbanks.genbank_accession = 'AUX21502.1' OR
Genbanks.genbank_accession = 'ALI54194.1' OR
Genbanks.genbank_accession = 'AQZ51310.1' OR
Genbanks.genbank_accession = 'QEW19930.1' OR
Genbanks.genbank_accession = 'AOM83753.1' OR
Genbanks.genbank_accession = 'AEB13023.1' OR
Genbanks.genbank_accession = 'AEB30801.1' OR
Genbanks.genbank_accession = 'ADL52305.1' OR
Genbanks.genbank_accession = 'CQR57257.1' OR
Genbanks.genbank_accession = 'AKO99108.1' OR
Genbanks.genbank_accession = 'CAN95047.1' OR
Genbanks.genbank_accession = 'AFU70837.1'
```

No PDB accessions were retrieved.
