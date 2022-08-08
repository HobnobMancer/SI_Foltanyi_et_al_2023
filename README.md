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
- `seqkit` == v2.2.0
- `MAFFT` >= v7.505
- `cazy_webscraper` >= 2.0.0
- `Cazomevolve`
- `get-ncbi-genomes`
- `dbCAN` >= [3.0.2](https://github.com/linnabrown/run_dbcan)

**Note on install dbCAN:** Paths are hardcoded in `dbCAN`, therefore, to use `dbCAN` in this analysis, follow 
the exact instructions provided in the `dbCAN` [README]((https://github.com/linnabrown/run_dbcan)) and run the commands in the `scripts/cazome_annotation` directory.

### Python packages
- tqdm

### R packages
- ape
- dplyr

## Data, results and scripts

- All **scripts** used in this analysis are stored in the `scripts` directory in the repo.  
- **Input data** for the analysis, such as FASTA files, are stored in the `data` directory.  
- **Results** data from this analysis, such as R markdown notebooks and MSA files, are stored in the `results` directory.

The protein sequence of _tmgh3_ is stored in [`data/tmgh3_exploration/tmgh3.fasta`](https://hobnobmancer.github.io/Foltanyi_et_al_2022/data/tmgh3_exploration.zip). All analyses were performed in March 2022.

## Method to reconstruct the analysis

To reconstruct the analysis run all commands from this directory.

The method is split into three sections:
1. [Construct a local CAZyme database](#construct-a-local-cazyme-database)


2. [Systematic exploration of tmgh3](#systematic-exploration-of-tmgh3)
  2.1 [Query tmgh against the NR database](#query_tmgh_against_the_nr_database)
  2.2 [Query tmgh against the CAZy database](#query_tmgh_against_the_cazy_database)
  2.3 [Compare NR and CAZy hits](#compare-nr-and-cazy-hits)
  2.4 [Generation of a MSA of xylosdiases](#generation-of-a-MSA-of-xylosidases)
  2.5 [HHpred](#HHpred)


3. [Interrogation of the CAZy database](#interrogation-of-the-cazy-database)


4. [Exploration of a GH3-CE complex](#exploration-of-a-gh3-ce-complex)
  - [Reconstructing the _Thermotoga_ genus phylogenetic tree](#reconstructing-the-thermotoga-genus-phylogenetic-tree)
  - [Annotate the CAZomes](#annotate-the-cazomes)
  - [GH3 flanking genes](#gh3-flanking-genes)

Below is presented a summary of the methods.

Individually pages are presented for each section of the analysis which include additional details, as well as commands used to faciltiate navigate the method. The hyperlinks are listed immediately below and in each summary section:
1. [Construct a local CAZyme database](https://hobnobmancer.github.io/Foltanyi_et_al_2022/supplementary/methods/construct_a_local_cazyme_database)
2. [Systematic exploration of tmgh3](https://hobnobmancer.github.io/Foltanyi_et_al_2022/supplementary/methods/systematic_exploration_of_tmgh3)
3. [Interrogation of the CAZy database](https://hobnobmancer.github.io/Foltanyi_et_al_2022/sql_queries/)
4. [Exploration of a GH3-CE complex](https://hobnobmancer.github.io/Foltanyi_et_al_2022/supplementary/methods/exploration_of_a_gh3_ce_complex)

## 1. Construct a local CAZyme database

`cazy_webscraper` [Hobbs et al., 2021] (DOI:) was used to construct a local CAZyme database, to facilitate the thorough interrogation of the CAZy dataset.

> Hobbs, Emma E. M.; Pritchard, Leighton; Chapman, Sean; Gloster, Tracey M. (2021): cazy_webscraper Microbiology Society Annual Conference 2021 poster. figshare. Poster. https://doi.org/10.6084/m9.figshare.14370860.v7

Data from UniProt was retrieved for proteins in the local CAZyme database, and added to the datbase. The following data was retrieved:
- UniProt accession
- Protein name
- PDB accessions
- EC numbers

The retreival of data was limited to proteins from the following GH families of interest: 1, 2, 3, 11, 26, 30, 43, 50, 51, 52, 54, 116, 120.

These data were downloaded in Feburary 2022. To faciltiate reproducing the analyses presenter here using this data set, a 
copy of this database is available in the [`data`]() directory of this repository.

## 2. Systematic exploration of tmgh3

### A. Query _tmgh3_ against the NR database

_Tmgh3_ was queryies against the [non-redundant database](https://www.ncbi.nlm.nih.gov/refseq/about/nonredundantproteins/#related-documentation) using BLASTP (via the NCBI BLASTP webinterface, using default parameters).

> Altschul, S. F., Gish, W., Miller, W., Myers, E. W., Lipman, D. J. (1990) 'Basic local alignment search tool', Journal of Molecular Biology, 215(3), pp. 403-10

The reults of the query against the NR database were stored in [`results/tmgh3_nr_query_desc_table.csv`](https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/tmgh3_nr_query_desc_table.csv).

### B. Query _tmgh3_ against CAZy db

The CAZy website does not support querying the database using BLASTP. Therefore, `cazy_webscraper` was used to facilitate a BLASTP comparison of the protein sequence of _tmgh3_ against the CAZy database. Specifically, `cazy_webscraper` was used to extract the GenBank protein sequences for all proteins in GH CAZy families of interest from the local CAZyme database and write them to a FASTA file.

The Python script `run_blastp_cazy.py` was used to query _tmgh3_ against the proteins from the GH protein sequences from CAZy GH families of interest using BLASTP.

The results were written to [`results/cazy_blastp_results.tsv`](https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/cazy_blastp_results.tsv).

### C. Compare NR and CAZy hits

Both the BLASTP query against the NR and CAZy databases returned 19 proteins from _Thermotoga_ with percentage identities of equal to or greater than 70% against _tmgh3_. To determine if the 19 hits from the BLASTP NR query (step A) were the non-redundanrt protein sequence representatives of the 19 hits from the BLASTP CAZy query (step B), the Python script `run_blastp_nr_cazy.py` was used to perform a BLASTP analysis of the 19 hits from NR query (step A) against the 19 hits from querying CAZy (step B).

The resulting `tsv` file was written to [`results/nr_cazy_blastp_results.tsv`](https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/nr_cazy_blastp_results.tsv).

The protein sequences for the 15 of the 19 from NR shared 100% sequence identity with at least one protein from CAZy, the remaining proteins shared greater than 90% sequence identity with at least one protein from CAZy.

### D. Generation of a MSA of xylosdiases

Previously _tmgh3_ had been queried against HHpred to find potential templates for molecular modelling. To explore the potential cause for HHpred returning many non-functionally relevant proteins and few xylosidases, the analysis using HHpred was repeated using an MSA of xylosdiase protein sequences.

The 19 hits from quering the NR database and the 19 hits from querying the CAZy database, which had greater than or equal to 70% sequence identity with _tmgh3_ were combined into a single fasta file. This is located at [`data/tmgh3_exploration/nr_and_cazy_hits.fasta`]().

Redundant protein sequences were removed from the NR-CAZy hit pool using [`seqkit`](https://bioinf.shenwei.me/seqkit/) (v2.2.0).

`MAFFT` [Katoh et al., 2002] (v7.505) was used to align the protein sequences, and generate the MSA.

> Katoh K, Misawa K, Kuma K, Miyata T. MAFFT: a novel method for rapid multiple sequence alignment based on fast Fourier transform. Nucleic Acids Res. 2002 Jul 15;30(14):3059-66. doi: 10.1093/nar/gkf436. PMID: 12136088; PMCID: PMC135756.

### E. Repeating the analysis using HHpred

HHpred was run using the default parameters (via the [HHpred webserver](https://toolkit.tuebingen.mpg.de/tools/hhpred)) and the MSA stored in `data/tmgh3_exploration/nr_and_cazy_hits_aligned.fasta`. 

> Söding J, Biegert A, Lupas AN. The HHpred interactive server for protein homology detection and structure prediction. Nucleic Acids Res. 2005 Jul 1;33(Web Server issue):W244-8. doi: 10.1093/nar/gki408. PMID: 15980461; PMCID: PMC1160169.

The results are stored in [`results/hhpred_results.hhr`](https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/hhpred_results.hhr).

Using the MSA did not signficantly increase the number of functionally relevant hits returned by HHpred. In general, the results between the two queries were similar. This potentially reflects the limited knowledge pool for _Thermotoga_ glycoside hydrolase GH3 proteins.

## 3.Interrogation of the CAZy database

A series of SQL commands were peformed to interrogoate the local CAZyme database. The commands are presented [here](https://hobnobmancer.github.io/Foltanyi_et_al_2022/sql_queries/), and all results are stored in the repository in the [`sql_queries/` dir](https://github.com/HobnobMancer/Foltanyi_et_al_2022/tree/master/sql_queries).

## 4. Exploration of a GH3-CE7 complex

More detailed explanation of the method for identifying the novel GH3-CE7 complex, and all commands used is presented [here](https://hobnobmancer.github.io/Foltanyi_et_al_2022/supplementary/methods/exploration_of_a_gh3_ce_complex)

Exploration of the local CAZyme database revealed the frequent co-occurence of a GH3 and CE4 and/or CE7 protein in the same _Thermotoga_ genomes. 
This mirrored the proposal of possible GH3-CE4 and/or GH3-CE7 complexes in the literature. To explore the probability of a GH3 and CE4 and/or CE7 complexes in _Thermotoga_ genomes, the CAZomes (all CAZymes incoded in a genome) of _Thermotoga_ genomes were annotated. The flanking genes of each GH3 protein in the _Thermotoga_ genomes were then identified using FlaGs (Saha _et al_., 2021).

> Saha, C. K, Pires, R. S., Brolin, H., Delannoy, M., Atkinson, G. C. (2021) 'FlaGs and webFlaGs: discovering novel biology through the analysis of gene neighbourhood conservation', Bioinformatics, 37(9), pp. 1312–1314

`FlaGs` requires a phylogenetic tree. No recent phylogenetic tree of _Thermotoga_ genomes was available, therefore, the phylogenetic tree was reconstructed using non-redundant genomes from NCBI.

### Reconstructing the _Thermotoga_ genus phylogenetic tree

To reconstruct the phylogenetic tree of _Thermotoga_ genus the method presented in [Hugouvieux-Cotte-Pattat _et al_., 2021](https://pure.strath.ac.uk/ws/portalfiles/portal/124038859/Hugouvieux_Cotte_Pattat_etal_IJSEM_2021_Proposal_for_the_creation_of_a_new_genus_Musicola_gen_nov_reclassification_of_Dickeya_paradisiaca.pdf) was used. The specific methodolgy is found in the [Hugouvieux-Cotte-Pattat _et al_. supplementary](https://widdowquinn.github.io/SI_Hugouvieux-Cotte-Pattat_2021/).

#### A. Download genomes

RefSeq genomic assemblies were retrieved from NCBI using [`ncbi-genome-download`](https://github.com/kblin/ncbi-genome-download/).

The genomic accessions of the genomic assemblies used to 
reconstruct the phylogenetic tree are listed in `data/ref_genomes_of_interest_acc.txt`. This includes the 
RefSef genome of **_Fervidobacterium changbaicum_ CBS-1 GCF_004117075.1 as an out group**, to facilitate 
identifying the root of the _Thermotoga_ tree.

The 25 genomes were downloaded in GenBank Flat File and FASTA format. The latter was used for reconstruction of the phylogenetic tree, the former were used for annotating the CAZome.

#### B. CDS prediction

To ensure consistency of nomenclature and support back threading the nucleotides sequences onto 
aligned single-copy orthologues, all downloaded RefSeq genomes were reannotated using 
[`prodigal`](https://github.com/hyattpd/Prodigal)

> Hyatt D, Chen GL, Locascio PF, Land ML, Larimer FW, Hauser LJ. Prodigal: prokaryotic gene recognition and translation initiation site identification. BMC Bioinformatics. 2010 Mar 8;11:119. doi: 10.1186/1471-2105-11-119. PMID: 20211023; PMCID: PMC2848648.

#### C. Identifying Single-Copy Orthologues (SCOs)

Orthologues present in the RefSeq _Thermotoga_ genomes were identified using [`orthofinder`](https://github.com/davidemms/OrthoFinder)

> Emms, D.M. and Kelly, S. (2019) OrthoFinder: phylogenetic orthology inference for comparative genomics. [Genome Biology 20:238](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-019-1832-y)

The output from `orthofinder` was written to the `orthologues/Results_Nov11/Single_Copy_Orthologue_Sequences` directory.

`orthofinder` assigned 46086 genes (98.6% of total) to 2662 orthogroups. Fifty percent of all genes were in orthogroups with 25 or more genes (G50 was 25) and were contained in the largest 889 orthogroups (O50 was 889). There were 990 orthogroups with all species present and 828 of these consisted entirely of single-copy genes.

`orthofinder` identified genome GCF_004117075.1 as the best out group.


#### D. Multiple Sequence Alignment

Each collection of single-copy orthologous was aligned using [`MAFFT`](https://mafft.cbrc.jp/alignment/software/).

The output from `MAFFT` (the aligned files) are placed in the `sco_proteins_aligned` directory.


#### E. Collect Single-Copy Orthologues CDS sequences

The CDS sequences corresponding to each set of single-copy orthologues are identified and extracted with the Python script `extract_cds.py`. To reproduce this analysis, ensure the `PROTDIR` constant in the script is 
directed to the correct output directory for orthofinder. The script can then be run from the current directory with:

```bash
python3 scripts/reconstruct_tree/extract_cds.py
```

The output is a set of unaligned CDS sequences corresponding to each single-copy orthologue, which are 
placed in the `sco_cds` directory


#### F. Back-translate Aligned Single-Copy Orthologues

The single-copy orthologue CDS sequences are threaded onto the corresponding aligned protein sequences using [`t-coffee`](http://www.tcoffee.org/Projects/tcoffee/).

> T-Coffee: A novel method for multiple sequence alignments. Notredame, Higgins, Heringa, JMB, 302(205-217)2000

The results can be reproduced by executing the `backtranslate.sh` script from this directory.

```bash
scripts/reconstruct_tree/backtranslate.sh \
  sco_proteins_aligned \
  sco_cds_aligned
```

The backtranslated CDS sequences are placed in the `sco_cds_aligned` directory.


#### G. Concatenating CDS into a Multigene Alignment

The threaded single-copy orthologue CDS sequences are concatenated into a single sequence per input organism using the Python script `concatenate_cds.py`. To reproduce this, execute the script from this directory with:

```bash
python scripts/reconstruct_tree/concatenate_cds.py
```

Two files are generated, a FASTA file with the concatenated multigene sequences, and a partition file allowing a different set of model parameters to be fit to each gene in phylogenetic reconstruction.


#### H. Phylogenetic reconstruction

To reconstruct the phylogenetic tree, the bash script `raxml_ng_build_tree.sh` is used, and is 
run from the root of this repository. This executes a series of [`raxml-ng`](https://github.com/amkozlov/raxml-ng) commands.

All genes were considered as separate partitions in the reconstuction, 
with parameters estimated  for the `GTR+FO+G4m+B` model (as recommended by `raxml-ng check`).

Tree reconstructions are placed in the `tree` directory. The best estimate tree is `03_infer.raxml.bestTree` and the midpoint-rooted, manually-annotated/coloured tree (using [`figtree`](http://tree.bio.ed.ac.uk/software/figtree/)) is `03_infer.raxml.bestTree.annotated`

> Alexey M. Kozlov, Diego Darriba, Tomáš Flouri, Benoit Morel, and Alexandros Stamatakis (2019) RAxML-NG: A fast, scalable, and user-friendly tool for maximum likelihood phylogenetic inference. Bioinformatics, btz305 [doi:10.1093/bioinformatics/btz305](https://doi.org/10.1093/bioinformatics/btz305)

The resulting tree in the [original format](https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/2022_annotated_thermotoga_tree.pdf) and after [rerooting using the outgroup](https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/2022_annotated_thermotoga_tree.rerooted.pdf) are stored in the `results` directory.


### Annotate the CAZomes

`cazy_webscraper` and `dbCAN` were used to annotate all CAZymes in the _Thermotoga_ genomes (the CAZomes).

#### 1. Extract proteins

The Python script `extract_proteins.py` was used to extract the protein sequences from each downloaded genome, and write the protein 
sequences to FASTA files. One FASTA file was created by per downloaded genome, and contained all protein sequences extracted from the 
respective genome.

The FASTA files were written to the `cazomes/extracted_proteins` directory.

In total 34,671 proteins were extracted.

#### 2. Identify proteins in CAZy

All proteins extracted from the downloaded genomes were queried against a local CAZyme database using the `get_cazy_cazymes.py` script. 

_The list of CAZy families of interest is hardcoded in to the `get_cazy_cazymes.py` script, in the constant `FAMILIES_OF_INTEREST`._ 

In total 0 proteins were found to be annotated by CAZy.  

#### 3. Run and parse dbCAN

CAZy annotates the GenBank protein sequence releases, therefore, it is rare for CAZy to include the RefSeq protein accessions. To annotate the comprehensive CAZome of each genome, `dbCAN` was used to annotate the CAZomes.

_`dbCAN` version 3.0.2_

> Zhang, H., Yohe, T., Huang, L., Entwistle, S., Wu, P., Yang, Z., Busk, P.K., Xu, Y., Yin, Y. (2018) ‘dbCAN2: a meta server for automated carbohydrate-active enzyme annotation’, Nucleic Acids Res., 46(W1), pp. W95-W101. doi: 10.1093/nar/gky418

The output directory `dbcan_output` was moved to the `cazomes` directory: `cazomes/dbcan_output`.

`dbCAN` parsed 34,671 proteins.  
1,663 of these proteinse were predicted to be CAZymes with a consensus CAZy family prediction (i.e. a CAZy family annotation that at least two of three tools in dbCAN agreed upon).
- 78 proteins from GH3
- 23 proteins from CE7

To facilitate reproduction of this analysis, the raw output `overview.txt` files from dbCAN for each _Thermotoga_ genome are available in the [`data/dbcan_output`](https://github.com/HobnobMancer/Foltanyi_et_al_2022/tree/master/data/dbcan_output) directory of this repository.

### GH3 flanking genes

#### 1. Run `FlaGs`

The flanking genes of each GH3 protein were identified using the Pythn tool [`FlaGs`](http://www.webflags.se/), using the list of GH3 protein accessions generated in the last step.

> Chayan Kumar Saha, Rodrigo Sanches Pires, Harald Brolin, Maxence Delannoy, Gemma Catherine Atkinson, FlaGs and webFlaGs: discovering novel biology through the analysis of gene neighbourhood conservation, Bioinformatics, Volume 37, Issue 9, 1 May 2021, Pages 1312–1314, https://doi.org/10.1093/bioinformatics/btaa788

#### 2. Generate figures

NitroPro was used to recolour the output from `FlaGs` and annotate a substree of the _Thermotoga_ phylogenetic tree shown in figure 1.

<figure>
<img src="https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/annotated_thermotoga_tree.rerooted.truncated.svg" alt="Thermotoga phylogenetic tree and the presence of a GH3-CE7 gene cluster" style="width:100%">
<figcaption align = "center"><b>Fig.1 - Rooted phylogenetic tree of Thermotoga, annotated with the presence of a GH3 gene cluster</b></figcaption>
</figure>

#### 3. Addressing proteins that were not clustered

##### _Thermotoga_ sp. 2812B (GCF_000789335.1)

To determine if the unclustered protein from _Thermotoga_ sp. 2812B (GCF_000789335.1) was a CE7 protein, `cazy_webscraper` was used to retrieve the protein sequences from GenBank for all proteins in CE7. 

The protein sequences were written to the local CAZyme database, and extracted to a FASTA file using `cazy_webscraper`.

In total, 2,664 protein sequences were retrieved from NCBI and written to the fasta a file [`cazy_ce7_proteins.fasta`]().

The nucleotide sequence of the gene that encoded the putative CE7 protein (named by FlaGs as pseudogene_69.1) was mannualy retrieved from genome (GCF_000789335.1). Both the forward and reverse strand sequences were retrieved, and written to a single fasta file located at [`data/g3_complex/unclustered_ce7_nt.fasta`]().
- Gene: axeA
- Locus tag: T2812B_RS04530
- Product: Cephalosporin-C deacetylase
- location: complement(901723..902701)

The nucleotide sequence was translated to a protein sequence (specifically the reverse strand was translated), and the protein sequence was stored at [`data/gh3_complex/unclustered_ce7_prt.fasta`]().

The Python script `run_blastp_unclustered_ce7.py` was used to query the potential CE7 protein from _Thermotoga_ sp. 2812B against all GenBank proteins in the CAZy family CE7. To allow for greater sequence diversity between proteins with a similar structure the BLOSUM45 matrix was used.

The output was written to [`results/blastpUnclusteredCe7.tsv]().

12 hits were returned with a percentage identitiy of greater than or equal to 90%, all of which had a percentage coverage of greater than or equal to 98%. In order of percentage identity these proteins were:
- AIY86427.1
- AKE29758.1
- AGL49000.1
- NP_227893.1
- AKE26023.1
- AHD18153.1
- AAD35171.1
- AKE27885.1
- ACB09222.1
- ADA66802.1
- ABQ46866.1
- AIY88183.1

The protein AIY86427.1 in CE7 shared 100% percentage identity and covereage with the query unclustered CE7 protein sequence.

The local CAZyme database `cazy_database.db` was queried to return the following data for the protein AIY86427.1:
- Source organism
- CAZy family annotations
- EC number annotations
- UniProt database record ID

The source organism was returned as 'Thermotoga	sp. 2812B', with the only CAZy family annotation being CE7. No EC number annotations of UniProt ID was returned.

This query was expanded to retrieve data for the 12 proteins with greater than or equal to 90% precentage identity with the query unclustered CE7 protein.

The results are stored in [`results/unclustedCE7_cazy_query.csv`]().

All 12 proteins were from _Thermotoga_ species.

To investigate if the entire GH3-CE7 gene cluster was conserved, the protein record of the product from the gene immediately upstream of the GH3 (WP_008194121.1) encoding gene (which was labelled by FlaGs as pseudogene_69.3) and which was individually clustered, was retrieved mannually from the _Thermotoga_ sp. 2812B (GCF_000789335.1) assembly (ASM78933v1).
- Locus tag: T2812B_RS04540
- Product: ABC transporter ATP-binding protein
- Protein: WP_004082591.1
- location: complement(905080..906083)

The protein was annotated as ABC transporter ATP-binding protein.

##### _Thermotoga_ sp. TBGT1765 (GCF_000784795.1) and _Thermotoga_ sp. TBGT1766 (GCF_000784825.1)

1765
annotated as pseudogene_27.2 by flags
located at 30820	31783
retrieved from GCF_000784795.1
locus_tag="TBGT1765_RS08750"
RefSeq:WP_004082591.1
ABC transporter ATP-binding protein

1766
GCF_000784825.1 assemby ASM78482v1, assembly level of contig
located the GH3 protein WP_038033230.1 at 31821..34157, locus tag TBGT1766_RS08440
immediately up stream was WP_004082591.1, which was annotated as an ABC transporter ATP-binding protein

Therefore, the GH3-CE7 gene cluster is conserved in  _Thermotoga_ sp. TBGT1765 and _Thermtoga_ sp. TBGT1766.

##### _Thermotoga_ sp. EMB (GCF_000294555.1)

Protein WP_008194121.1
Query NCBI Protein database: nucleotide: NCBI Reference Sequence: NZ_AJII01000008.1 from _Thermotoga_ sp. EMP Contig 08 as part of the assembly ASM29455v1, with an assembly level of contig
Mannually found NZ_AJII01000008.1 in the assembly
REFSEQ INFORMATION: The reference sequence is identical to
            AJII01000008.1
located at AJII01000008.1:1..2412 in the conti
Without assembling the contigs onto a scaffold, the flanking genes cannot be identified. However, the degree of conservation, we speculate the GH3-Ce7 gene cluster is also conserved in _Thermotoga_ sp. EMB, espeically because dbCAN did predict the proteome contained 1 CE7 protein.
checked if the first and last 20 nucleotides of the contig NZ_AJII01000008.1 appeared any other contigs in the assembly (in the aim to identify the flanking contigs and therefore the flanking genes), but they did not.

##### _Thermotoga_ sp. Mc24 (GCF_000784835.1)



#### Potential GH3-CE7 complex

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

