# Foltanyi_et_al_2022

Welcome to the repository containing all scripts, commands and methods used in the bioinformatic analysis
presented in the paper Foltanyi _et al._, 2022.

This repo contains the commands and data files necessary to repeat the study presented in the paper.

## Contributors

- [Emma E. M. Hobbs](https://github.com/HobnobMancer), PhD candidate, University of St Andrews, James Hutton Institute and University of Strathclyde
- [Dr Leighton Pritchard](https://github.com/widdowquinn), University of Strathclyde
- Flora Foltanyi, PhD candidate, University of St Andrews
- Dr Tracey M. Gloster, University of St Andrews

## Requirements

- POISx or Mac OS, or linux emulator
- Python version 3.9+
- Miniconda3 or Anaconda managed microenvironment  
- Prodigal
- Coinfinder
- Pyani
- cazy_webscraper
- Cazomevolve
- get-ncbi-genomes

### Python packages
- tqdm

### R packages
- ape
- dplyr

## Method to reconstruct the analysis

To reconstruct the analysis run all commands from this directory.

The method is split into four sections:
1. [Construct a local CAZyme database](#construct-a-local-cazyme-database)
2. [Reconstructing the _Thermotoga_ genus phylogenetic tree](#reconstructing-the-thermotoga-genus-phylogenetic-tree)
3. [Selecting models for molecular replacement](#selecting-models-for-molecular-replacement)
4. [Identifying co-evolving CAZy families](#identifying-co-evolving-cazy-families)


## Construct a local CAZyme database

`cazy_webscraper` [Hobbs et al., 2021] (DOI:) was used to construct a local CAZyme database.

> Hobbs, Emma E. M.; Pritchard, Leighton; Chapman, Sean; Gloster, Tracey M. (2021): cazy_webscraper Microbiology Society Annual Conference 2021 poster. figshare. Poster. https://doi.org/10.6084/m9.figshare.14370860.v7

To reconstruct the database to repeat the analysis, use the following command from the root of this repository:
```bash
cazy_webscraper <user_email> --kingdoms bacteria --db_output cazy_database.db
```

The CAZy database was downloaded on 2022-01-28.

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
- CE1
- CE2
- CE3
- CE4
- CE5
- CE6
- CE7
- CE12
- CE16

The retreival of the data can be repeated using the following command:
```bash
cw_get_uniprot_data cazy_database.db \
  --families GH1,GH2,GH3,GH11,GH26,GH30,GH43,GH51,GH52,GH54,GH116,GH120,CE1,CE2,CE3,CE4,CE5,CE6,CE7,CE12,CE16
  --ec \
  -- pdb
```

## Reconstructing the _Thermotoga_ genus phylogenetic tree

To reconstruct the phylogenetic tree of _Thermotoga_ genus the method presented in [Hugouvieux-Cotte-Pattat _et al_., 2021](https://pure.strath.ac.uk/ws/portalfiles/portal/124038859/Hugouvieux_Cotte_Pattat_etal_IJSEM_2021_Proposal_for_the_creation_of_a_new_genus_Musicola_gen_nov_reclassification_of_Dickeya_paradisiaca.pdf) was used. The specific methodolgy is found in the [Hugouvieux-Cotte-Pattat _et al_. supplementary](https://widdowquinn.github.io/SI_Hugouvieux-Cotte-Pattat_2021/).

### 1. Download genomes

RefSeq genomic assemblies were retrieved from NCBI. The genomic accessions of the genomic assemblies used to 
reconstruct the phylogenetic tree are listed in `data/ref_genomes_of_interest_acc.txt`. This includes the 
RefSef genome of **_Fervidobacterium changbaicum_ CBS-1 GCF_004117075.1 as an out group**, to facilitate 
identifying the root of the _Thermotoga_ tree. The output group was selected based upon the 
the Thermotogae distance based tree (the method for construction is laid out further down), and was 
labelled with an assembly level of 'chromosome or greater' and genome representation labelled as 'full', in NCBI Assembly database.

The genomes were downloaded from NCBI using [`ncbi-genome-download`](https://github.com/kblin/ncbi-genome-download/).

To reproduce this download run the following command from the root of this repository:
```bash
scripts ncbi/download_genomes.sh \
  data/ref_genomes_of_interest_acc.txt
  ml_tree_genomes
```

25 genomes were downloaded and stored in the directory `ml_tree_genomes`. The accession numbers of the downloaded genomes are listed in `data/downloaded_genome_acc.txt`


### 2. CDS prediction

In order to ensure consistency of nomenclature and support back threading the nucleotides sequences onto 
aligned single-copy orthologues, all downloaded RefSeq genomes were reannotated using 
[`prodigal](https://github.com/hyattpd/Prodigal)

> Hyatt D, Chen GL, Locascio PF, Land ML, Larimer FW, Hauser LJ. Prodigal: prokaryotic gene recognition and translation initiation site identification. BMC Bioinformatics. 2010 Mar 8;11:119. doi: 10.1186/1471-2105-11-119. PMID: 20211023; PMCID: PMC2848648.

To reproduce the annotation of the genomes, run the `annotate_genomes_prodigal.sh` script from the root of 
this repository.
```bash
scripts/reconstruct_tree/ml_tree/annotate_genomes_prodigal.sh ml_tree_genomes
```
Only one argument is provided: the path to the directory containing the downloaded genomes.

The output from `prodigal` are placed in the following directories:
- The predicted CDS are placed in the `genomes/cds` directory
- The conceptural translations are placed in `genomes/proteins`
- The GenBank formate files are placed in the `genomes/gbk` directory

A log of the `prodigal` terminal output was placed in `data/logs/prodigal.log`.


### 3. Identifying Single-Copy Orthologues (SCOs)

Orthologues present in the RefSeq _Thermotoga_ genomes were identified using [`orthofinder`](https://github.com/davidemms/OrthoFinder)

> Emms, D.M. and Kelly, S. (2019) OrthoFinder: phylogenetic orthology inference for comparative genomics. [Genome Biology 20:238](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-019-1832-y)

To reproduce the identifcation of orthologues, run the following command from the root of this repository:
```bash
scripts/reconstruct_tree/ml_tree/get_scos.sh \
  ml_tree_genomes/proteins \
  orthologues
```
To arguments are provided:
1. The path to the directory containing the FASTA files of predicted protein sequences from `prodigal`
2. A path to an output directory

The output from `orthofinder` was written to the `orthologues/Results_Nov11/Single_Copy_Orthologue_Sequences` directory.

`orthofinder` assigned 46086 genes (98.6% of total) to 2662 orthogroups. Fifty percent of all genes were in orthogroups with 25 or more genes (G50 was 25) and were contained in the largest 889 orthogroups (O50 was 889). There were 990 orthogroups with all species present and 828 of these consisted entirely of single-copy genes.

`orthofinder` identified genome GCF_004117075.1 as the best out group.


### 4. Multiple Sequence Alignment

Each collection of single-copy orthologous was aligned using [`MAFFT`](https://mafft.cbrc.jp/alignment/software/).

> Nakamura, Yamada, Tomii, Katoh 2018 (Bioinformatics 34:2490–2492)
Parallelization of MAFFT for large-scale multiple sequence alignments.
(describes MPI parallelization of accurate progressive options) 

To reproduce the MSA, run following command from the root of this repository.
```bash
scripts/reconstruct_tree/ml_tree/align_scos.sh \
  orthologues/Results_Nov11/Single_Copy_Orthologue_Sequences
```

The output from `MAFFT` (the aligned files) are placed in the `sco_proteins_aligned` directory.


### 5. Collect Single-Copy Orthologues CDS sequences

The CDS sequences corresponding to each set of single-copy orthologues are identified and extracted with the Python script `extract_cds.py`. To reproduce this analysis, ensure the `PROTDIR` constant in the script is 
directed to the correct output directory for orthofinder. The script can then be run from the current directory with:

```bash
python3 scripts/reconstruct_tree/ml_tree/extract_cds.py
```

The output is a set of unaligned CDS sequences corresponding to each single-copy orthologue, which are 
placed in the `sco_cds` directory


### 6. Back-translate Aligned Single-Copy Orthologues

The single-copy orthologue CDS sequences are threaded onto the corresponding aligned protein sequences using [`t-coffee`](http://www.tcoffee.org/Projects/tcoffee/).

> T-Coffee: A novel method for multiple sequence alignments. Notredame, Higgins, Heringa, JMB, 302(205-217)2000

The results can be reproduced by executing the `backtranslate.sh` script from this directory.

```bash
scripts/reconstruct_tree/ml_tree/backtranslate.sh \
  sco_proteins_aligned \
  sco_cds_aligned
```

The backtranslated CDS sequences are placed in the `sco_cds_aligned` directory.


### 7. Concatenating CDS into a Multigene Alignment

The threaded single-copy orthologue CDS sequences are concatenated into a single sequence per input organism using the Python script `concatenate_cds.py`. To reproduce this, execute the script from this directory with:

```bash
python scripts/reconstruct_tree/concatenate_cds.py
```

Two files are generated, a FASTA file with the concatenated multigene sequences, and a partition file allowing a different set of model parameters to be fit to each gene in phylogenetic reconstruction.


### 8. Phylogenetic reconstruction

To reconstruct the phylogenetic tree, the bash script `raxml_ng_build_tree.sh` is used, and is 
run from the root of this repository. This executes a series of [`raxml-ng`](https://github.com/amkozlov/raxml-ng) commands.

```bash
scripts/reconstruct_tree/raxml_ng_build_tree.sh \
  concatenated_cds
```

The `raxml-ng parse` command estimated memory and processor requirements as

```text
* Estimated memory requirements                : 6428 MB
* Recommended number of threads / MPI processes: 77
```

but, as we had limited access to computing resource at the time, we had to proceed with 8 cores.

All genes were considered as separate partitions in the reconstuction, 
with parameters estimated  for the `GTR+FO+G4m+B` model (as recommended by `raxml-ng check`).

The log files from `raxml-ng` are stored in `data/raxmlng_tree_reconstruction`.

Tree reconstructions are placed in the `tree` directory. The best estimate tree is `03_infer.raxml.bestTree` and the midpoint-rooted, manually-annotated/coloured tree (using [`figtree`](http://tree.bio.ed.ac.uk/software/figtree/)) is `03_infer.raxml.bestTree.annotated`

> Alexey M. Kozlov, Diego Darriba, Tomáš Flouri, Benoit Morel, and Alexandros Stamatakis (2019) RAxML-NG: A fast, scalable, and user-friendly tool for maximum likelihood phylogenetic inference. Bioinformatics, btz305 [doi:10.1093/bioinformatics/btz305](https://doi.org/10.1093/bioinformatics/btz305)



## Selecting models for molecular replacement

Via SQL and an SQL database browser, the local CAZyme database was queried with the aim to retrieve functionally relevant proteins, to generate an MSA of functional relevant proteins for molecular modeling. 

A list of all SQL queries performed and the output is presented [here](https://hobnobmancer.github.io/Foltanyi_et_al_2022/sql_queries/).

In summary, from the CAZy families of interest, 560 proteins were annotated with the EC number 3.2.1.37, indicating they potentially had the function of interest.

`cazy_webscraper` was used to retrieve the GenBank protein sequences for these 560 proteins.

[`MMSeq2`](https://github.com/soedinglab/MMseqs2) was used to cluster the proteins with a percentage identity and coverage cut-off of 80%.

To repeat this analysis, run the following code from the root of the repository, using a fasta file called ec_proteins_seqs.fasta
which contains all bacterial proteins retieved with the EC number of interest. This analysis also uses the Python script `get_clusters.py`, which 
parses the MMseq output to create a `csv` file with the size of each cluster, and a `JSON` file containing the GenBank accessions for each cluster.

```bash
# make an output directory
mkdir mmseq_cluster_80

# create the db
mmseqs createdb ec_proteins_seqs.fasta mmseq_cluster_80/mmseq_db_80

# cluster the proteins
mmseqs cluster mmseq_cluster_80/mmseq_db_80 \
  mmseq_cluster_80/mmseq_db_80_output \
  mmseq_cluster_80/mmseq_db_80/tmp \
  --min-seq-id 0.8 -c 0.8

# create tsv
mmseqs createtsv \
  cluster mmseq_cluster_80/mmseq_db_80 \
  cluster mmseq_cluster_80/mmseq_db_80 \
  mmseq_cluster_80/mmseq_db_80_output \
  mmseq_cluster_80/mmseq_db_80_output.tsv

# get summary
python3 get_clusters.py \
  mmseq_cluster_80/mmseq_db_80_output.tsv \
  mmseq_cluster_80/mmseq_cluster_summary.csv \
  mmseq_cluster_80/mmseq_clusters.json
```

This produced 420 clusters. Only 2 clusters contained more than 10 proteins, each contained 17 proteins sequences. All remaining clusters contained less than 10 proteins, 366 clusters contained only 1 proteins.

`MMSeq2` was used to cluster the protein again, but with a percentage identity and coverage cut-off of 70% with the aim to increase the cluster sizes.

To repeat this analysis, run the following code from the root of the repository, using a fasta file called ec_proteins_seqs.fasta
which contains all bacterial proteins retieved with the EC number of interest.

```bash
# make an output directory
mkdir mmseq_cluster_70

# create the db
mmseqs createdb ec_proteins_seqs.fasta mmseq_cluster_70/mmseq_db_70

# cluster the proteins
mmseqs cluster mmseq_cluster_70/mmseq_db_70 \
  mmseq_cluster_70/mmseq_db_70_output \
  mmseq_cluster_70/mmseq_db_70/tmp \
  --min-seq-id 0.7 -c 0.7

# create tsv
mmseqs createtsv \
  cluster mmseq_cluster_70/mmseq_db_70 \
  cluster mmseq_cluster_70/mmseq_db_70 \
  mmseq_cluster_70/mmseq_db_70_output \
  mmseq_cluster_70/mmseq_db_70_output.tsv

# get summary
python3 get_clusters.py \
  mmseq_cluster_70/mmseq_db_70_output.tsv \
  mmseq_cluster_70/mmseq_cluster_summary.csv \
  mmseq_cluster_70/mmseq_clusters.json
```

This produced 346 clusters. The 4 largest clusters contained 33, 28, 17 and 13 proteins each. All remaining clusters contained less than 10 proteins, 227 of which contained only 1 protein.

The JSON file containing the GenBank accessions of each cluster compiled by `MMSeq2` can be found [here](https://github.com/HobnobMancer/Foltanyi_et_al_2022/blob/master/supplementary/cluster_data/clusters_70.json).

A representative sequence from each of the 4 largest clusters from this second clustering were compared using BLASTP all-versus-all, using the Python script `run_blastp.py` from the Python package [`pyrewton` DOI:10.5281/zenodo.3876218)](https://github.com/HobnobMancer/pyrewton).

The R notebook `cluster_analysis.Rmd` was used to parse and analyse the results. This notebook can be viewed [here](https://hobnobmancer.github.io/Foltanyi_et_al_2022/supplementary/cluster_data/cluster_analysis.html) and found [here](https://github.com/HobnobMancer/Foltanyi_et_al_2022/tree/master/supplementary/cluster_data).

The GenBank accessions for each of the 4 largest clusters were extracted to plain text files, with one unique GenBank accession per row. These files can be found here:
- [AGE22437_1.txt](https://github.com/HobnobMancer/Foltanyi_et_al_2022/blob/master/supplementary/cluster_data/AGE22437_1.txt)
- [CBK6950_1.txt](https://github.com/HobnobMancer/Foltanyi_et_al_2022/blob/master/supplementary/cluster_data/CBK6950_1.txt)
- [CDG29680_1.txt](https://github.com/HobnobMancer/Foltanyi_et_al_2022/blob/master/supplementary/cluster_data/CDG29680_1.txt)
- [QJR11213_1.txt](https://github.com/HobnobMancer/Foltanyi_et_al_2022/blob/master/supplementary/cluster_data/QJR11213_1.txt)

These text files were parsed by `cazy_webscraper` in order to extract the GenBank protein sequences of all proteins in each cluster, and write the protein sequences to a FASTA file. One FASTA file per cluster was compiled.

```bash
cw_extract_db_sequences cazy_database.db genbank AGE22437_1.txt --fasta_file AGE22437_1.fasta -f -n
cw_extract_db_sequences cazy_database.db genbank CBK6950_1.txt --fasta_file CBK6950_1.fasta -f -n
cw_extract_db_sequences cazy_database.db genbank CDG29680_1.txt --fasta_file CDG29680_1.fasta -f -n
cw_extract_db_sequences cazy_database.db genbank QJR11213_1.txt --fasta_file QJR11213_1.fasta -f -n
```

The Python script `run_blastp.py` from [`pyrewton` DOI:10.5281/zenodo.3876218)](https://github.com/HobnobMancer/pyrewton) was used to run a BLASTP all-vs-all analysis for each cluster. The results of which can be viewed [here](https://hobnobmancer.github.io/Foltanyi_et_al_2022/supplementary/cluster_data/cluster_analysis.html#4_Sequence_divergence_in_individual_clusters).

The BLASTP all-versus-all of the representative proteins from each cluster inferred the AGE224371.1 and CDG296801.1 clusters had relatively low sequence diveregence across all proteins from the two clusters. To futher explore this, a BLASTP all-versus-all of all proteins in the two clusters was performed, and demonstrated high sequence similarity across the two clusters. The BLAST score ratios of the BLASTP analysis can be found [here](https://hobnobmancer.github.io/Foltanyi_et_al_2022/supplementary/cluster_data/cluster_analysis.html#51_AGE224371_and_CDG296801).

The sequence diveregence when pooling all proteins from the 4 clusters was also explored, and demonstrated a relatively high sequence similarity across the entire protein pool. The BLAST score ratios of the BLASTP analysis can be found [here](https://hobnobmancer.github.io/Foltanyi_et_al_2022/supplementary/cluster_data/cluster_analysis.html#52_Sequence_divergence_across_all_4_clusters).



## Identification of neighbouring genes

...



## Identifying co-evolving CAZy families

### 1. CAZy family co-occurence

`cazomevolve` was used to identify co-occurning CAZy families in the Thermotogae gnomes.

#### 1.1. Download genomes  

To download genomes from NCBI GenBank, the Python script from `cazomevolve` `cazomevolve/scripts/genomes/download_genomes.py` was used, and called from the root of the `cazomevolve` repo, using the following command:
```bash
python3 scripts/genomes/download_genomes.py \
  <user_email_address> \
  Thermotogae \
  gbff,fna \
  thermotogae_genomes \
  --gbk
```

Genomes were downloaded into both GenBank flat file and FASTA format and writte out the directory `thermotogae_genomes`. Assemblies from all assembly levels were retrieved.

#### 1.2. Reconstruct phylogenetic tree

To reconstruct the distance-based phylogenetic tree, `pyani` [Pritchard et al., 2016] was used to calculate the average nucleotide identity between all pairs of genomes retrieved from NCBI GenBank.

> Pritchard et al. (2016) "Genomics and taxonomy in diagnostics for food security: soft-rotting enterobacterial plant pathogens" Anal. Methods 8, 12-24

To repeat this analysis use the following command from this directory:
```bash
scripts/reconstruct_tree/distance_tree/pyani_ani.sh \
  thermotogae_genomes/  \         # path to directory containing downloaded .fna files
  thermotogae_pyani_output/ \     # path to output directory
  pyani_log.log                  # write out log file
```

The tabular data from `pyani` is stored in the [supplementary dir](https://github.com/HobnobMancer/Foltanyi_et_al_2022/tree/master/supplementary) of this repository.
The graphical output is stored in the same directory, as well as being viewable here:  
- [Alignment coverage](https://hobnobmancer.github.io/Foltanyi_et_al_2022/supplementary/pyani_output/ANIm_alignment_coverage.pdf)
- [Percentage identity](https://hobnobmancer.github.io/Foltanyi_et_al_2022/supplementary/pyani_output/ANIm_percentage_identity.pdf)
- [Alignment lengths](https://hobnobmancer.github.io/Foltanyi_et_al_2022/supplementary/pyani_output/ANIm_alignment_lengths.pdf)

From `cazomevolve`, the R script `cazomevolve/scripts/tree/build_distance_tree.R` was used to build a Newick-formatted distance tree.

#### 1.3. Annotate CAZomes

**1.3.1. Extract protein sequences from genomes**

The Python script `cazomevolve/scripts/genomes/extract_gbk_proteins.py` was used to retrieve protein sequences and associated annotations from the downloaded GenBank genomic assebmlies.
```bash
python3 scripts/genomes/extract_gbk_proteins.py \
  thermotogae_genomes/ \
  thermotogae_proteins
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

From `cazomevolve`, Python script `cazomevolve/scripts/cazymes/get_cazy_cazymes.py` was used to retrieve the CAZy family annotations from the local CAZyme database (created using `cazy_webscraper`) for proteins extracted from 
the genomic assemblies. 

The CAZy family annotations were written out to tab delimited list, with one CAZy family annotation on each line, and each line containing the CAZy family followed by the genomic accession of the source genome.

To repeat this analysis, use the following command:
```bash
python3 scripts/cazymes/get_cazy_cazymes.py \
  thermotogae_proteins \
  cazy_database.db \
  thermotogae_dbcan_input \
  thermotogae_fam_acc_list \
  -f \
  -n 
```
To repeat the analysis make sure the `--force` (`-f`) and `--nodelete` (`-n`) flags are used so that the data can be added to the `thermotogae_dbcan_input` directory without deteling the predicted protein sequences from `prokka`.

2,555 CAZy family annotations were retrieved.

Proteins not annotated by CAZy were written out to FASTA files, one FASTA file per species, which were written out to the `thermotogae_dbcan_input` directory.

**1.3.4. Get dbCAN annotated CAZymes**

From `cazomevolve` the Python script `cazomevolve/scripts/cazymes/get_dbcan_cazymes.py` was used to invoke dbCAN for every FASTA file in the `thermotogae_dbcan_input` directory to predict the CAZy families of all contained proteins. 

The Python script also parsed the output from dbCAN and added the consensus CAZy family annotations to the same tab deliminted list from the step before (*1.3.3. Get CAZy annotated CAZymes*).

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
coinfinder \
  -i sp_thermotogae_fam_acc_list 
  -p sp_ANIm.tab \
  -a
```

To produce the circular phylogenetic tree and heatmap, with the coloured annotations, a modified version of the 
R script `aasd` from `coinfinder` was used. A copy of the modified R script is stored in `scripts/R/...`. Use 
this modified file instead of the original R file to recreate the analysis. Additional modifications to the script 
maybe required if a different data set is used.

### 2. Finding models for molecular replacement and comparison

#### 2.1. Build a CAZyme database

`cazy_webscraper` [Hobbs et al 2021] was used to build a local CAZyme database containing CAZymes from the CAZy classes GH and CE.

> Hobbs, Emma E. M.; Pritchard, Leighton; Chapman, Sean; Gloster, Tracey M. (2021): cazy_webscraper Microbiology Society Annual Conference 2021 poster. figshare. Poster. https://doi.org/10.6084/m9.figshare.14370860.v7

`cazy_webscraper` was invoked using the following command:
```bash
cazy_webscraper --database_dir Foltany_et_al_2022_cazyme_db --classes GH,CE
```
