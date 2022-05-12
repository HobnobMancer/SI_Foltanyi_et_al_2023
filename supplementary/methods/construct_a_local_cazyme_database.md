# Construct a local CAZyme database

`cazy_webscraper` [Hobbs et al., 2021] (DOI:) was used to construct a local CAZyme database, to facilitate the thorough interrogation of the CAZy dataset.

> Hobbs, Emma E. M.; Pritchard, Leighton; Chapman, Sean; Gloster, Tracey M. (2021): cazy_webscraper Microbiology Society Annual Conference 2021 poster. figshare. Poster. https://doi.org/10.6084/m9.figshare.14370860.v7

To reconstruct the database to repeat the analysis, use the following command from the root of this repository:
```bash
cazy_webscraper <user_email> --db_output cazy_database.db
```

Data from UniProt was retrieved for proteins in the local CAZyme database, and added to the datbase. The following data was retrieved:
- UniProt accession
- Protein name
- PDB accessions
- EC numbers

The retreival of data was limited to proteins from the following families of interest:
- GH1
- GH2
- GH3
- GH11
- GH26
- GH30
- GH43
- GH51
- GH52
- GH54
- GH116
- GH120

The retreival of the data can be repeated using the following command:
```bash
cw_get_uniprot_data cazy_database.db \
  --families GH1,GH2,GH3,GH11,GH26,GH30,GH43,GH51,GH52,GH54,GH116,GH120
  --ec \
  -- pdb
```

These data were downloaded in Feburary 2022. To faciltiate reproducing the analyses presenter here using this data set, a 
copy of this database is available in the [`data`]() directory of this repository.
