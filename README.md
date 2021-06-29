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

### 1. CAZy family co-occurence

`cazomevolve` was used to identify co-occurning CAZy families in the Thermotogae gnomes.

#### 1.1. Download genomes  

To download genomes from NCBI GenBank, the Python script `cazomevolve/scripts/genomes/download_genomes.py` was used, and called using the following command:
```bash
python3 scripts/genomes/download_genomes.py <user_email_address> Thermotogae gbff,fna thermotogae_genomes --gbk
```
Genomes were downloaded into both GenBank flat file and FASTA format and writte out the directory `thermotogae_genomes`. Assemblies from all assembly levels were retrieved.

#### 1.2. Reconstruct phylogenetic tree

To reconstruct the distance-based phylogenetic tree, `pyani` [Pritchard et al., 2016] was used to calculate the average nucleotide identity between all pairs of genomes retrieved from NCBI GenBank.

> Pritchard et al. (2016) "Genomics and taxonomy in diagnostics for food security: soft-rotting enterobacterial plant pathogens" Anal. Methods 8, 12-24

To repeat this analysis use the following command from this directory:
```bash
pyani -- average_nucleotide_identity.py \
-i thermotogae_genomes/  \         # path to directory containing downloaded .fna files
-o thermotogae_pyani_output/ \     # path to output directory
-l pyani_log.log \                 # write out log file
-v --nocompress --noclobber -g --gformat pdf,png,eps
```

The R script `cazomevolve/scripts/tree/build_distance_tree.R` was used to build a Newick-formatted distance tree.

#### 1.3. Annotate CAZomes
  
`cazy_webscraper` [Hobbs et al 2021] was used to build a JSON file containing the CAZy family annotation of every protein in CAZy.

> Hobbs, Emma E. M.; Pritchard, Leighton; Chapman, Sean; Gloster, Tracey M. (2021): cazy_webscraper Microbiology Society Annual Conference 2021 poster. figshare. Poster. https://doi.org/10.6084/m9.figshare.14370860.v7


### 2. Finding models for molecular replacement and comparison

#### 2.1. Build a CAZyme database

`cazy_webscraper` [Hobbs et al 2021] was used to build a local CAZyme database containing CAZymes from the CAZy classes GH and CE.

> Hobbs, Emma E. M.; Pritchard, Leighton; Chapman, Sean; Gloster, Tracey M. (2021): cazy_webscraper Microbiology Society Annual Conference 2021 poster. figshare. Poster. https://doi.org/10.6084/m9.figshare.14370860.v7

`cazy_webscraper` was invoked using the following command:
```bash
cazy_webscraper --database_dir Foltany_et_al_2022_cazyme_db --classes GH,CE
```

#### 2.2. Find potential proteins of interest

Via SQL and an SQL database browser, the local CAZyme database was queried to retrieve the records of proteins that:
- From the bacteria phylum Thermotogae
- From any of the following CAZy families
- Annotated with at least one of the following EC numbers

...

### 3. Phylogenetic tree re-construction
...
