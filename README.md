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

**1.3.1. Extract protein sequences from genomes**

The Python script `cazomevolve/scripts/genomes/extract_gbk_proteins.py` was used to retrieve protein sequences and associated annotations from the downloaded GenBank genomic assebmlies.
```bash
python3 scripts/genomes/extract_gbk_proteins.py thermotogae_genomes/ thermotogae_proteins
```

XX of the genomes contained no protein annotations.

**1.3.2. Annotate genomes**

The XX genomes with no protein annotations were annotated using `prokka`  [Seemann, 2014].

> Seemann T. (2014) Prokka: rapid prokaryotic genome annotation. Bioinformatics. 30(14):2068-9

The bash script `cazomevolve/scripts/genomes/predict_cds_prokka.sh` was used to automate invoking `prokka` for all genomes retrieved from NCBI, and which did not contain any CDS features.
```bash
scripts/genomes/predict_cds_prokka.sh \
thermotogae_prokka_input \      # path to dir containing genomes that contain no CDS features
thermotogae_prokka_output \     # path to output dir to write prokka output to
thermotogae_dbcan_input \       # path to dir containing protein sequences to be parsed by dbCAN
| tee prokka_log_file.log       # write out a log file
```

The predicted proteins sequences were written out to one FASTA file per parsed genome, and stored in `thermotogae_dbcan_input`.

**1.3.3. Get CAZy annotated CAZymes**

`cazy_webscraper` [Hobbs et al 2021] was used to build a JSON file containing the CAZy family annotation of every protein in CAZy.

> Hobbs, Emma E. M.; Pritchard, Leighton; Chapman, Sean; Gloster, Tracey M. (2021): cazy_webscraper Microbiology Society Annual Conference 2021 poster. figshare. Poster. https://doi.org/10.6084/m9.figshare.14370860.v7

The Python script `cazomevolve/scripts/cazymes/get_cazy_cazymes.py` was used to retrieve the CAZy family annotations of CAZy annotated CAZymes. The CAZy family annotations were written out to tab delimited list, with one CAZy family annotation on each line, and each line containing the CAZy family followed by the genomic accession of the source genome.

Proteins not annotated by CAZy were written out to FASTA files, one FASTA file per species, which were written out to the `thermotogae_dbcan_input` directory.

**1.3.4. Get dbCAN annotated CAZymes**

The Python script `cazomevolve/scripts/cazymes/get_dbcan_cazymes.py` was used to invoke dbCAN for every FASTA file in the `thermotogae_dbcan_input` directory to predict the CAZy families of all contained proteins. The Python script also parsed the output from dbCAN and added the consensus CAZy family annotations to the same tab deliminted list from the step before (*1.3.3. Get CAZy annotated CAZymes*).

To repeat the analysis, use the following command:
```bash
python3 ...
```

#### 1.4 Add species names

All analysises up to this point identify each genome by its genomic accession. To make the data more human-readable, the tab deliminted list and pyani output were parsed, adding the organism name as a prefix to every genomic accession.

This was done by using the Python script `cazomevolve/scripts/add_organisms_names.py`:
```bash
python3 scripts/add_organisms_names.py thermotogae_fam_acc_list sp_thermotogae_fam_acc_list ANIm.tab sp_ANIm.tab
```

#### 1.5 CAZy family co-occurence search

`coinfinder` [Whelan et al., 2002] was used to identify CAZy families that co occure more often than expected from the species lineage.

To repeat the analysis use the following command:
```bash
coinfinder -i sp_thermotogae_fam_acc_list -p sp_ANIm.tab -a
```

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
