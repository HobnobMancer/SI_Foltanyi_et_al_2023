Return to [main page](https://hobnobmancer.github.io/Foltanyi_et_al_2022/).

# Exploration of a GH3-CE7 complex

Below is the detailed method used to generate the results presented in the paper `Folyanyi _et al_., 2022` during the identification of a potentially novel GH3-CE7 complex.

The work is broken into 2 steps:
1. [Reconstruction of the phylogenetic tree](#recontruction-of-the-phylogenetic-tree)  
1.1 [Download genomes](#download-genomes)  
1.2 [CDS prediction](#cds-prediction)  
1.3 [Identifying Single-Copy Orthologues (SCOs)](#identifying-single-copy-orthologues)  
1.4 [Multiple Sequence Alignment](#multiple-sequence-alignment)  
1.5 [Collect Single-Copy Orthologues CDS sequences](#collect-single-copy-orthologoues-cds-sequences)  
1.6 [Back-translate](#back-translate)  
1.7 [Concatenate](#concatenate)  
1.8 [Phylogenetic reconstruction](#phylogenetic-reconstruction)  
2. [Annotate the CAZomes](#annotate-the-cazomes)  
2.1 [Extract proteins](#extract-proteins)  
2.2 [Identify proteins in CAZy](#identifying-proteins-in-CAZy)  
2.3 [Run and parse dbCAN](#run-and-parse-dbcan)  
3. [GH3 flanking genes](#gh3-flanking-genes)  

Exploration of the local CAZyme database revealed the frequent co-occurence of a GH3 and CE4 and/or CE7 protein in the same _Thermotoga_ genomes. 
This mirrored the proposal of possible GH3-CE4 and/or GH3-CE7 complexes in the literature. To explore the probability of a GH3 and CE4 and/or CE7 complexes in 
_Thermotoga_ genomes, the CAZomes (all CAZymes incoded in a genome) of _Thermotoga_ genomes were annotated. The flanking genes of each GH3 protein in the 
_Thermotoga_ genomes were then identified using FlaGs (Saha _et al_., 2021).

> Saha, C. K, Pires, R. S., Brolin, H., Delannoy, M., Atkinson, G. C. (2021) 'FlaGs and webFlaGs: discovering novel biology through the analysis of gene neighbourhood conservation', Bioinformatics, 37(9), pp. 1312–1314

## 1. Recontruction of the phylogenetic tree

No recent phylogenetic tree of _Thermotoga_ genomes was available (i.e. a tree representing all RefSeq genomes available in NCBI in Feburary 2022) , therefore, the phylogenetic tree was reconstructed using non-redundant genomes from NCBI.

To reconstruct the phylogenetic tree of _Thermotoga_ genus the method presented in [Hugouvieux-Cotte-Pattat _et al_., 2021](https://pure.strath.ac.uk/ws/portalfiles/portal/124038859/Hugouvieux_Cotte_Pattat_etal_IJSEM_2021_Proposal_for_the_creation_of_a_new_genus_Musicola_gen_nov_reclassification_of_Dickeya_paradisiaca.pdf) was used. The specific methodolgy is found in the [Hugouvieux-Cotte-Pattat _et al_. supplementary](https://widdowquinn.github.io/SI_Hugouvieux-Cotte-Pattat_2021/).

### A. Download genomes

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

### B. CDS prediction

In order to ensure consistency of nomenclature and support back threading the nucleotides sequences onto 
aligned single-copy orthologues, all downloaded RefSeq genomes were reannotated using 
[`prodigal`](https://github.com/hyattpd/Prodigal)

> Hyatt D, Chen GL, Locascio PF, Land ML, Larimer FW, Hauser LJ. Prodigal: prokaryotic gene recognition and translation initiation site identification. BMC Bioinformatics. 2010 Mar 8;11:119. doi: 10.1186/1471-2105-11-119. PMID: 20211023; PMCID: PMC2848648.

To reproduce the annotation of the genomes, run the `annotate_genomes_prodigal.sh` script from the root of 
this repository.
```bash
scripts/reconstruct_tree/annotate_genomes_prodigal.sh ml_tree_genomes
```
Only one argument is provided: the path to the directory containing the downloaded genomes.

The output from `prodigal` are placed in the following directories:
- The predicted CDS are placed in the `genomes/cds` directory
- The conceptural translations are placed in `genomes/proteins`
- The GenBank formate files are placed in the `genomes/gbk` directory

A log of the `prodigal` terminal output was placed in `data/logs/prodigal.log`.

### C. Identifying Single-Copy Orthologues (SCOs)

Orthologues present in the RefSeq _Thermotoga_ genomes were identified using [`orthofinder`](https://github.com/davidemms/OrthoFinder)

> Emms, D.M. and Kelly, S. (2019) OrthoFinder: phylogenetic orthology inference for comparative genomics. [Genome Biology 20:238](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-019-1832-y)

To reproduce the identifcation of orthologues, run the following command from the root of this repository:
```bash
scripts/reconstruct_tree/get_scos.sh \
  ml_tree_genomes/proteins \
  orthologues
```
To arguments are provided:
1. The path to the directory containing the FASTA files of predicted protein sequences from `prodigal`
2. A path to an output directory

The output from `orthofinder` was written to the `orthologues/Results_Nov11/Single_Copy_Orthologue_Sequences` directory.

`orthofinder` assigned 46086 genes (98.6% of total) to 2662 orthogroups. Fifty percent of all genes were in orthogroups with 25 or more genes (G50 was 25) and were contained in the largest 889 orthogroups (O50 was 889). There were 990 orthogroups with all species present and 828 of these consisted entirely of single-copy genes.

`orthofinder` identified genome GCF_004117075.1 as the best out group.

### D. Multiple Sequence Alignment

Each collection of single-copy orthologous was aligned using [`MAFFT`](https://mafft.cbrc.jp/alignment/software/).

To reproduce the MSA, run following command from the root of this repository.
```bash
scripts/reconstruct_tree/align_scos.sh \
  orthologues/Results_Nov11/Single_Copy_Orthologue_Sequences
```

The output from `MAFFT` (the aligned files) are placed in the `sco_proteins_aligned` directory.


### F. Collect Single-Copy Orthologues CDS sequences

The CDS sequences corresponding to each set of single-copy orthologues are identified and extracted with the Python script `extract_cds.py`. To reproduce this analysis, ensure the `PROTDIR` constant in the script is 
directed to the correct output directory for orthofinder. The script can then be run from the current directory with:

```bash
python3 scripts/reconstruct_tree/extract_cds.py
```

The output is a set of unaligned CDS sequences corresponding to each single-copy orthologue, which are 
placed in the `sco_cds` directory


### G. Back-tranlsate

The single-copy orthologue CDS sequences are threaded onto the corresponding aligned protein sequences using [`t-coffee`](http://www.tcoffee.org/Projects/tcoffee/).

> T-Coffee: A novel method for multiple sequence alignments. Notredame, Higgins, Heringa, JMB, 302(205-217)2000

The results can be reproduced by executing the `backtranslate.sh` script from this directory.

```bash
scripts/reconstruct_tree/backtranslate.sh \
  sco_proteins_aligned \
  sco_cds_aligned
```

The backtranslated CDS sequences are placed in the `sco_cds_aligned` directory.


### H. Concatenate

The threaded single-copy orthologue CDS sequences are concatenated into a single sequence per input organism using the Python script `concatenate_cds.py`. To reproduce this, execute the script from this directory with:

```bash
python scripts/reconstruct_tree/concatenate_cds.py
```

Two files are generated, a FASTA file with the concatenated multigene sequences, and a partition file allowing a different set of model parameters to be fit to each gene in phylogenetic reconstruction.


### I. Phylogenetic reconstruction

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

## 2. Annotate the CAZomes

`cazy_webscraper` and `dbCAN` were used to annotate all CAZymes in the _Thermotoga_ genomes (the CAZomes).

### A. Extract proteins

The Python script `extract_proteins.py` was used to extract the protein sequences from each downloaded genome, and write the protein 
sequences to FASTA files. One FASTA file was created by per downloaded genome, and contained all protein sequences extracted from the 
respective genome.

The script takes the following args:
1. Path to input dir containing genomes (in `.gbff` format)
2. Path to output dir to write out FASTA files

To reproduce the analysis, run the following command from the root of the repository:
```bash
python3 scripts/get_cazomes/extract_proteins.py \
  cazomes/cazome_genomes \
  cazomes/extracted_proteins
```

The FASTA files were written to the `cazomes/extracted_proteins` directory.

In total 34,671 proteins were extracted.

### B. Identify proteins in CAZy

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
python3 scripts/get_cazomes/get_cazy_cazymes.py \
  cazomes/extracted_proteins \
  cazy_database.db \
  cazomes/non_cazy_proteins \
  cazomes/proteins_of_interest.txt
```

In total 0 proteins were retrieved from CAZy.  
34,671 proteins were extracted from the genomes and were not included in CAZy.  

#### C. Run and parse dbCAN

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


### GH3 flanking genes

The flanking genes of each GH3 protein were identified using the Pythn tool `FlaGs`

### A. Run `FlaGs`

To repeat the analysis using [`FlaGs`](http://www.webflags.se/), install `FlaGs` in a dir called `FlaGs` (located in the root of the repository) and run the following from the root of this repository:
```bash
mkdir cazomes/flags_output  # create output directory

python3 FlaGs/FlaGs.py \
  -a cazomes/proteins_of_interest.txt \
  -o cazomes_flags_output/thermotoga_gh3_flags_ \
  -u <email_address>
```

> Chayan Kumar Saha, Rodrigo Sanches Pires, Harald Brolin, Maxence Delannoy, Gemma Catherine Atkinson, FlaGs and webFlaGs: discovering novel biology through the analysis of gene neighbourhood conservation, Bioinformatics, Volume 37, Issue 9, 1 May 2021, Pages 1312–1314, https://doi.org/10.1093/bioinformatics/btaa788

### B. Generate figures

NitroPro was used to recolour the output from `FlaGs` and annotate a substree of the _Thermotoga_ phylogenetic tree shown in figure 1.

<figure>
<img src="https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/annotated_thermotoga_tree.rerooted.truncated.svg" alt="Thermotoga phylogenetic tree and the presence of a GH3-CE7 gene cluster" style="width:100%">
<figcaption align = "center"><b>Fig.1 - Rooted phylogenetic tree of Thermotoga, annotated with the presence of a GH3 gene cluster</b></figcaption>
</figure>

### C. Addressing proteins that were not clustered

`FlaGs` clusters all flanking genes that it identifies, to facilitate identitying conserved sets of flanking genes. Some proteins were assigned to clusters of their own, containing no additional proteins, and `FlaGs` failed to retrieve flanking genes for some of the GH3 proteins. This section walks through the methods used to explore the causes of the events for GH3 genes flanked by a CE7 encoding gene.

#### _Thermotoga_ sp. 2812B (GCF_000789335.1)

To determine if the unclustered protein from _Thermotoga_ sp. 2812B (GCF_000789335.1) was a CE7 protein, `cazy_webscraper` was used to retrieve the protein sequences from GenBank for all proteins in CE7.

```bash
cw_get_genbank_seqs cazy_database.db <user email> --families CE7
```

The protein sequences were written to the local CAZyme database, and extracted to a FASTA file using `cazy_webscraper`.

```bash
cw_extract_db_seqs \
  cazy_database.db \
  genbank \
  --families CE7 \
  --fasta_file data/gh3_complex/cazy_ce7_proteins.fasta \
  -f -n
```

In total, 2,664 protein sequences were retrieved from NCBI and written to the fasta a file [`cazy_ce7_proteins.fasta`]().

The nucleotide sequence of the gene that encoded the putative CE7 protein (named by FlaGs as pseudogene_69.1) was mannualy retrieved from genome (GCF_000789335.1). Both the forward and reverse strand sequences were retrieved, and written to a single fasta file located at [`data/g3_complex/unclustered_ce7_nt.fasta`]().
- Gene: axeA
- Locus tag: T2812B_RS04530
- Product: Cephalosporin-C deacetylase
- location: complement(901723..902701)


The nucleotide sequence was translated to a protein sequence (specifically the reverse strand was translated), and the protein sequence was stored at [`data/gh3_complex/unclustered_ce7_prt.fasta]().

The Python script `run_blastp_unclustered_ce7.py` was used to query the potential CE7 protein from _Thermotoga_ sp. 2812B against all GenBank proteins in the CAZy family CE7. To allow for greater sequence diversity between proteins with a similar structure the BLOSUM45 matrix was used.

To repeat this analysis run the following command from the root of this repository:
```bash
python3 scripts/gh3_complex/run_blastp_unclustered_ce7.py
```

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

```sql
WITH Tax_Query (tax_gbk, organism_genus, organism_sp) AS (
	SELECT DISTINCT GenBanks.genbank_accession, Taxs.genus, Taxs.species
	FROM Genbanks
	INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
	WHERE Genbanks.genbank_accession = 'AIY86427.1'
), Fam_Query (fam_gbk, cazy_family) AS (
	SELECT Genbanks.genbank_accession, CazyFamilies.family
	FROM Genbanks
	INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
	INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
	WHERE Genbanks.genbank_accession = 'AIY86427.1'
), Ec_Query (ec_gbk, ec_annotation) AS (
	SELECT Genbanks.genbank_accession, Ecs.ec_number
	FROM Genbanks
	INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
	INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
	WHERE Genbanks.genbank_accession = 'AIY86427.1'
), Uniprot_Query (uni_gbk, uniprot) AS (
	SELECT Genbanks.genbank_accession, UniProts.uniprot_accession
	FROM Genbanks
	INNER JOIN Uniprots ON Genbanks.genbank_id = Uniprots.genbank_id
	WHERE Genbanks.genbank_accession = 'AIY86427.1'
)
SELECT DISTINCT Genbanks.genbank_accession, Tax_Query.organism_genus, Tax_Query.organism_sp, Fam_Query.cazy_family, Ec_Query.ec_annotation, Uniprot_Query.uniprot
FROM Genbanks
LEFT JOIN Tax_Query ON Genbanks.genbank_accession = Tax_Query.tax_gbk
LEFT JOIN Fam_Query ON Genbanks.genbank_accession = Fam_Query.fam_gbk
LEFT JOIN Ec_Query ON Genbanks.genbank_accession = Ec_Query.ec_gbk
LEFT JOIN Uniprot_Query ON Genbanks.genbank_accession = Uniprot_Query.uni_gbk
WHERE Genbanks.genbank_accession = 'AIY86427.1'
```

The source organism was returned as 'Thermotoga	sp. 2812B', with the only CAZy family annotation being CE7. No EC number annotations of UniProt ID was returned.

This query was expanded to retrieve data for the 12 proteins with greater than or equal to 90% precentage identity with the query unclustered CE7 protein.
```sql
WITH Tax_Query (tax_gbk, organism_genus, organism_sp) AS (
	SELECT DISTINCT GenBanks.genbank_accession, Taxs.genus, Taxs.species
	FROM Genbanks
	INNER JOIN Taxs ON Genbanks.taxonomy_id = Taxs.taxonomy_id
	WHERE Genbanks.genbank_accession = 'AIY86427.1' OR
		Genbanks.genbank_accession = 'AKE29758.1' OR
		Genbanks.genbank_accession = 'AGL49000.1' OR
		Genbanks.genbank_accession = 'NP_227893.1' OR
		Genbanks.genbank_accession = 'AKE26023.1' OR
		Genbanks.genbank_accession = 'AHD18153.1' OR
		Genbanks.genbank_accession = 'AAD35171.1' OR
		Genbanks.genbank_accession = 'AKE27885.1' OR
		Genbanks.genbank_accession = 'ACB09222.1' OR
		Genbanks.genbank_accession = 'ADA66802.1' OR
		Genbanks.genbank_accession = 'ABQ46866.1' OR
		Genbanks.genbank_accession = 'AIY88183.1'
), Fam_Query (fam_gbk, cazy_family) AS (
	SELECT Genbanks.genbank_accession, CazyFamilies.family
	FROM Genbanks
	INNER JOIN Genbanks_CazyFamilies ON Genbanks.genbank_id = Genbanks_CazyFamilies.genbank_id
	INNER JOIN CazyFamilies ON Genbanks_CazyFamilies.family_id = CazyFamilies.family_id
	WHERE Genbanks.genbank_accession = 'AIY86427.1' OR
		Genbanks.genbank_accession = 'AKE29758.1' OR
		Genbanks.genbank_accession = 'AGL49000.1' OR
		Genbanks.genbank_accession = 'NP_227893.1' OR
		Genbanks.genbank_accession = 'AKE26023.1' OR
		Genbanks.genbank_accession = 'AHD18153.1' OR
		Genbanks.genbank_accession = 'AAD35171.1' OR
		Genbanks.genbank_accession = 'AKE27885.1' OR
		Genbanks.genbank_accession = 'ACB09222.1' OR
		Genbanks.genbank_accession = 'ADA66802.1' OR
		Genbanks.genbank_accession = 'ABQ46866.1' OR
		Genbanks.genbank_accession = 'AIY88183.1'
), Ec_Query (ec_gbk, ec_annotation) AS (
	SELECT Genbanks.genbank_accession, Ecs.ec_number
	FROM Genbanks
	INNER JOIN Genbanks_Ecs ON Genbanks.genbank_id = Genbanks_Ecs.genbank_id
	INNER JOIN Ecs ON Genbanks_Ecs.ec_id = Ecs.ec_id
	WHERE Genbanks.genbank_accession = 'AIY86427.1' OR
		Genbanks.genbank_accession = 'AKE29758.1' OR
		Genbanks.genbank_accession = 'AGL49000.1' OR
		Genbanks.genbank_accession = 'NP_227893.1' OR
		Genbanks.genbank_accession = 'AKE26023.1' OR
		Genbanks.genbank_accession = 'AHD18153.1' OR
		Genbanks.genbank_accession = 'AAD35171.1' OR
		Genbanks.genbank_accession = 'AKE27885.1' OR
		Genbanks.genbank_accession = 'ACB09222.1' OR
		Genbanks.genbank_accession = 'ADA66802.1' OR
		Genbanks.genbank_accession = 'ABQ46866.1' OR
		Genbanks.genbank_accession = 'AIY88183.1'
), Uniprot_Query (uni_gbk, uniprot) AS (
	SELECT Genbanks.genbank_accession, UniProts.uniprot_accession
	FROM Genbanks
	INNER JOIN Uniprots ON Genbanks.genbank_id = Uniprots.genbank_id
	WHERE Genbanks.genbank_accession = 'AIY86427.1' OR
		Genbanks.genbank_accession = 'AKE29758.1' OR
		Genbanks.genbank_accession = 'AGL49000.1' OR
		Genbanks.genbank_accession = 'NP_227893.1' OR
		Genbanks.genbank_accession = 'AKE26023.1' OR
		Genbanks.genbank_accession = 'AHD18153.1' OR
		Genbanks.genbank_accession = 'AAD35171.1' OR
		Genbanks.genbank_accession = 'AKE27885.1' OR
		Genbanks.genbank_accession = 'ACB09222.1' OR
		Genbanks.genbank_accession = 'ADA66802.1' OR
		Genbanks.genbank_accession = 'ABQ46866.1' OR
		Genbanks.genbank_accession = 'AIY88183.1'
)
SELECT DISTINCT Genbanks.genbank_accession, Tax_Query.organism_genus, Tax_Query.organism_sp, Fam_Query.cazy_family, Ec_Query.ec_annotation, Uniprot_Query.uniprot
FROM Genbanks
LEFT JOIN Tax_Query ON Genbanks.genbank_accession = Tax_Query.tax_gbk
LEFT JOIN Fam_Query ON Genbanks.genbank_accession = Fam_Query.fam_gbk
LEFT JOIN Ec_Query ON Genbanks.genbank_accession = Ec_Query.ec_gbk
LEFT JOIN Uniprot_Query ON Genbanks.genbank_accession = Uniprot_Query.uni_gbk
	WHERE Genbanks.genbank_accession = 'AIY86427.1' OR
		Genbanks.genbank_accession = 'AKE29758.1' OR
		Genbanks.genbank_accession = 'AGL49000.1' OR
		Genbanks.genbank_accession = 'NP_227893.1' OR
		Genbanks.genbank_accession = 'AKE26023.1' OR
		Genbanks.genbank_accession = 'AHD18153.1' OR
		Genbanks.genbank_accession = 'AAD35171.1' OR
		Genbanks.genbank_accession = 'AKE27885.1' OR
		Genbanks.genbank_accession = 'ACB09222.1' OR
		Genbanks.genbank_accession = 'ADA66802.1' OR
		Genbanks.genbank_accession = 'ABQ46866.1' OR
		Genbanks.genbank_accession = 'AIY88183.1'
```

The results are stored in [`results/unclustedCE7_cazy_query.csv`]().

All 12 proteins were from _Thermotoga_ species.

To investigate if the entire GH3-CE7 gene cluster was conserved, the protein record of the product from the gene immediately upstream of the GH3 (WP_008194121.1) encoding gene (which was labelled by FlaGs as pseudogene_69.3) and which was individually clustered, was retrieved mannually from the _Thermotoga_ sp. 2812B (GCF_000789335.1) assembly (ASM78933v1).
- Locus tag: T2812B_RS04540
- Product: ABC transporter ATP-binding protein
- Protein: WP_004082591.1
- location: complement(905080..906083)

The protein was annotated as ABC transporter ATP-binding protein.

##### _Thermotoga_ sp. TBGT1765 () and _Thermtoga_ sp. TBGT1766 ()

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
