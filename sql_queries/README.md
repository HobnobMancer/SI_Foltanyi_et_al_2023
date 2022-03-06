# SQL queries

This doc lists the queries made in SQL to a local CAZyme database, in the search for CAZymes to extract information from and infer structural information about _tm_gh3.

The local CAZyme database was created uing [`cazy_webscraper`](https://hobnobmancer.github.io/cazy_webscraper/). All proteins were retrieved from CAZy, and protein data (IDs, names, EC numbers and PDBs) were retrieved from UniProt for the following CAZy families: GH1, GH2, GH3, GH11, GH26, GH30, GH43, GH51, GH52, GH54, GH116, and GH120.

## Table of contents
1. [EC 3.2.1.37](#1-ec-32137)
2. [EC 3.2.1.37 AND Bacteria](#2-ec-32137-and-bacteria)
3. [EC 3.2.1.37 AND PDB accessions](#3-ec-32137-and-pdbs)

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
SELECT DISTINCT CazyFamilies.family, COUNT(Genbanks.genbank_accession)
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

## 2. EC 3.2.1.37 AND Bacteria

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

## 3. EC 3.2.1.37 AND PDBs

The PDB accessions retrieved from UniProt, CAZy family annotations and source organism for all CAZymes annotated with the EC number 3.2.1.37 were retrieved using the following command.

```sql
WITH King_Query (king_gbk, king, king_genus, king_species) AS (
	SELECT Genbanks.genbank_accession, Kingdoms.kingdom, Taxs.genus, Taxs.species
	FROM Genbanks
	INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
	INNER JOIN Kingdoms ON Taxs.kingdom_id = Kingdoms.kingdom_id
)
SELECT DISTINCT Genbanks.genbank_accession, King_Query.king, King_Query.king_genus, King_Query.king_species, Pdbs.pdb_accession, CazyFamilies.family
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

## 4. GH3

The number of CAZymes in GH3 (42,968 proteins) was retrieved using the following command:

```sql
SELECT COUNT(Genbanks.genbank_accession)
FROM Genbanks
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
WHERE CazyFamilies.family = 'GH3'
```

## 5. GH3 AND Bacteria

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

## 6. GH3 AND EC 3.2.1.37

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

## 7. GH3 AND EC 3.2.1.37 AND Bacteria

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

## 8. GH3 AND EC 3.2.1.37 AND PDB

The PDB accessions retrieved from UniProt for proteins in GH3 annotated with the EC number 3.2.1.37 were retrieved using the following command:

```sql
SELECT DISTINCT Genbanks.genbank_accession, Pdbs.pdb_id, Pdbs.pdb_accession
FROM Genbanks
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
INNER JOIN Genbanks_Pdbs ON Genbanks.genbank_id = Genbanks_Pdbs.genbank_id
INNER JOIN Pdbs ON Genbanks_Pdbs.pdb_id = Pdbs.pdb_id
WHERE CazyFamilies.family = 'GH3' AND
	Ecs.ec_number = '3.2.1.37'
```

The returned PDB accessions were:

| GenBank Accession | PDB Accession |
|-------------------|---------------|
| CAA73902.1        | 6Q7J          |
| CAA73902.1        | 6Q7I          |
| CAA93248.1        | 5AE6          |
| CAA93248.1        | 5A7M          |

## 9. GH3 AND EC 3.2.1.37 AND Bacteria

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

## 10. GH3 AND PDBs

A list of all PDB accessions associated with proteins in CAZy family GH3 was retrieved using the following command:

```sql
SELECT DISTINCT Genbanks.genbank_accession, Pdbs.pdb_accession
FROM Genbanks
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
INNER JOIN Genbanks_Pdbs ON Genbanks.genbank_id = Genbanks_Pdbs.genbank_id
INNER JOIN Pdbs ON Genbanks_Pdbs.pdb_id = Pdbs.pdb_id
WHERE CazyFamilies.family = 'GH3'
```

88 PDB accessions were returned, and these are listed in the [repository]().

## 11. GH3 AND PDBs AND Bacteria

A list of all PDB accessions associated with bacterial proteins in CAZy family GH3 was retrieved using the following command:

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
	Genbanks.genbank_accession IN King_Query
```

55 PDB accessions were returned, and these are listed in the [repository]().
