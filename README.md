# Foltanyi_et_al_2022

Bioinformatics work for the paper Foltanyi et al., 2022

This repo contains the commands and data files necessary to repeat the study presented in Foltanyi et al., 2022.

## Requirements

- POISx or Mac OS, or linux emulator
- Python version 3.9+
- Miniconda3 or Anaconda managed microenvironment  
- Prodigal
- Coinfinder
- Pyani

### Python packages
- tqdm

### R packages
- ape
- dplyr

## Method to reconstruct the analysis

To reconstruct the analysis run all commands from this directory.

The method is split into three sections:
1. [Reconstructing the _Thermotoga_ genus phylogenetic tree](#reconstructing-the-thermotoga-genus-phylogenetic-tree)
2. [Selecting models for molecular replacement](#selecting-models-for-molecular-replacement)
3. [Identifying co-evolving CAZy families](#identifying-co-evolving-cazy-families)


## Reconstructing the _Thermotoga_ genus phylogenetic tree

To reconstruct the phylogenetic tree of _Thermotoga_ genus the method presented in [Hugouvieux-Cotte-Pattat _et al_., 2021](https://pure.strath.ac.uk/ws/portalfiles/portal/124038859/Hugouvieux_Cotte_Pattat_etal_IJSEM_2021_Proposal_for_the_creation_of_a_new_genus_Musicola_gen_nov_reclassification_of_Dickeya_paradisiaca.pdf) was used. The specific methodolgy is found in the [Hugouvieux-Cotte-Pattat _et al_. supplementary](https://widdowquinn.github.io/SI_Hugouvieux-Cotte-Pattat_2021/).


### Download genomes

RefSeq genomic assemblies retrieved from NCBI. The genomic accessions of the genomic assemblies used to 
reconstruct the phylogenetic tree are listed in `data/ref_genomes_of_interest_acc.txt`. This includes the 
RefSef genome of _Fervidobacterium changbaicum CBS-1 GCF_004117075.1, to be used as an out group in order 
to facilitate identifying the root of the _Thermotoga_ tree. The output group was selected based upon the 
the Thermotogae distance based tree (the method for construction is laid out further down), and was labelled as at the assembly level of chromosome or greater with genome representation labelled as 'full', in NCBI Assembly database.

The genomes were downloaded from NCBI using [`ncbi-genome-download`](https://github.com/kblin/ncbi-genome-download/).

To reproduce this download run the following command from the root of this repository:
```bash
# Download files
ncbi-genome-download \
    --assembly-accessions data/ref_genomes_of_interest_acc.txt \
    --formats fasta \
    --output-folder genomes \
    --flat-output \
    -v \
    bacteria

# Extract sequences
gunzip genomes/*.gz
```

25 genomes were downloaded. The accession numbers of the downloaded genomes are listed in `data/downloaded_genome_acc.txt`


### CDS prediction

In order to ensure consistency of nomenclature and support back threading the nucleotides sequences onto 
aligned single-copy orthologues, all downloaded RefSeq genomes were reannotated using 
[`prodigal](https://github.com/hyattpd/Prodigal)

> Hyatt D, Chen GL, Locascio PF, Land ML, Larimer FW, Hauser LJ. Prodigal: prokaryotic gene recognition and translation initiation site identification. BMC Bioinformatics. 2010 Mar 8;11:119. doi: 10.1186/1471-2105-11-119. PMID: 20211023; PMCID: PMC2848648.

To reproduce the annotation of the genomes, run the `annotate_genomes_prodigal.sh` script from the root of 
this repository.
```bash
scripts/reconstruct_tree/annotate_genomes_prodigal.sh
```

The output from `prodigal` are placed in the following directories:
- The predicted CDS are placed in the `genomes/cds` directory
- The conceptural translations are placed in `genomes/proteins`
- The GenBank formate files are placed in the `genomes/gbk` directory

A log of the `prodigal` terminal output was placed in `data/logs/prodigal.log`.


### Identifying Single-Copy Orthologues (SCOs)

Orthologues present in the RefSeq _Thermotoga_ genomes were identified using [`orthofinder`](https://github.com/davidemms/OrthoFinder)

> Emms, D.M. and Kelly, S. (2019) OrthoFinder: phylogenetic orthology inference for comparative genomics. [Genome Biology 20:238](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-019-1832-y)

To reproduce the identifcation of orthologues, run the following command from the root of this repository:
```bash
# Change soft limit on simultaneously open files
ulimit -n 5000

# Run orthofinder
orthofinder -f genomes/proteins \
  -o orthologues
```

The output from `orthofinder` was written to the `orthologues/Results_Nov11/Single_Copy_Orthologue_Sequences` directory.

`orthofinder` assigned 46086 genes (98.6% of total) to 2662 orthogroups. Fifty percent of all genes were in orthogroups with 25 or more genes (G50 was 25) and were contained in the largest 889 orthogroups (O50 was 889). There were 990 orthogroups with all species present and 828 of these consisted entirely of single-copy genes.

`orthofinder` identified genome GCF_004117075.1 as the best out group.


### Multiple Sequence Alignment

Each collection of single-copy orthologous was aligned using [`MAFFT`](https://mafft.cbrc.jp/alignment/software/).

> Nakamura, Yamada, Tomii, Katoh 2018 (Bioinformatics 34:2490–2492)
Parallelization of MAFFT for large-scale multiple sequence alignments.
(describes MPI parallelization of accurate progressive options) 

To reproduce the MSA, run following command from the root of this repository.
```bash
scripts/reconstruct_tree/align_scos.sh <path to dir containing SCO identified using orthofinder>
```
For example:
```bash
scripts/reconstruct_tree/align_scos.sh orthologues/Results_Nov11/Single_Copy_Orthologue_Sequences
```

The output from `MAFFT` (the aligned files) are placed in the `sco_proteins_aligned` directory.


### Collect Single-Copy Orthologues CDS sequences

The CDS sequences corresponding to each set of single-copy orthologues are identified and extracted with the Python script `extract_cds.py`. To reproduce this analysis, ensure the `PROTDIR` constant in the script is 
directed to the correct output directory for orthofinder. The script can then be run from the current directory with:

```bash
python3 scripts/reconstruct_tree/extract_cds.py
```

The output is a set of unaligned CDS sequences corresponding to each single-copy orthologue, which are 
placed in the `sco_cds` directory



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
-v -g --gformat pdf,png,eps
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

To repeat this analysis, use the following command:
```bash
python3 scripts/cazymes/get_cazy_cazymes.py thermotogae_proteins <path to JSON file created using cazy_webscraper> thermotogae_dbcan_input thermotogae_fam_acc_list -f -n
```
To repeat the analysis make sure the `--force` and `--nodelete` flags are used so that the data can be added to the `thermotogae_dbcan_input` directory without deteling the predicted protein sequences from `prokka`.

2,555 CAZy family annotations were retrieved.

Proteins not annotated by CAZy were written out to FASTA files, one FASTA file per species, which were written out to the `thermotogae_dbcan_input` directory.

**1.3.4. Get dbCAN annotated CAZymes**

The Python script `cazomevolve/scripts/cazymes/get_dbcan_cazymes.py` was used to invoke dbCAN for every FASTA file in the `thermotogae_dbcan_input` directory to predict the CAZy families of all contained proteins. The Python script also parsed the output from dbCAN and added the consensus CAZy family annotations to the same tab deliminted list from the step before (*1.3.3. Get CAZy annotated CAZymes*).

To repeat the analysis, use the following command:
```bash
python3 ...
```

Combining CAZy annotated and dbCAN annotated CAZymes identified XXXX total CAZymes across all 263 genomes.

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
