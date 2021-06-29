# Foltanyi_et_al_2022
Bioinformatics work for the paper Foltanyi et al., 2022

## Requirements

- POISx or Mac OS, or linux emulator
- Python version 3.9+
- Miniconda3 or Anaconda managed microenvironment  
- Prokka
- Coinfinder
- Pyani

### Python packages
- tqdm

### R packages
- ape
- dplyr

## Method to reconstruct the analysis

To reconstruct the analysis run all commands from this directory.

### CAZy family co-occurence

`cazomevolve` was used to identify co-occurning CAZy families in the Thermotogae gnomes.

### Finding models for molecular replacement and comparison

#### Build a CAZyme database

`cazy_webscraper` [Hobbs et al 2021] was used to build a local CAZyme database containing CAZymes from the CAZy classes GH and CE.

> Hobbs, Emma E. M.; Pritchard, Leighton; Chapman, Sean; Gloster, Tracey M. (2021): cazy_webscraper Microbiology Society Annual Conference 2021 poster. figshare. Poster. https://doi.org/10.6084/m9.figshare.14370860.v7

`cazy_webscraper` was invoked using the following command:
```bash
cazy_webscraper --database_dir Foltany_et_al_2022_cazyme_db --classes GH,CE
```

#### Find potential proteins of interest

Via SQL and an SQL database browser, the local CAZyme database was queried to retrieve the records of proteins that:
- From the bacteria phylum Thermotogae
- From any of the following CAZy families
- Annotated with at least one of the following EC numbers

...

### Phylogenetic tree re-construction

...
