# SQL queries

This docs logs the queries made in SQL to a local CAZyme database, in the search for suitable model CAZymes.

## 1. Number of bacterial proteins in GH3

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

## 2. Number of proteins annotated with the EC number EC 3.2.1.37

```sql
SELECT COUNT(DISTINCT Genbanks.genbank_accession)
FROM Genbanks
INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
WHERE Ecs.ec_number = '3.2.1.37'
```

This identified CAZy contained **75** bacterial proteins annotated with the EC number 3.2.1.37.

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

The output from this query can be found [here](https://github.com/HobnobMancer/Foltanyi_et_al_2022/blob/master/sql_queries/query_2_ec_3-2-1-37_families.csv).

All these proteins belonged to CAZy family GH3. Some proteins contained an additional CBM6 domain.

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

Similarly, the following command was used to retrieve the PDB accessions of all proteins in GH3.

```sql
SELECT DISTINCT Genbanks.genbank_accession, CazyFamilies.family, Pdbs.pdb_accession
FROM Genbanks
INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
INNER JOIN Pdbs ON Genbanks.genbank_id = Pdbs.genbank_id
WHERE CazyFamilies.family = 'GH3'
```

This returned **26 bacterial proteins** with PDB accessions listed in UniProt.

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
