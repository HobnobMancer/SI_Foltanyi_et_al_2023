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

The protein sequence of _tmgh3_ is stored in [`data/tmgh3_exploration/tmgh3.fasta`](https://hobnobmancer.github.io/Foltanyi_et_al_2022/data/tmgh3_exploration.zip).

### 1. Query against the NR database

As a preliminary search to identify potentially functionally similar proteins to infer functional and structural information about _tmgh3_, the 
[non-redundant database](https://www.ncbi.nlm.nih.gov/refseq/about/nonredundantproteins/#related-documentation) was queried using BLASTP.

> Altschul, S. F., Gish, W., Miller, W., Myers, E. W., Lipman, D. J. (1990) 'Basic local alignment search tool', Journal of Molecular Biology, 215(3), pp. 403-10

This was done via the NCBI BLASTP (webinterface)[https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastp&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome] using default query parameters.

The reults of the query against the NR database were stored in [`results/tmgh3_nr_query_desc_table.csv`](https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/tmgh3_nr_query_desc_table.csv).

A 70% identity cut-off was used to select proteins, which is widely accepted as a reasonably cut-off for selecting proteins that share the first 3 digits of their respective EC numbers.

The protein sequences of the 19 hits with sequence identity of equal to or greater than 70% against _tmgh3_ were written to the FASTA file `data/tmgh3_exploration/nr_hits.fasta`.

### 2. Query against CAZy

CAZy annotates GenBank database releases. Reference sequence protein IDs are not catalogued in CAZy. Therefore, the _tmgh3_ prortein sequence was queried against the CAZy database to find potentially functionally similar proteins to infer functional and structural information about _tmgh3_.

The CAZy website does not support querying the database using BLASTP. Therefore, `cazy_webscraper` was used to extract the GenBank protein sequences for all GH CAZy families of interest from the local CAZyme database and write them to a FASTA file.
```bash
cw_extract_protein_sequences \
  cazy_database.db genbank \
  --families GH1,GH2,GH3,GH11,GH26,GH30,GH43,GH51,GH52,GH54,GH116,GH120 \
  --fasta_file data/tmgh3_exploration/cazy_proteins_seqs.fasta \
  -f -n
```

The Python script `run_blastp_cazy.py` was used to query _tmgh3_ against the proteins from the CAZy families of interest using BLASTP. To repeat this analysis, run the following command from the root of the repository.
```bash
python3 scripts/tmgh3_exploration/run_blastp_cazy.py
```

The results were written to [`results/cazy_blastp_results.tsv`](https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/cazy_blastp_results.tsv).

The protein sequences of the 19 hits with sequence identity of equal to or greater than 70% against _tmgh3_ were written to the FASTA file `data/tmgh3_exploration/cazy_hits.fasta`.

### 3. Exploration of NR and CAZy hits

Both the BLASTP query against the NR and CAZy databases returned 19 proteins from _Thermotoga_ with percentage identities of equal to or greater than 70% against _tmgh3_. 

CAZy annotates GenBank database releases. Reference sequence protein IDs are not catalogued in CAZy. To determine if the hits from NR were reference sequences of proteins in CAZy, the Python script `run_blastp_nr_cazy.py` was used to perform a BLASTP analysis of the 19 hits from NR against the 19 hits from querying CAZy. To repeat this analysis, run the following command from the root of the repository.
```bash
python3 scripts/tmgh3_exploration/run_blastp_nr_cazy.py
```

The resulting `tsv` file was written to [`results/nr_cazy_blastp_results.tsv`](https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/nr_cazy_blastp_results.tsv).

The protein sequences for the 15 of the 19 from NR shared 100% sequence identity with at least one protein from CAZy, the remaining proteins shared greater than 90% sequence identity with at least one protein from CAZy.

### 4. Generation of a MSA of xylosdiases

Previously _tmgh3_ had been queried against HHpred to find potential templates for molecular modelling. To explore the potential cause for HHpred returning many non-functionally relevant proteins and few xylosidases, the analysis using HHpred was repeated using an MSA of xylosdiase protein sequences.

To create the MSA the proteins sequences 19 hits from quering the NR database and the 19 hits from querying the CAZy database, which had greater than or equal to 70% sequence identity with _tmgh3_ were combined into a single fasta file. This is located at [`data/tmgh3_exploration/nr_and_cazy_hits.fasta`]().

The previous BLASTP query of the NR hits against the CAZy hits revealed several NR hits shared 100% sequence identity with hits from CAZy. Therefore, [`seqkit`](https://bioinf.shenwei.me/seqkit/) was used to remove redundant protein sequences based upon sequence.
```bash
seqkit rmdup -s data/tmgh3_exploration/nr_and_cazy_hits.fasta data/tmgh3_exploration/nr_cazy_hits_nonred.fasta
```

`MAFFT` was used to align the protein sequences. To repeat this analysis run the following command from the root of the repository.
```bash
mafft --thread 12 data/tmgh3_exploration/nr_cazy_hits_nonred.fasta > data/tmgh3_exploration/nr_and_cazy_hits_aligned.fasta
```

> Katoh K, Misawa K, Kuma K, Miyata T. MAFFT: a novel method for rapid multiple sequence alignment based on fast Fourier transform. Nucleic Acids Res. 2002 Jul 15;30(14):3059-66. doi: 10.1093/nar/gkf436. PMID: 12136088; PMCID: PMC135756.

### 4. Repeating the analysis using HHpred

HHpred was run using the default parameters (via the [HHpred webserver](https://toolkit.tuebingen.mpg.de/tools/hhpred)) and the MSA stored in `data/tmgh3_exploration/nr_and_cazy_hits_aligned.fasta`. 

> Söding J, Biegert A, Lupas AN. The HHpred interactive server for protein homology detection and structure prediction. Nucleic Acids Res. 2005 Jul 1;33(Web Server issue):W244-8. doi: 10.1093/nar/gki408. PMID: 15980461; PMCID: PMC1160169.

The results are stored in [`results/hhpred_results.hhr`](https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/hhpred_results.hhr).

Using the MSA did not signficantly increase the number of functionally relevant hits returned by HHpred. In general, the results between the two queries were similar. This potentially reflects the limited knowledge pool for _Thermotoga_ glycoside hydrolase GH3 proteins.

### 3. Interrogation of the CAZy database

So why couldn't we find anything? Let's interrogate CAZy.
SQL commands... why does our protein come up with so few hits?

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

The resulting tree in the [original format](https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/2022_annotated_thermotoga_tree.pdf) and after [rerooting using the outgroup](https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/2022_annotated_thermotoga_tree.rerooted.pdf) are stored in the `results` directory.


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

In total 0 proteins were retrieved from CAZy.  
34,671 proteins were extracted from the genomes and were not included in CAZy.  

#### 4. Run and parse dbCAN

CAzy annotates the GenBank protein sequence releases, therefore, it is rare for CAZy to include the RefSeq protein accessions. To annotate the comprehensive CAZome of each genome, `dbCAN` was used to annotate the CAZomes.

_`dbCAN` version 3.0.2_

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

To facilitate reproduction of this analysis, the raw output `overview.txt` files from dbCAN for each _Thermotoga_ genome are available in the [`data/dbcan_output`](https://github.com/HobnobMancer/Foltanyi_et_al_2022/tree/master/data/dbcan_output) directory of this repository.

### Run `FlaGs`

To repeat the analysis using [`FlaGs`](http://www.webflags.se/), install `FlaGs` in a dir called `FlaGs` (located in the root of the repository) and run the following from the root of this repository:
```bash
mkdir cazomes/flags_output  # create output directory

python3 FlaGs/FlaGs.py \
  -a cazomes/proteins_of_interest.txt \
  -o cazomes_flags_output/thermotoga_gh3_flags_ \
  -u <email_address>
```

> Chayan Kumar Saha, Rodrigo Sanches Pires, Harald Brolin, Maxence Delannoy, Gemma Catherine Atkinson, FlaGs and webFlaGs: discovering novel biology through the analysis of gene neighbourhood conservation, Bioinformatics, Volume 37, Issue 9, 1 May 2021, Pages 1312–1314, https://doi.org/10.1093/bioinformatics/btaa788

### GH3 flanking genes

NitroPro was used to recolour the output from `FlaGs` and annotate a substree of the _Thermotoga_ phylogenetic tree shown in figure 1.

<figure>
<img src="https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/annotated_thermotoga_tree.rerooted.truncated.svg" alt="Thermotoga phylogenetic tree and the presence of a GH3-CE7 gene cluster" style="width:100%">
<figcaption align = "center"><b>Fig.1 - Rooted phylogenetic tree of Thermotoga, annotated with the presence of a GH3 gene cluster</b></figcaption>
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
The outputs from BLASTP are written to the `results` directory for the [GH3](https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/blastp_gh3_complex_proteins.tsv) and [CE7](https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/blastp_ce7_complex_proteins.tsv) proteins.

The two data files of GH3 and CE7 protein accessions used in this analysis are located in the `data/gh3_complex` directory.

The R script `scripts/gh3_complex/get_heatmaps.R` was used to generate heatmaps plotting the percentage identity of the BLASTP all-versus-all 
analysis of the GH3 and CE7 proteins, to explore the degree of conservation over the potential complex.

<figure>
<img src="https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/blastpGh3ComplexProteins.svg" alt="Percentage identity between Gh3 proteins" style="width:100%">
<figcaption align = "center"><b>Fig.2 - Percentage identity between GH3 proteins</b></figcaption>
</figure>

<figure>
<img src="https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/blastpCe7ComplexProteins.svg" alt="Percentage identity between CE7 proteins" style="width:100%">
<figcaption align = "center"><b>Fig.3 - Percentage identity between CE7 proteins</b></figcaption>
</figure>

