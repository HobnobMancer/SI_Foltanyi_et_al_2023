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
- `Miniconda3` or `Anaconda` managed microenvironment  
- `Prodigal`
- `HMMER` >= 3.3
- `Coinfinder`
- `Pyani`
- `cazy_webscraper` >= 2.0.0
- `Cazomevolve`
- `get-ncbi-genomes`
- `dbCAN` >= [3.0.2](https://github.com/linnabrown/run_dbcan)

**Note on install dbCAN:** Paths are hardcoded in `dbCAN` v2.0.11, therefore, to use `dbCAN` in this analysis, follow 
the exact instructions provided in the `dbCAN` [README]((https://github.com/linnabrown/run_dbcan)) and run the commands in the `scripts/cazome_annotation` directory.

### Python packages
- tqdm

### R packages
- ape
- dplyr

## Data, results and scripts

All **scripts** used in this analysis are stored in the `scripts` directory in the repo.  

**Input data** for the analysis, such as FASTA files, are stored in the `data` directory.  

**Results** data from this analysis, such as R markdown notebooks and MSA files, are stored in the `results` directory.

## Method to reconstruct the analysis

To reconstruct the analysis run all commands from this directory.

The method is split into four sections:
1. [Construct a local CAZyme database](#construct-a-local-cazyme-database)
2. [Systematic exploration of tmgh3](#systematic-exploration-of-tmgh3)
3. [Exploration of a GH3-CE complex](#exploration-of-a-gh3-ce-complex)
  - [Reconstructing the _Thermotoga_ genus phylogenetic tree](#reconstructing-the-thermotoga-genus-phylogenetic-tree)
  - [Annotate the CAZomes](#annotate-the-cazomes)
  - [Run `FlaGs`](#run-flags)
  - [GH3 flanking genes](#gh3-flanking-genes)


## Construct a local CAZyme database

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

## Systematic exploration of tmgh3

### 1. Query against the NR database

As a preliminary search to identify potentially functionally similar proteins to infer functional and structural information about tmgh3, the 
[non-redundant database](https://www.ncbi.nlm.nih.gov/refseq/about/nonredundantproteins/#related-documentation) was queried using BLASTP.

> Altschul, S. F., Gish, W., Miller, W., Myers, E. W., Lipman, D. J. (1990) 'Basic local alignment search tool', Journal of Molecular Biology, 215(3), pp. 403-10

This was done via the NCBI BLASTP (webinterface)[https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastp&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome] using default query parameters.

The reults of the query against the NR database were stored in a [csv file]().

A 70% identity cut-off was used to select proteins, which is widely accepted as a reasonably cut-off for selecting proteins that share the first 3 digits of their respective EC numbers.

### 2. Query against the CAZy database
The analysis presented in Folasdas _et al._ using HHpred was repeated using the MSA of potentially functionally relevant proteins, with the aim to identify more functionally relevant proteins than querying with only the protein sequence of interest.

### 3. Interrogation of the CAZy database
SQL commands... why does our protein come up with so few hits?

### 4. Repeating the analysis using HHpred
Generation of an MSA...

Using the MSA did not signficantly increase the number of functionally relevant hits returned by HHpred. In general, the results between the two queries were similar. This potentially reflects the limited knowledge pool for _Thermotoga_ glycoside hydrolase GH3 proteins.

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

Owing to the overall high sequence similarity across the entire protein pool, all 91 protein sequences were aligned using `MAFFT`.
```bash
# FASTA output
mafft --thread 12 mafft --thread 12 data/cluster_data/all_clusters.fasta > supplementary/cluster_data/all_clusters_aligned.fasta
# CLUSTAL output
mafft --thread 12 --clustalout data/cluster_data/all_clusters.fasta > supplementary/cluster_data/all_clusters_aligned.clustal
```

The total number of proteins in across all 4 clusters was 91. This included 0 proteins with PDB accessions listed in UniProt. The following SQL command was used to retrive the results:

```sql
WITH Ec_Query (ec_gbk_acc) AS (
	SELECT DISTINCT Genbanks.genbank_accession
	FROM Genbanks
	INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
	INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
	WHERE Ecs.ec_number = '3.2.1.37'
)
SELECT DISTINCT Genbanks.genbank_accession, Pdbs.pdb_accession
FROM Genbanks
INNER JOIN Pdbs ON Genbanks.genbank_id = Pdbs.genbank_id
LEFT JOIN Ec_Query ON Genbanks.genbank_accession = Ec_Query.ec_gbk_acc
WHERE (Genbanks.genbank_accession IN Ec_Query)
```

To further expand the pool of potentially functionally relevant proteins, the proteins from the CAZy families of interest (listed below) which were not included in the clusters were BLASTP queries against the members of the 4 clusters. Specifically:

1. `cazy_webscraper` was used to extract the GenBank protein sequences for all proteins in the Glycoside Hydrolase families of interest:
```bash
cw_extract_db_sequences \
  cazy_database.db \
  genbank \
  --families GH1,GH2,GH3,GH11,GH26,GH30,GH43,GH51,GH52,GH54,GH116,GH120 \
  --fasta_file all_fam_seqs.fasta \
  -f -n
```

2. The Python script `remove_duplicate_seqs.py` was run from the root of the repository and used to remove proteins from the `all_fam_seqs.fasta` file (containing protein sequences for the GH CAZy families of interest) that were already in the one of the 4 clusters of interest.
```bash
python3 scripts/molecular_modeling/remove_duplicate_seqs.py \
  data/molecular_modeling/all_fam_seqs.fasta
```

3. [`Trimal`](http://trimal.cgenomics.org/trimal) () (version 1.4.1) was used to trim the MSA, by removing all columns with gaps in more than 20% of the sequences:

> Capella-Gutierrez, S., Silla-Martinez, J. M., Gabaldon, T. (2009) 'trimAl: a tool for automated alignment trimming in large-scale phylogenetic analyses', Bioinformatics, 25, pp. 1972-1973

```bash
# run from the root of the repository
trimal -in data/cluster_data/all_clusters_aligned.fasta -out data/cluster_data/trimed_aligned_clusters.fasta -gt 0.8
```

4. A HMM model of the protein sequences across all 4 protein clusters of interest was constructed using [`HMMBuild`](http://rothlab.ucdavis.edu/genhelp/hmmerbuild.html) (Eddy, 2008) using default parameters.

> Eddy, S. R. (2008) 'A Probabilistic Model of Local Sequence Alignment that Simplifies Statistical Significance Estimation', _PloS Comput. Biol._, 4, pp. e1000069.

To rerun this analysis, run the following command in the root of this repository:
```bash
hmmbuild \
	-n supplementary/cluster_data/ec_cluster_hmm \
	-o supplementary/cluster_data/ec_cluster_hmm_summary \
	-O supplementary/cluster_data/ec_cluster_msa \
	--amino \
	supplementary/cluster_data/ec_cluster_phmm \
	supplementary/cluster_data/trimed_aligned_clusters.fasta
```
This produces a HMM profile, called [`ec_cluster_phmm`]().

5. Determine the bitscore cut-offs for using the pHMM to identify potentially functionally relevant proteins.

By default [`HMMERSearch`](https://academic.oup.com/nar/article/41/12/e121/1025950?login=false) (Mistry _et al.,_ 2013) uses a E-value threshold to identify candidates of interest. However, the E-value is database size dependent and is a measure of the significance of the hit against the size of the database. The bitscore is a measure of the statistical significance of the alignment.

> Mistry, J., Finn, R. D., Eddy, S. R., Bateman, A., Punta, M. (2013) 'Challenges in Homology Search: HMMER3 and Convergent Evolution of Coiled-Coil Regions', Nucleic Acids Research, 41, pp. e121

The **'noise cut-off' (NC)** bitscore was calculated by querying a set of proteins known negatives, in this case proteins that do not have ability to catalyse the reaction represented by the EC number 3.2.1.37.

Initally, bacterial protein sequences from the Glycosidetransferase (GT) family GT10 were selected as known negatives for calculating the NC. This was because all GT CAZymes are involved the synthesis of oligo- and polysaccharides, and do not posses functions related to the degradation of polysaccharides, which the catalytic reaction represented by the EC number 3.2.1.37 is associated with. The GT10 protein sequences were retrieved from NCBI, added to the local CAZyme database and extracted from the local CAZyme database using `cazy_webscraper`. However, even with a E-value cut-off of 1000, no hits between the bacterial GT10 protein sequences and the pHMM were found by `Hmmsearch`.

Instead, bacterial proteins with the EC number 2.4.1.12 (a UDP-glucose--beta-glucan glucosyltransferase) were selected at the known negatives for calculating the NC score.
```bash
cw_get_genbank_seqs \
	data/cazy_database.db <email_address> --ec_filter 2.7.1.12
cw_extract_db_sequences \
	datacazy_database.db genbank \
	--ec_filter \
	--fasta_file data/cluster_data/2-7-1-12_protein_seqs.fasta
```
**110** bacterial protein sequences were retrieved from the local CAZyme database and written to the fasta file `data/cluster_data/2-7-1-12_protein_seqs.fasta`.

`Hmmsearch` was then used to query these protein sequences against the constructed pHMM.
```
hmmsearch \
	-o supplementary/cluster_data/ec_hmm_search_nc_results \
	-A supplementary/cluster_data/ec_hmm_search_nc_alignment \
	--tblout supplementary/cluster_data/ec_hmm_search_nc_tab \
	supplementary/cluster_data/ec_cluster_phmm \
	data/cluster_data/2-7-1-12_protein_seqs.fasta
```
The NC was defined as the largest valued returned from `HMMER`, which was **a**.  
All output files are stored in the `supplementary/cluster_data` directory of the repository.

The **'gathering cutoff' (GC)** bitscore was calculated by quering the pHMM against the training set of proteins used to construct the model.
```bash
hmmsearch \
	-o supplementary/cluster_data/ec_hmm_search_gc_results \
	-A supplementary/cluster_data/ec_hmm_search_gc_alignment \
	--tblout supplementary/cluster_data/ec_hmm_search_gc_tab \
	supplementary/cluster_data/ec_cluster_phmm \
	data/cluster_data/all_clusters.fasta
```
The GC was defined as the smallest valued returned from `HMMER`, which was **607.0**.  
All output files are stored in the `supplementary/cluster_data` directory of the repository.

6. [`HMMERSearch`](https://academic.oup.com/nar/article/41/12/e121/1025950?login=false) (Mistry _et al.,_ 2013) was used to query the proteins from the GH CAZy families of interest against the constructed pHMM, using default search parameters.

To repeat this analysis, run the following command in the `./supplementary/cluster_data/` directory:
```bash
hmmsearch \
	-o supplementary/cluster_data/ec_hmm_search_results \
	-A supplementary/cluster_data/ec_hmm_search_alignment \
	--tblout supplementary/cluster_data/ec_hmm_search_tab \
	-T 607.0 \
	supplementary/cluster_data/ec_cluster_phmm \
	data/cluster_data/remaining_fam_seqs.fasta
```

7. The hits from `hmmsearch` were added to the protein pool (containing proteins from the 4 clusters of interest) to generate an extended protein pool. This was done using the Python script `extract_hmmer_accessions.py`, which parsed the HMMER output using the `BioPython.SearchIO` module, and which wrote out all protein sequences in the extended protein pool to the fasta file `expanded_protein_pool.fasta`. This FASTA file contained **150** protein sequences (59 protein sequences in addition to the 91 protein sequences in the clusters of interest).

The new protein pool was stored in the FASTA file [`expanded_protein_pool.fasta`]().

8. The Python script `run_blastp.py` from `pyrewton` was run from the root of the repository to run a all-vs-all BLASTP of all proteins in the expanded protein sequence pool to measure the degree of sequence diversity across the sequence pool. The results were written to [`supplementary/cluster_data/expanded_protein_pool_blastp.tsv`]().

9. The R note [`cluster_analysis.Rmd`]() was used to parse, analyse and present the results of the all-vs-all BLASTP analysis.

10. `MAFFT` was then used to align the new protein pool of 99 proteins. The resulting MSA in fasta and clustal format are located in the [supplementary]().
```bash
# FASTA output
mafft --thread 12 data/cluster_data/expanded_protein_pool.fasta > data/cluster_data/expanded_protein_pool_aligned.fasta
```

11. [`Trimal`](http://trimal.cgenomics.org/trimal)  was used to trim the MSA, by removing all columns with gaps in more than 20% of the sequences:

```bash
# run from the root of the repository
trimal -in data/cluster_data/expanded_protein_pool_aligned.fasta -out data/cluster_data/trimed_expanded_protein_pool_aligned.fasta -gt 0.8
```

The two MSA were then used for molecular modeling:
1. [MSA of protein sequences from the 4 largest clusters of proteins annotated with the EC number 3.2.1.37]()
2. [MSA of the expanded protein pool]()

## Exploration of a GH3-CE complex

Exploration of the local CAZyme database revealed the frequent co-occurence of a GH3 and CE4 and/or CE7 protein in the same _Thermotoga_ genomes. 
This mirrored the proposal of possible GH3-CE4 and/or GH3-CE7 complexes in the literature. To explore the probability of a GH3 and CE4 and/or CE7 complexes in 
_Thermotoga_ genomes, the CAZomes (all CAZymes incoded in a genome) of _Thermotoga_ genomes were annotated. The flanking genes of each GH3 protein in the 
_Thermotoga_ genomes were then identified using FlaGs (Saha _et al_., 2021).

> Saha, C. K, Pires, R. S., Brolin, H., Delannoy, M., Atkinson, G. C. (2021) 'FlaGs and webFlaGs: discovering novel biology through the analysis of gene neighbourhood conservation', Bioinformatics, 37(9), pp. 1312–1314

`FlaGs` requires a phylogenetic tree. No recent phylogenetic tree of _Thermotoga_ genomes was available, therefore, the phylogenetic tree was reconstructed using non-redundant genomes from NCBI.

### Reconstructing the _Thermotoga_ genus phylogenetic tree

To reconstruct the phylogenetic tree of _Thermotoga_ genus the method presented in [Hugouvieux-Cotte-Pattat _et al_., 2021](https://pure.strath.ac.uk/ws/portalfiles/portal/124038859/Hugouvieux_Cotte_Pattat_etal_IJSEM_2021_Proposal_for_the_creation_of_a_new_genus_Musicola_gen_nov_reclassification_of_Dickeya_paradisiaca.pdf) was used. The specific methodolgy is found in the [Hugouvieux-Cotte-Pattat _et al_. supplementary](https://widdowquinn.github.io/SI_Hugouvieux-Cotte-Pattat_2021/).

#### 1. Download genomes

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
  data/ref_genomes_of_interest_acc.txt \
  ml_tree_genomes \
  fasta
```
The arguments provided are:
1. Path to the file containing a list of the genomes of interest
2. Path to the output directory
3. The file format to download the genomes as

25 genomes were downloaded and stored in the directory `ml_tree_genomes`. The accession numbers of the downloaded genomes are listed in `data/downloaded_genome_acc.txt`

The 25 genomes were downloaded in GenBank Flat File and FASTA format. The latter was used for reconstruction of the phylogenetic tree, the former were used for annotating the CAZome.

#### 2. CDS prediction

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


#### 3. Identifying Single-Copy Orthologues (SCOs)

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


#### 4. Multiple Sequence Alignment

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


#### 5. Collect Single-Copy Orthologues CDS sequences

The CDS sequences corresponding to each set of single-copy orthologues are identified and extracted with the Python script `extract_cds.py`. To reproduce this analysis, ensure the `PROTDIR` constant in the script is 
directed to the correct output directory for orthofinder. The script can then be run from the current directory with:

```bash
python3 scripts/reconstruct_tree/ml_tree/extract_cds.py
```

The output is a set of unaligned CDS sequences corresponding to each single-copy orthologue, which are 
placed in the `sco_cds` directory


#### 6. Back-translate Aligned Single-Copy Orthologues

The single-copy orthologue CDS sequences are threaded onto the corresponding aligned protein sequences using [`t-coffee`](http://www.tcoffee.org/Projects/tcoffee/).

> T-Coffee: A novel method for multiple sequence alignments. Notredame, Higgins, Heringa, JMB, 302(205-217)2000

The results can be reproduced by executing the `backtranslate.sh` script from this directory.

```bash
scripts/reconstruct_tree/ml_tree/backtranslate.sh \
  sco_proteins_aligned \
  sco_cds_aligned
```

The backtranslated CDS sequences are placed in the `sco_cds_aligned` directory.


#### 7. Concatenating CDS into a Multigene Alignment

The threaded single-copy orthologue CDS sequences are concatenated into a single sequence per input organism using the Python script `concatenate_cds.py`. To reproduce this, execute the script from this directory with:

```bash
python scripts/reconstruct_tree/concatenate_cds.py
```

Two files are generated, a FASTA file with the concatenated multigene sequences, and a partition file allowing a different set of model parameters to be fit to each gene in phylogenetic reconstruction.


#### 8. Phylogenetic reconstruction

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








### Annotate the CAZomes

`cazy_webscraper` and `dbCAN` were used to annotate all CAZymes in the _Thermotoga_ genomes (the CAZomes).

#### 1. Download genomes

The proteins from the _Thermotoga_ genomes were required, therefore, the genomes of interested were downloaded in 
GenBank Flat File format.

To reproduce this download run the following command from the root of this repository:
```bash
scripts/ncbi/download_genomes.sh \
  data/ref_genomes_of_interest_acc.txt \
  cazomes/cazome_genomes \
  genbank
```

25 genomes were downloaded and stored in the `cazome_genomes` directory, and were decompressed by the `download_genomes.sh` script.

#### 2. Extract proteins

The Python script `extract_proteins.py` was used to extract the protein sequences from each downloaded genome, and write the protein 
sequences to FASTA files. One FASTA file was created by per downloaded genome, and contained all protein sequences extracted from the 
respective genome.

The script takes the following args:
1. Path to input dir containing genomes (in `.gbff` format)
2. Path to output dir to write out FASTA files

To reproduce the analysis, run the following command from the root of the repository:
```bash
python3 scripts/cazome_annotation/extract_proteins.py \
  cazomes/cazome_genomes \
  cazomes/extracted_proteins
```

The FASTA files were written to the `cazomes/extracted_proteins` directory.

In total 34,671 proteins were extracted.

#### 3. Identify proteins in CAZy

All proteins extracted from the downloaded genomes were queried against a local CAZyme database using the `get_cazy_cazymes.py` script. 

The script has 3 positiional arguments:
1. Path to directory containing FASTA files of extracted protein sequences
2. Path to the local CAZyme database
3. Path to output directory to write out FASTA files of proteins not in CAZy
4. Path to write out tab delimited list of proteins in the CAZy families of interest.

_The list of CAZy families of interest is hardcoded in to the `get_cazy_cazymes.py` script, in the constant `FAMILIES_OF_INTEREST`._ 

This script produced 3 outputs:
1. A single `csv` file containing all extrated CAZy annotations (including the genomic accession, protein accession and CAZy family annotation), in tidy data formatting (this is written to the output directory)
2. A FASTA file per parsed genome containing all protein sequences that are not included in CAZy (these are written to the output directory)
3. A single tab-delimited list with the genomic accession and protein accession of all proteins that are from the families of interest.
4. A `summary.txt` file, listing the number of proteins from CAZy, not in CAZy and from the families of interest (this is writte to the output directory)

Run the following command from the root of the repository to repeat this analysis:
```bash
python3 scripts/cazome_annotation/get_cazy_cazymes.py \
  cazomes/extracted_proteins \
  cazy_database.db \
  cazomes/non_cazy_proteins \
  cazomes/proteins_of_interest.txt
```

The `csv` file containing all proteins annotated in CAZy in the genomes is available in the [repository]().

In total 0 proteins were retrieved from CAZy.  
34,671 proteins were extracted from the genomes and were not included in CAZy.  

#### 4. Run and parse dbCAN

CAzy annotates the GenBank protein sequence releases, therefore, it is rare for CAZy to include the RefSeq protein accessions. To annotate the comprehensive CAZome of each genome, `dbCAN` was used to annotate the CAZomes.

_`dbCAN` version 2.0.11._

> Zhang, H., Yohe, T., Huang, L., Entwistle, S., Wu, P., Yang, Z., Busk, P.K., Xu, Y., Yin, Y. (2018) ‘dbCAN2: a meta server for automated carbohydrate-active enzyme annotation’, Nucleic Acids Res., 46(W1), pp. W95-W101. doi: 10.1093/nar/gky418

To run dbCAN for every set of protein sequences extracted from the genomes and not included in CAZy, run the following command in `dbcan` directory (*this is necessary because the paths encoded in `dbCAN` are hard coded, this does require copying the input data into a new directory withint the `dbcan` directory*):
```bash
python3 invoke_dbcan.py \
  non_cazy_proteins_copy \
  dbcan_output \
```

The output directory `dbcan_output` was moved to the `cazomes` directory: `cazomes/dbcan_output`.

To parse the output from dbCAN, and the proteins from the CAZy GH3 of interest to the tab delimited list, run the following command in the root of the repository:
```bash
python3 scripts/get_cazomes/get_dbcan_cazymes.py \
  cazomes/dbcan_output \
  cazomes/proteins_of_interest.txt \
  -f -n
```
The first argument is the path to the directory containing output from `dbCAN`. The second argument is a path to the tab delimited lists of genomic accessions and protein accession, listing proteins from GH3.

`dbCAN` parsed 34,671 proteins.  
1,663 of these proteinse were predicted to be CAZymes with a consensus CAZy family prediction (i.e. a CAZy family annotation that at least two of three tools in dbCAN agreed upon).
- 78 proteins from GH3
- 23 proteins from CE7

To facilitate reproduction of this analysis, the raw output `overview.txt` files from dbCAN for each _Thermotoga_ genome are available in the `data/dbcan_output` directory of this repository.

### Run `FlaGs`

To repeat the analysis using [`FlaGs`](), install `FlaGs` in a dir called `FlaGs` (located in the root of the repository) and run the following from the root of this repository:
```bash
mkdir cazomes/flags_output  # create output directory

python3 FlaGs/FlaGs.py \
  -a cazomes/proteins_of_interest.txt \
  -o cazomes_flags_output/thermotoga_gh3_flags_ \
  -u <email_address>
```

### GH3 flanking genes

NitroPro was used to recolour the output from `FlaGs` and annotate a substree of the _Thermotoga_ phylogenetic tree shown in figure 1.

<figure>
<img src="https://images.unsplash.com/photo-1549740425-5e9ed4d8cd34?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxjb2xsZWN0aW9uLXBhZ2V8MXwzOTU0NTB8fGVufDB8fHw%3D&w=1000&q=80" alt="Thermotoga phylogenetic tree and the presence of a GH3-CE7 gene cluster" style="width:100%">
<figcaption align = "center"><b>Fig.1 - Rooted phylogenetic tree of Thermotoga, annotated with the presence of a GH3 gene cluster. Flanking genes are numbers and coloured to indicate the protein pool they were clustered into by FlaGs. The GH3 genes are shown in black. Genes highlighted in purple (cluster 7) and genes shown in pink (cluster 3) encode ATP-binding cassette (ABC) transporter permeases. The parent genes of ABC transporter ATP-binding proteins (cluster 1) and iron ABC transporter permeases (cluster 11) are shown in green. Genes in light green (cluster 12) encode cobalamin-binding proteins. Genes shown in blue (cluster 5) produce a cephalosporin-C deacetylase from CAZy family CE7. Genes shown in white had significant sequence diversity to all other GH3 flanking genes and were clustered individually.</b></figcaption>
</figure>

- GH3 protein was highly conserved across _Thermotoga martima_, the genomes shared the same protein reference sequence ID
- The protein was flanked by (traversing upstream to downstream, and the values in brackets are the RefSeq protein IDs for the proteins in the T. martima_ genomes):
  - ABC transporter permease (WP_004082581.1)
  - ABC transporter permease (WP_004082583.1)
  - ABC transporter ATP-binding protein (WP_041426669.1)
  - ABC transporter ATP-binding protein (WP_004082591.1)
  - GH3 (WP_004082594.1)
  - cephalosporin-C deacetylase from CAZy family CE7 (WP_004082599.1)
  - ABC transporter ATP-binding protein (WP_004082601.1)
  - iron ABC transporter permease (WP_004082603.1)
  - cobalamin-binding protein (WP_004082604.1)

ABC transporter ATP-binding protein (WP_004082591.1), cephalosporin-C deacetylase from CAZy family CE7 (WP_004082599.1) and ABC transporter ATP-binding protein (WP_004082601.1) were queried against the NR database to explore the possibility of sequence similarity to proteins from archae. The results of which are stored in the `results` directory of this repository.

Only proteins from _Thermotoga_ and _Pseudothermotoga_ species shared greater than 70% sequence identity with the query proteins. Except CE7 (WP_004082599.1), which returned 2 fits of 71% identity against _Firmicutes bacterium_ and one hit against a generic bacterium. The highest sequence identity achieved between WP_004082601.1 and a bacterial protein was 41%.

Tmgh3 was flanked upstream by (in order) two ABC transporter permeases and two ABC transporter ATP-binding protein, and downstream by a cephalosporin-C deacetylase from CAZy family CE7, an ABC transporter ATP-binding protein, an iron ABC transporter permease and a cobalamin-binding protein. This gene cluster including distances between, and lengths of the genes (allowing for small variations of a few nucleotides) was conserved across the Thermotoga genomes.

To estimate the degree of conservation across the GH3-CE7 gene cluster, BLASTP all-versus-all analysis was performed for the retrieved GH3 proteins and CE7 proteins (GH3 vs GH3 and CE7 vs CE7 analyses were performed).

The GH3 and CE7 protein sequences were retrieved from the NCBI Protein database using [Batch Entrez](https://www.ncbi.nlm.nih.gov/sites/batchentrez). The resulting fasta files for [GH3]() and [CE7]() protein sequences are available in the `data/gh3_complex` directory.

To reproduce the BLASTP all-versus-all analyses, call the following commands in the root of this repository.
```bash
python3 scripts/gh3_complex/run_blastp_gh3.py
python3 scripts/gh3_complex/run_blastp_ce7.py
```
The outputs from BLASTP are written to the `results` directory for the [GH3]() and [CE7]() proteins.

The two data files of GH3 and CE7 protein accessions used in this analysis are located in the `data/gh3_complex` directory.

The R script `scripts/gh3_complex/get_heatmaps.R` was used to generate heatmaps plotting the percentage identity of the BLASTP all-versus-all 
analysis of the GH3 and CE7 proteins, to explore the degree of conservation over the potential complex.



<figure>
<img src="https://images.unsplash.com/photo-1549740425-5e9ed4d8cd34?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxjb2xsZWN0aW9uLXBhZ2V8MXwzOTU0NTB8fGVufDB8fHw%3D&w=1000&q=80" alt="Percentage identity between CE7 proteins" style="width:100%">
<figcaption align = "center"><b>Fig.3 - Percentage identity between CE7 proteins</b></figcaption>
</figure>
