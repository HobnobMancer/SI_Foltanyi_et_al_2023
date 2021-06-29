# SQL queries

This docs logs the queries made in SQL to a local CAZyme database, in the search for suitable model CAZymes.

## Query 1, search only with the EC number EC 3.2.1.37

```sql
SELECT DISTINCT genbanks.genbank_accession, families.family, ecs.ec_number, taxs.genus, taxs.species
FROM genbanks
INNER JOIN cazymes_genbanks ON genbanks.genbank_id = cazymes_genbanks.genbank_id
INNER JOIN cazymes ON cazymes_genbanks.cazyme_id = cazymes.cazyme_id

INNER JOIN cazymes_families ON cazymes.cazyme_id = cazymes_families.cazyme_id
INNER JOIN families ON cazymes_families.family_id = families.family_id

INNER JOIN taxs ON cazymes.taxonomy_id = taxs.taxonomy_id

INNER JOIN cazymes_ecs ON cazymes.cazyme_id = cazymes_ecs.cazyme_id
INNER JOIN ecs ON cazymes_ecs.ec_id = ecs.ec_id

WHERE (ecs.ec_number = '3.2.1.37')
```

This returned 343 rows, but included proteins from Eukaryotes.
Need to add 'bacteria' filter

## Query 2, search for CAZymes from bacteria with the EC number EC3.2.1.37

```sql
SELECT DISTINCT genbanks.genbank_accession, families.family, ecs.ec_number, taxs.genus, taxs.species
FROM genbanks
INNER JOIN cazymes_genbanks ON genbanks.genbank_id = cazymes_genbanks.genbank_id
INNER JOIN cazymes ON cazymes_genbanks.cazyme_id = cazymes.cazyme_id

INNER JOIN cazymes_families ON cazymes.cazyme_id = cazymes_families.cazyme_id
INNER JOIN families ON cazymes_families.family_id = families.family_id

INNER JOIN taxs ON cazymes.taxonomy_id = taxs.taxonomy_id

INNER JOIN kingdoms ON taxs.kingdom_id = kingdoms.kingdom_id

INNER JOIN cazymes_ecs ON cazymes.cazyme_id = cazymes_ecs.cazyme_id
INNER JOIN ecs ON cazymes_ecs.ec_id = ecs.ec_id

WHERE (ecs.ec_number = '3.2.1.37') AND (kingdoms.kingdom = 'Bacteria')
```

This returned 194 CAZymes. Many of which had no GenBank accession, likely becuase they are sourced from patents.

The activity of EC3.2.1.37 is xylosidase, which is a GH activity. Some of the families retrieved are not GH families and 
thees are potentially additional modules predicted to be present in the CAZymes of interest.

## Query 3, search for CAZymes from bacteria with the EC number EC3.2.1.37 and return the PDB

The aim of this work is to find appropriate structural models for comparison and molecular replacement, therefore, 
query 2 was repeated with the addition of filtering out proteins without a PDB record. Additionally, multiple GenBank 
accessions may be returned for each CAZyme because some CAZymes have multiple GenBank accessions. Therefore, the results 
were further filtered to retrieve only the primary GenBank accession for each CAZyme.

```sql
SELECT DISTINCT genbanks.genbank_accession, cazymes.cazyme_id, families.family, ecs.ec_number, taxs.genus, taxs.species
FROM genbanks
INNER JOIN cazymes_genbanks ON genbanks.genbank_id = cazymes_genbanks.genbank_id
INNER JOIN cazymes ON cazymes_genbanks.cazyme_id = cazymes.cazyme_id

INNER JOIN cazymes_families ON cazymes.cazyme_id = cazymes_families.cazyme_id
INNER JOIN families ON cazymes_families.family_id = families.family_id

INNER JOIN taxs ON cazymes.taxonomy_id = taxs.taxonomy_id

INNER JOIN kingdoms ON taxs.kingdom_id = kingdoms.kingdom_id

INNER JOIN cazymes_ecs ON cazymes.cazyme_id = cazymes_ecs.cazyme_id
INNER JOIN ecs ON cazymes_ecs.ec_id = ecs.ec_id

INNER JOIN cazymes_pdbs ON cazymes.cazyme_id = cazymes_pdbs.cazyme_id
INNER JOIN pdbs ON cazymes_pdbs.pdb_id = pdbs.pdb_id

WHERE (ecs.ec_number = '3.2.1.37') AND (kingdoms.kingdom = 'Bacteria') AND (pdbs.pdb_accession is not null) AND (cazymes_genbanks.'primary' = 1)
```

The results of thi query are stored in this directory, in the file `query_3_species.csv`.

## Query 4, retrieve PDB accessions

This query repeats query 3 but includes the PDB accessions.

Many of the proteins that met the criteria have no GenBank accession, therefore, the primary PDB accession was also retrieved. Only the primary UniProt accession was retrieved. An additionally, CAZy class 
filter was applied. Xylosidase is a GH class function, therefore, only CAZymes from families in GH were retrieved, in an attempt in retrieving proteins with some 
functional similarity.

```sql
SELECT DISTINCT genbanks.genbank_accession, cazymes.cazyme_id, families.family, ecs.ec_number, taxs.genus, taxs.species, pdbs.pdb_accession
FROM genbanks
INNER JOIN cazymes_genbanks ON genbanks.genbank_id = cazymes_genbanks.genbank_id
INNER JOIN cazymes ON cazymes_genbanks.cazyme_id = cazymes.cazyme_id

INNER JOIN cazymes_families ON cazymes.cazyme_id = cazymes_families.cazyme_id
INNER JOIN families ON cazymes_families.family_id = families.family_id

INNER JOIN taxs ON cazymes.taxonomy_id = taxs.taxonomy_id

INNER JOIN kingdoms ON taxs.kingdom_id = kingdoms.kingdom_id

INNER JOIN cazymes_ecs ON cazymes.cazyme_id = cazymes_ecs.cazyme_id
INNER JOIN ecs ON cazymes_ecs.ec_id = ecs.ec_id

INNER JOIN cazymes_pdbs ON cazymes.cazyme_id = cazymes_pdbs.cazyme_id
INNER JOIN pdbs ON cazymes_pdbs.pdb_id = pdbs.pdb_id

INNER JOIN cazymes_uniprots ON cazymes_uniprots.cazyme_id = cazymes.cazyme_id
INNER JOIN uniprots ON uniprots.uniprot_id = cazymes_uniprots.uniprot_id

WHERE (ecs.ec_number = '3.2.1.37') AND 
(kingdoms.kingdom = 'Bacteria') AND 
(pdbs.pdb_accession is not null) AND 
(cazymes_genbanks.'primary' = 1) AND 
(uniprots.'primary' = 1) AND 
(families.family like 'GH%')
```

The results of this query are stored in this directory, in the file `query_4_ec_pdb_accessions.csv`.

## Query 5, apply genus filter

The main focus on the study is xylosidases from the bacterial phylum Thermotogae. Therefore, query 4 was repeated, filtering for only CAZymes from this phylum.

```sql
SELECT DISTINCT genbanks.genbank_accession, cazymes.cazyme_id, families.family, ecs.ec_number, taxs.genus, taxs.species, pdbs.pdb_accession
FROM genbanks
INNER JOIN cazymes_genbanks ON genbanks.genbank_id = cazymes_genbanks.genbank_id
INNER JOIN cazymes ON cazymes_genbanks.cazyme_id = cazymes.cazyme_id

INNER JOIN cazymes_families ON cazymes.cazyme_id = cazymes_families.cazyme_id
INNER JOIN families ON cazymes_families.family_id = families.family_id

INNER JOIN taxs ON cazymes.taxonomy_id = taxs.taxonomy_id

INNER JOIN kingdoms ON taxs.kingdom_id = kingdoms.kingdom_id

INNER JOIN cazymes_ecs ON cazymes.cazyme_id = cazymes_ecs.cazyme_id
INNER JOIN ecs ON cazymes_ecs.ec_id = ecs.ec_id

INNER JOIN cazymes_pdbs ON cazymes.cazyme_id = cazymes_pdbs.cazyme_id
INNER JOIN pdbs ON cazymes_pdbs.pdb_id = pdbs.pdb_id

WHERE (ecs.ec_number = '3.2.1.37') AND (pdbs.pdb_accession is not null) AND (cazymes_genbanks.'primary' = 1) AND
(taxs.genus = 'Kosmotoga') AND (taxs.genus = 'Mesotoga') AND (taxs.genus = 'Athalassotoga') AND (taxs.genus = 'Mesoaciditoga') AND
(taxs.genus = 'Defluviitoga') AND (taxs.genus = 'Geotoga') AND (taxs.genus = 'Marinitoga') AND (taxs.genus = 'Oceanotoga') AND
(taxs.genus = 'Petrotoga') AND (taxs.genus = 'Tepiditoga') AND (taxs.genus = 'Fervidobacterium') AND (taxs.genus = 'Thermosipho') AND
(taxs.genus = 'Pseudothermotoga') AND (taxs.genus = 'Thermopallium') AND (taxs.genus = 'Thermotoga') AND (taxs.genus = 'Thermotogales')
```

No results were returned.

## Query 6, remove EC number filter

One issue with relying on EC number annotation is that computationally predicted 4 digit EC numbers are not often very accuracte, 
and the minority of CAZymes are annotated with an EC number. Therefore, query 5 was repeated, without the EC number filter. An additionally, CAZy class 
filter was applied. Xylosidase is a GH class function, therefore, only CAZymes from families in GH were retrieved, in an attempt in retrieving proteins with some 
functional similarity.

```sql
SELECT DISTINCT genbanks.genbank_accession, cazymes.cazyme_id, families.family, taxs.genus, taxs.species, pdbs.pdb_accession
FROM genbanks
INNER JOIN cazymes_genbanks ON genbanks.genbank_id = cazymes_genbanks.genbank_id
INNER JOIN cazymes ON cazymes_genbanks.cazyme_id = cazymes.cazyme_id

INNER JOIN cazymes_families ON cazymes.cazyme_id = cazymes_families.cazyme_id
INNER JOIN families ON cazymes_families.family_id = families.family_id

INNER JOIN taxs ON cazymes.taxonomy_id = taxs.taxonomy_id

INNER JOIN kingdoms ON taxs.kingdom_id = kingdoms.kingdom_id

INNER JOIN cazymes_ecs ON cazymes.cazyme_id = cazymes_ecs.cazyme_id
INNER JOIN ecs ON cazymes_ecs.ec_id = ecs.ec_id

INNER JOIN cazymes_pdbs ON cazymes.cazyme_id = cazymes_pdbs.cazyme_id
INNER JOIN pdbs ON cazymes_pdbs.pdb_id = pdbs.pdb_id

WHERE (pdbs.pdb_accession is not null) AND (cazymes_genbanks.'primary' = 1) AND (
(taxs.genus = 'Kosmotoga') OR (taxs.genus = 'Mesotoga') OR (taxs.genus = 'Athalassotoga') OR (taxs.genus = 'Mesoaciditoga') OR
(taxs.genus = 'Defluviitoga') OR (taxs.genus = 'Geotoga') OR (taxs.genus = 'Marinitoga') OR (taxs.genus = 'Oceanotoga') OR
(taxs.genus = 'Petrotoga') OR (taxs.genus = 'Tepiditoga') OR (taxs.genus = 'Fervidobacterium') OR (taxs.genus = 'Thermosipho') OR
(taxs.genus = 'Pseudothermotoga') OR (taxs.genus = 'Thermopallium') OR (taxs.genus = 'Thermotoga') OR (taxs.genus = 'Thermotogales')) AND 
(families.family like 'GH%')
```

201 results were returned. These results are stored in this directory, in the file `query_6_thermotogae_pdb_accessions.csv`

# Retrieving the PDB accessions

One limitation of how PDB accessions are stored in CAZy is that they include the chain id. Therefore, to determine the exact number of unique 
CAZymes retrieved from queries 4 (EC number filter) and 6 (genus filter), the jupyter notebook `parse_sql_query_output.ipynb` was used to parse the 
dataframes created from queries 4 and 6. The output dataframes from the notebook stored in this directory and are called 
`ec_pdb_accessions.csv` and `gh_thermotogae_pdb_accessions.csv`, respectively.

`ec_pdb_accessions.csv` contains XX unique CAZymes with a total 303 PDB structure file accessions.
`gh_thermotogae_pdb_accessions.csv` contains 31 unique CAZymes with a total 130 PDB structure file accessions.
