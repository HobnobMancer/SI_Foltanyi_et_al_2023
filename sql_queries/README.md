# SQL queries

This doc lists the queries made in SQL to a local CAZyme database, in the search for CAZymes to extract information from and infer structural information about _tm_gh3.

The local CAZyme database was created uing [`cazy_webscraper`](https://hobnobmancer.github.io/cazy_webscraper/). All proteins were retrieved from CAZy, and protein data (IDs, names, EC numbers and PDBs) were retrieved from UniProt for the following CAZy families: GH1, GH2, GH3, GH11, GH26, GH30, GH43, GH51, GH52, GH54, GH116, and GH120.

## Table of contents

The queries are grouped by their target of exploration, and each query is named to represent the boolean (AND/OR) operations used to retrieve the data of interest.

### List of queries:

&nbsp; _Exploration of EC 3.2.1.37_
1. [EC 3.2.1.37](#1-ec-32137)
2. [EC 3.2.1.37 AND Bacteria](#2-ec-32137-and-bacteria)
3. [EC 3.2.1.37 AND PDB accessions](#3-ec-32137-and-pdbs)

	_Exploration of family GH3_
4. [GH3](#4-gh3)
5. [GH3 AND Bacteria](#5-gh3-and-bacteria)
6. [GH3 AND EC 3.2.1.37](#6-gh3-and-ec-32137)
7. [GH3 AND EC 3.2.1.37 AND Bacteria](#7-gh3-and-ec-32137-and-bacteria)
8. [GH3 AND EC 3.2.1.37 AND PDBs](#8-gh3-and-ec-32137-and-pdb)
9. [GH3 AND EC 3.2.1.37 AND PDBs AND Bacteria](#9-gh3-and-ec-32137-and-bacteria)
10. [GH3 AND PDBs](#10-gh3-and-pdbs)
11. [GH3 AND PDBs AND Bacteria](#11-gh3-and-pdbs-and-bacteria)

	_Exploring Thermotoga_
12. [_Thermotoga_](#12-thermotoga)
13. [CAZy families of _Thermotoga_](#13-cazy-families-of-thermotoga)
14. [_Thermotoga_ AND PDBs](#14-thermotoga-and-pdbs)
15. [_Thermotoga_ AND EC 3.2.1.37](#15-thermotoga-and-ec-32137)
16. [CAZy families of _Thermotoga_ AND EC 3.2.1.37](#16-cazy-families-of-thermotoga-and-ec-32137)
17. [_Thermotoga_ AND EC 3.2.1.37 AND PDBs](#17-thermotoga-and-ec-32137-and-pdbs)

	_Exploration of Thermotoga and closely related Pseudothermotoga_
18. [_Thermotoga_ OR _Pseudothermotoga_](#18-thermotoga-or-pseudothermotoga)
19. [CAZy families of _Thermotoga_ AND _Pseudothermotoga_](#19-cazy-families-of-thermotoga-or-pseudothermotoga)
20. [_Thermotoga_ AND _Pseudothermotoga_ AND PDBs](#20-thermotoga-or-pseudothermotoga-and-pdbs)
21. [_Thermotoga_ AND _Pseudothermotoga_ AND EC 3.2.1.37](#21-thermotoga-or-pseudothermotoga-and-ec-32137)
22. [CAZy families of _Thermotoga_ AND _Pseudothermotoga_ AND EC 3.2.1.37](#22-cazy-families-of-thermotoga-or-pseudothermotoga-and-ec-32137)
23. [_Thermotoga_ AND _Pseudothermotoga_ AND EC 3.2.1.37 AND PDBs](#23-thermotoga-or-pseudothermotoga-and-ec-32137-and-pdbs)


# Exploration of EC 3.2.1.37

## 1. EC 3.2.1.37

The number of proteins in CAZy with the EC number 3.2.1.37 was retrieved using the following command.

```sql
SELECT COUNT(Genbanks.genbank_accession)
FROM Genbanks
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
WHERE Ecs.ec_number = '3.2.1.37'
```

669 proteins were annotated with the EC number 3.2.1.37

## 2. Families of EC 3.2.1.37

The CAZy families that contain CAZymes annotated with the EC number 3.2.1.37, and the number of CAZymes in each family with the EC number 3.2.1.37 were retrieved using the following command:

```sql
SELECT DISTINCT CazyFamilies.family, COUNT(Genbanks.genbank_accession) AS num_of_proteins
FROM CazyFamilies
INNER JOIN Genbanks_CazyFamilies ON CazyFamilies.family_id = Genbanks_CazyFamilies.family_id
INNER JOIN Genbanks ON Genbanks_CazyFamilies.genbank_id = Genbanks.genbank_id
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
WHERE Ecs.ec_number = '3.2.1.37'
GROUP BY CazyFamilies.family
```

This command returned the following families:

| CAZy family | Number of proteins |
|-------------|--------------------|
| GH3         |                173 |
| GH5         |                  1 |
| GH43        |                462 |
| GH51        |                  2 |
| GH52        |                 27 |
| GH54        |                  7 |
| GH120       |                  2 |
| CBM2        |                  1 |
| CBM5        |                  1 |
| CBM6        |                 16 |
| CBM13       |                  3 |
| CBM22       |                  1 |
| CBM42       |                  2 |

A `csv` file of the results is available in [the repository]().

## 3. EC 3.2.1.37 AND Bacteria

554 proteins were identified as being sourced from bacteria *and* annotated with the EC number 3.2.1.37.

```sql
WITH King_Query (king_gbk) AS (
	SELECT Genbanks.genbank_accession
	FROM Genbanks
	INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
	INNER JOIN Kingdoms ON Taxs.kingdom_id = Kingdoms.kingdom_id
	WHERE Kingdoms.kingdom = 'Bacteria'
)
SELECT COUNT(Genbanks.genbank_accession)
FROM Genbanks
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
LEFT JOIN King_Query ON Genbanks.genbank_accession = King_Query.king_gbk
WHERE Ecs.ec_number = '3.2.1.37' AND
	Genbanks.genbank_accession IN King_Query
```

## 4. EC 3.2.1.37 AND PDBs

The PDB accessions retrieved from UniProt, CAZy family annotations and source organism for all CAZymes annotated with the EC number 3.2.1.37 were retrieved using the following command.

```sql
WITH King_Query (king_gbk, king, king_genus, king_species) AS (
	SELECT Genbanks.genbank_accession, Kingdoms.kingdom, Taxs.genus, Taxs.species
	FROM Genbanks
	INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
	INNER JOIN Kingdoms ON Taxs.kingdom_id = Kingdoms.kingdom_id
)
SELECT DISTINCT Genbanks.genbank_accession, King_Query.king AS kingdom, King_Query.king_genus AS genus, King_Query.king_species AS species, Pdbs.pdb_accession, CazyFamilies.family
FROM Genbanks
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
INNER JOIN Genbanks_Pdbs ON Genbanks.genbank_id = Genbanks_Pdbs.genbank_id
INNER JOIN Pdbs ON Genbanks_Pdbs.pdb_id = Pdbs.pdb_id
LEFT JOIN King_Query ON Genbanks.genbank_accession = King_Query.king_gbk
WHERE Ecs.ec_number = '3.2.1.37'
ORDER BY Genbanks.genbank_accession
```

The results are listed here and a [`csv` file]() is available in the repository.

| GenBank Accession | Kingdom      | Genus              | Species                           | PDB Accession | CAZy Family |
|-------------------|--------------|--------------------|-----------------------------------|---------------|-------------|
| ABC75004.1        | Bacteria     | Geobacillus        | thermoleovorans IT-08             | 5Z5D          | GH43        |
| ABC75004.1        | Bacteria     | Geobacillus        | thermoleovorans IT-08             | 5Z5I          | GH43        |
| ABC75004.1        | Bacteria     | Geobacillus        | thermoleovorans IT-08             | 5Z5H          | GH43        |
| ABC75004.1        | Bacteria     | Geobacillus        | thermoleovorans IT-08             | 5Z5F          | GH43        |
| ADL35052.1        | Bacteria     | Butyrivibrio       | proteoclasticus B316              | 4NOV          | GH43        |
| AFP23142.1        | unclassified | uncultured         | organism                          | 4MLG          | GH43        |
| BAB07402.1        | Bacteria     | Alkalihalobacillus | halodurans C-125                  | 1YRZ          | GH43        |
| CAA29235.1        | Bacteria     | Bacillus           | pumilus IPO                       | 5ZQX          | GH43        |
| CAA29235.1        | Bacteria     | Bacillus           | pumilus IPO                       | 5ZQJ          | GH43        |
| CAA29235.1        | Bacteria     | Bacillus           | pumilus IPO                       | 5ZQS          | GH43        |
| CAA73902.1        | Eukaryota    | Aspergillus        | nidulans                          | 6Q7J          | GH3         |
| CAA73902.1        | Eukaryota    | Aspergillus        | nidulans                          | 6Q7I          | GH3         |
| CAA93248.1        | Eukaryota    | Trichoderma        | reesei                            | 5AE6          | GH3         |
| CAA93248.1        | Eukaryota    | Trichoderma        | reesei                            | 5A7M          | GH3         |
| CAB13642.2        | Bacteria     | Bacillus           | subtilis subsp. subtilis str. 168 | 1YIF          | GH43        |

11 PDB accessions were retrieved from family GH43, from 6 proteins, and 4 PDB accessions were retrieved from CAZy family GH3, from 2 proteins.

The source organisms of the proteins with PDB accession in GH3, annotated with the EC number 3.2.1.37, can also be retrieved using the following command:

```sql
SELECT DISTINCT Genbanks.genbank_accession, Taxs.genus, Taxs.species
FROM Genbanks
INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
INNER JOIN Kingdoms ON Taxs.kingdom_id = Kingdoms.kingdom_id
WHERE Genbanks.genbank_accession = 'CAA73902.1' OR
	Genbanks.genbank_accession = 'CAA93248.1'
```

| Genbank Accession |          Genus       |      Species    |
|:-----------------:|:--------------------:|:---------------:|
|     CAA73902.1    |      Aspergillus     |     nidulans    |
|     CAA93248.1    |      Trichoderma     |     reesei      |


# Exploration of CAZy family GH3

## 5. GH3

The number of CAZymes in GH3 (42,968 proteins) was retrieved using the following command:

```sql
SELECT COUNT(Genbanks.genbank_accession)
FROM Genbanks
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
WHERE CazyFamilies.family = 'GH3'
```

## 6. GH3 AND Bacteria

The number of bacterial proteins in CAZy family GH3 (40,090 proteins) was retrieved using the following comamnd:

```sql
WITH King_Query (king_gbk) AS (
	SELECT Genbanks.genbank_accession
	FROM Genbanks
	INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
	INNER JOIN Kingdoms ON Taxs.kingdom_id = Kingdoms.kingdom_id
	WHERE Kingdoms.kingdom = 'Bacteria'
)
SELECT COUNT(Genbanks.genbank_accession)
FROM Genbanks
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
LEFT JOIN King_Query ON Genbanks.genbank_accession = King_Query.king_gbk
WHERE CazyFamilies.family = 'GH3' AND
	Genbanks.genbank_accession IN King_Query
```

## 7. GH3 AND EC 3.2.1.37

The number of CAZymes in CAZy family GH3 *and* annotated with the EC number 3.2.1.37 (173 proteins) was retrieved using the following command:

```sql
SELECT COUNT(Genbanks.genbank_accession)
FROM Genbanks
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
WHERE CazyFamilies.family = 'GH3' AND Ecs.ec_number = '3.2.1.37'
```

## 8. GH3 AND EC 3.2.1.37 AND Bacteria

The number of proteins in CAZy family GH3, annotated with the EC number 3.2.1.37 *and* are sourced from bacteria was retrieved using the following command:

```sql
WITH King_Query (king_gbk) AS (
	SELECT Genbanks.genbank_accession
	FROM Genbanks
	INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
	INNER JOIN Kingdoms ON Taxs.kingdom_id = Kingdoms.kingdom_id
	WHERE Kingdoms.kingdom = 'Bacteria'
)
SELECT COUNT(Genbanks.genbank_accession)
FROM Genbanks
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
LEFT JOIN King_Query ON Genbanks.genbank_accession = King_Query.king_gbk
WHERE CazyFamilies.family = 'GH3' AND 
	Ecs.ec_number = '3.2.1.37' AND
	Genbanks.genbank_accession IN King_Query
```

This identified 77 proteins.

## 9. GH3 AND EC 3.2.1.37 AND PDB

The PDB accessions retrieved from UniProt for proteins in GH3 annotated with the EC number 3.2.1.37, including the source organism, were retrieved using the following command:

```sql
SELECT DISTINCT Genbanks.genbank_accession, Pdbs.pdb_accession, Taxs.genus, Taxs.species
FROM Genbanks
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
INNER JOIN Genbanks_Pdbs ON Genbanks.genbank_id = Genbanks_Pdbs.genbank_id
INNER JOIN Pdbs ON Genbanks_Pdbs.pdb_id = Pdbs.pdb_id
INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
WHERE CazyFamilies.family = 'GH3' AND
	Ecs.ec_number = '3.2.1.37'
```

The returned PDB accessions were:

| GenBank Accession | PDB Accession | Genus       | Species  |
|-------------------|---------------|-------------|----------|
| CAA73902.1        | 6Q7J          | Trichoderma | reesei   |
| CAA73902.1        | 6Q7I          | Trichoderma | reesei   |
| CAA93248.1        | 5AE6          | Aspergillus | nidulans |
| CAA93248.1        | 5A7M          | Aspergillus | nidulans |

## 10. GH3 AND EC 3.2.1.37 AND Bacteria and PDBs

The PDB accessions retrieved from UniProt for CAZymes in GH3, annotated with the EC number 3.2.1.37 and retrieved from Bacteria were retrieved using the following command:

```sql
WITH King_Query (king_gbk) AS (
	SELECT Genbanks.genbank_accession
	FROM Genbanks
	INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
	INNER JOIN Kingdoms ON Taxs.kingdom_id = Kingdoms.kingdom_id
	WHERE Kingdoms.kingdom = 'Bacteria'
)
SELECT DISTINCT Genbanks.genbank_accession, Pdbs.pdb_accession
FROM Genbanks
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
INNER JOIN Genbanks_Pdbs ON Genbanks.genbank_id = Genbanks_Pdbs.genbank_id
INNER JOIN Pdbs ON Genbanks_Pdbs.pdb_id = Pdbs.pdb_id
LEFT JOIN King_Query ON Genbanks.genbank_accession = King_Query.king_gbk
WHERE CazyFamilies.family = 'GH3' AND 
	Ecs.ec_number = '3.2.1.37' AND
	Genbanks.genbank_accession IN King_Query
```

However, no PDB accessions matched the provided criteria.

## 11. GH3 AND PDBs

To expand the search beyond EC annotated proteins, because the majoirty of proteins are not annotated with an EC number in GH3, a list of all PDB accessions associated with proteins in CAZy family GH3 (including the source organism) was retrieved using the following command:

```sql
SELECT DISTINCT Genbanks.genbank_accession, Pdbs.pdb_accession, Taxs.genus, Taxs.species
FROM Genbanks
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
INNER JOIN Genbanks_Pdbs ON Genbanks.genbank_id = Genbanks_Pdbs.genbank_id
INNER JOIN Pdbs ON Genbanks_Pdbs.pdb_id = Pdbs.pdb_id
INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
WHERE CazyFamilies.family = 'GH3'
```

63 PDB accessions were returned from 20 proteins, and these are listed in the [repository]().

For each protein matching the provided criteria, the command returuned:
- GenBank accession
- PDB accession
- Genus of the source organism
- Species of the source organism
- Protein name listed in UniProt

## 12. GH3 AND Bacteria AND PDBs 

A list of all PDB accessions associated with bacterial proteins in CAZy family GH3 was retrieved using the following command:

```sql
WITH King_Query (king_gbk) AS (
	SELECT Genbanks.genbank_accession
	FROM Genbanks
	INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
	INNER JOIN Kingdoms ON Taxs.kingdom_id = Kingdoms.kingdom_id
	WHERE Kingdoms.kingdom = 'Bacteria'
)
SELECT DISTINCT Genbanks.genbank_accession, Pdbs.pdb_accession, Taxs.genus, Taxs.species, Uniprots.uniprot_name
FROM Genbanks
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
INNER JOIN Genbanks_Pdbs ON Genbanks.genbank_id = Genbanks_Pdbs.genbank_id
INNER JOIN Pdbs ON Genbanks_Pdbs.pdb_id = Pdbs.pdb_id
INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
INNER JOIN Uniprots ON Genbanks.genbank_id = Uniprots.genbank_id
LEFT JOIN King_Query ON Genbanks.genbank_accession = King_Query.king_gbk
WHERE CazyFamilies.family = 'GH3' AND
	Genbanks.genbank_accession IN King_Query
```

For each protein matching the provided criteria, the command returuned:
- GenBank accession
- PDB accession
- Genus of the source organism
- Species of the source organism
- Protein name listed in UniProt

42 PDB accessions were returned, and these are listed in the [repository]().


# Exploration of Thermotoga

## 13. _Thermotoga_

The total number of CAZymes from _Thermotoga_ species in CAZy was retrievied using the command:

```sql
SELECT COUNT(DISTINCT genbank_accession)
FROM Genbanks
INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
WHERE Taxs.genus = 'Thermotoga'
```

This identied 1211 proteins

## 14. CAZy families of _Thermotoga_

The CAZy families containing proteins from _Thermotoga_ and the number of _Thermotoga_ proteins per CAZy family were retrieved using the following command:

```sql
WITH Tax_Query (tax_gbk) AS (
	SELECT genbank_accession
	FROM Genbanks
	INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
	WHERE Taxs.genus = 'Thermotoga'
)
SELECT DISTINCT CazyFamilies.family, COUNT(Genbanks.genbank_accession) AS num_of_cazymes
FROM CazyFamilies
INNER JOIN Genbanks_CazyFamilies ON CazyFamilies.family_id = Genbanks_CazyFamilies.family_id
INNER JOIN Genbanks ON Genbanks_CazyFamilies.genbank_id = Genbanks.genbank_id
LEFT JOIN Tax_Query ON Genbanks.genbank_accession = Tax_Query.tax_gbk
WHERE Genbanks.genbank_accession IN Tax_Query
GROUP BY CazyFamilies.family
```

68 CAZy families were returned.  

A `csv` file of the output is available in the [repository]().

## 15. _Thermotoga_ AND PDBs

The PDB accessions retrieved from UniProt for CAZymes from _Thermotoga_ species , including the CAZy family annotation, were retrieved using the following command:

```sql
WITH Thermo_Query (thermo_gbk) AS (
	SELECT DISTINCT genbank_accession
	FROM Genbanks
	INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
	WHERE Taxs.genus = 'Thermotoga'
)
SELECT DISTINCT Genbanks.genbank_accession, Pdbs.pdb_accession, CazyFamilies.family, Uniprots.uniprot_name
FROM Genbanks
INNER JOIN Genbanks_Pdbs ON Genbanks.genbank_id = Genbanks_Pdbs.genbank_id
INNER JOIN Pdbs ON Genbanks_Pdbs.pdb_id = Pdbs.pdb_id
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
INNER JOIN Uniprots ON Genbanks.genbank_id = Uniprots.genbank_id
LEFT JOIN Thermo_Query ON Genbanks.genbank_accession = Thermo_Query.thermo_gbk
WHERE genbank_accession IN Thermo_Query
```

This returned 46 PDB accessions from 9 proteins.

These 9 proteins were:
| GenBank Accession | CAZy family |
|-------------------|-------------|
| AAB95492.2        | GH1         |
| AAD35369.1        | GH51        |
| AAD35891.1        | GH3         |
| AAK16587.1        | GH3         |
| ABI29899.1        | GH3         |
| ABQ46651.1        | GH51        |
| ABQ46657.1        | GH43        |
| CAA04513.1        | GH2         |
| CAA52276.1        | GH1         |

The results were stored in a `csv` file, which is available in the [repository]().

## 16. _Thermotoga_ AND EC 3.2.1.37

The number of CAZymes from _Thermotoga_ species annotated with the EC number 3.2.1.37 (1 protein) was retrieved using the command:

```sql
WITH Thermo_Query (thermo_gbk) AS (
	SELECT DISTINCT genbank_accession
	FROM Genbanks
	INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
	WHERE Taxs.genus = 'Thermotoga'
)
SELECT COUNT(DISTINCT genbank_accession)
FROM Genbanks
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
LEFT JOIN Thermo_Query ON Genbanks.genbank_accession = Thermo_Query.thermo_gbk
WHERE Ecs.ec_number = '3.2.1.37' AND
	genbank_accession IN Thermo_Query
```

The GenBank accession of CAZymes from _Thermotoga_ were retrievied using the command:

```sql
WITH Thermo_Query (thermo_gbk) AS (
	SELECT DISTINCT genbank_accession
	FROM Genbanks
	INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
	WHERE Taxs.genus = 'Thermotoga'
)
SELECT DISTINCT genbank_accession
FROM Genbanks
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
LEFT JOIN Thermo_Query ON Genbanks.genbank_accession = Thermo_Query.thermo_gbk
WHERE Ecs.ec_number = '3.2.1.37' AND
	genbank_accession IN Thermo_Query
```

This returned the GenBank accession of **AGL48999.1**.

**The protein AGL48999.1 was the protein of interest _tm_gh3.**

## 17. CAZy families of _Thermotoga_ AND EC 3.2.1.37

The CAZy families of proteins from _Thermotoga_ species annotated with the EC number 3.2.1.37, including the number of _Thermotoga_ proteins annotated with the EC number 3.2.1.37 per CAZy family, was retrieved using the following command:

```sql
WITH Tax_Query (tax_gbk) AS (
	SELECT genbank_accession
	FROM Genbanks
	INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
	WHERE Taxs.genus = 'Thermotoga'
)
SELECT DISTINCT CazyFamilies.family, COUNT(Genbanks.genbank_accession)
FROM CazyFamilies
INNER JOIN Genbanks_CazyFamilies ON CazyFamilies.family_id = Genbanks_CazyFamilies.family_id
INNER JOIN Genbanks ON Genbanks_CazyFamilies.genbank_id = Genbanks.genbank_id
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
LEFT JOIN Tax_Query ON Genbanks.genbank_accession = Tax_Query.tax_gbk
WHERE Ecs.ec_number = '3.2.1.37' AND 
	Genbanks.genbank_accession IN Tax_Query
GROUP BY CazyFamilies.family
```

This returned one CAZy family, GH3.

## 18. _Thermotoga_ AND EC 3.2.1.37 AND PDBs

```sql
WITH Tax_Query (tax_gbk) AS (
	SELECT genbank_accession
	FROM Genbanks
	INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
	WHERE Taxs.genus = 'Thermotoga'
)
SELECT DISTINCT pdb_accession
FROM Pdbs
INNER JOIN Genbanks_Pdbs ON Pdbs.pdb_id = Genbanks_Pdbs.pdb_id
INNER JOIN Genbanks ON Genbanks_Pdbs.genbank_id = Genbanks.genbank_id
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
LEFT JOIN Tax_Query ON Genbanks.genbank_accession = Tax_Query.tax_gbk
WHERE Ecs.ec_number = '3.2.1.37' AND 
	Genbanks.genbank_accession IN Tax_Query
```

No PDB accessions were returned.

# Exploration of _Thermotoga_ and _Pseudothermotoga_

To expand the pool of potentially functionally and structurally relevant proteins, the search was expanded to include the _Pseudothermotoga_ genus, which is close to _Thermotoga_ in the evolutionary tree.

## 19. _Thermotoga_ OR _Pseudothermotoga_

The total number of CAZymes from _Thermotoga_ and _Pseudothermotoga_ species was retrieved using the following command:

```sql
SELECT COUNT(DISTINCT genbank_accession)
FROM Genbanks
INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
WHERE Taxs.genus = 'Thermotoga' OR Taxs.genus = 'Pseudothermotoga'
```

This identified 1379 proteins

## 20. CAZy families of _Thermotoga_ OR _Pseudothermotoga_

The CAZy families of proteins from _Thermotoga_ and _Pseudothermotoga_ species, as well as the number of proteins from these species in the CAZy families was retrieived using:

```sql
WITH Tax_Query (tax_gbk) AS (
	SELECT genbank_accession
	FROM Genbanks
	INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
	WHERE Taxs.genus = 'Thermotoga' OR Taxs.genus = 'Pseudothermotoga'
)
SELECT DISTINCT CazyFamilies.family, COUNT(Genbanks.genbank_accession) AS num_of_cazymes
FROM CazyFamilies
INNER JOIN Genbanks_CazyFamilies ON CazyFamilies.family_id = Genbanks_CazyFamilies.family_id
INNER JOIN Genbanks ON Genbanks_CazyFamilies.genbank_id = Genbanks.genbank_id
LEFT JOIN Tax_Query ON Genbanks.genbank_accession = Tax_Query.tax_gbk
WHERE Genbanks.genbank_accession IN Tax_Query
GROUP BY CazyFamilies.family
```

68 CAZy families were returned, and the output is stored in a `csv` file in the [repository]().

## 21. _Thermotoga_ OR _Pseudothermotoga_ AND PDBs

The PDB accessions for all proteins from _Thermotoga_ and _Pseudothermotoga_ species

```sql
WITH Thermo_Query (thermo_gbk) AS (
	SELECT DISTINCT genbank_accession
	FROM Genbanks
	INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
	WHERE Taxs.genus = 'Thermotoga' OR Taxs.genus = 'Pseudothermotoga'
)
SELECT DISTINCT Genbanks.genbank_accession, Pdbs.pdb_accession, CazyFamilies.family, Taxs.genus, Uniprots.uniprot_name
FROM Genbanks
INNER JOIN Genbanks_Pdbs ON Genbanks.genbank_id = Genbanks_Pdbs.genbank_id
INNER JOIN Pdbs ON Genbanks_Pdbs.pdb_id = Pdbs.pdb_id
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
INNER JOIN Uniprots ON Genbanks.genbank_id = Uniprots.genbank_id
LEFT JOIN Thermo_Query ON Genbanks.genbank_accession = Thermo_Query.thermo_gbk
WHERE genbank_accession IN Thermo_Query
ORDER BY Taxs.genus
```

No additional PDB accessions were retrieved when compared against query #15. All PDB accessions were retrievied from _Thermotoga_ species.

The output was stored in a `csv` file and stored in the [repository]().

## 22. _Thermotoga_ OR _Pseudothermotoga_ AND EC 3.2.1.37

The number of CAZymes from _Thermotoga_ and _Pseudothermotoga_ species annotated with the EC number 3.2.1.37 (XXX proteins) was retrieved using the command:

```sql
WITH Thermo_Query (thermo_gbk) AS (
	SELECT DISTINCT genbank_accession
	FROM Genbanks
	INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
	WHERE Taxs.genus = 'Thermotoga' OR Taxs.genus = 'Pseudothermotoga'
)
SELECT COUNT(DISTINCT genbank_accession)
FROM Genbanks
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
LEFT JOIN Thermo_Query ON Genbanks.genbank_accession = Thermo_Query.thermo_gbk
WHERE Ecs.ec_number = '3.2.1.37' AND
	genbank_accession IN Thermo_Query
```

## 23. CAZy families of _Thermotoga_ OR _Pseudothermotoga_ AND EC 3.2.1.37

The CAZy families of proteins from _Thermotoga_  and _Pseudothermotoga_ species annotated with the EC number 3.2.1.37, including the number of _Thermotoga_ and _Pseudothermotoga_ proteins annotated with the EC number 3.2.1.37 per CAZy family, was retrieved using the following command:

```sql
WITH Tax_Query (tax_gbk) AS (
	SELECT genbank_accession
	FROM Genbanks
	INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
	WHERE Taxs.genus = 'Thermotoga' OR Taxs.genus = 'Pseudothermotoga'
)
SELECT DISTINCT CazyFamilies.family, COUNT(Genbanks.genbank_accession) AS num_of_proteins
FROM CazyFamilies
INNER JOIN Genbanks_CazyFamilies ON CazyFamilies.family_id = Genbanks_CazyFamilies.family_id
INNER JOIN Genbanks ON Genbanks_CazyFamilies.genbank_id = Genbanks.genbank_id
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
LEFT JOIN Tax_Query ON Genbanks.genbank_accession = Tax_Query.tax_gbk
WHERE Ecs.ec_number = '3.2.1.37' AND 
	Genbanks.genbank_accession IN Tax_Query
GROUP BY CazyFamilies.family
```

As with query #16, this only returned the protein of interest _tm_gh3.
