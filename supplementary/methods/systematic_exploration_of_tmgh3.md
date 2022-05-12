# Systematic exploration of tmgh3

Below is the comprehensive method for exploring _TmGH3_, including all comamnds used.

The exploration is broken up into X steps:

Preliminary exploration:
- [Query tmgh against the NR database](#query_tmgh_against_the_nr_database)
- [Query tmgh against the CAZy database](#query_tmgh_against_the_cazy_database)
- [Compare NR and CAZy hits](#compare-nr-and-cazy-hits)

Further exploration of HHpred:
- [Generation of a MSA of xylosdiases](#generation-of-a-MSA-of-xylosidases)
- [HHpred](#HHpred)

Interrogation of CAZy:
- [Interrogation of the CAZy database](#interrogation-of-the-cazy-database)

The protein sequence of _tmgh3_ is stored in [`data/tmgh3_exploration/tmgh3.fasta`](https://hobnobmancer.github.io/Foltanyi_et_al_2022/data/tmgh3_exploration.zip). All analyses were performed in March 2022.

## Query tmgh against the NR database

As a preliminary search to identify potentially functionally similar proteins to infer functional and structural information about _tmgh3_, the 
[non-redundant database](https://www.ncbi.nlm.nih.gov/refseq/about/nonredundantproteins/#related-documentation) was queried using BLASTP.

> Altschul, S. F., Gish, W., Miller, W., Myers, E. W., Lipman, D. J. (1990) 'Basic local alignment search tool', Journal of Molecular Biology, 215(3), pp. 403-10

This was done via the NCBI BLASTP (webinterface)[https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastp&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome] using default query parameters.

The reults of the query against the NR database were stored in [`results/tmgh3_nr_query_desc_table.csv`](https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/tmgh3_nr_query_desc_table.csv).

A 70% identity cut-off was used to select proteins, which is widely accepted as a reasonably cut-off for selecting proteins that share the first 3 digits of their respective EC numbers.

The protein sequences of the 19 hits with sequence identity of equal to or greater than 70% against _tmgh3_ were written to the FASTA file `data/tmgh3_exploration/nr_hits.fasta`.

## Query tmgh3 against the CAZy database

The CAZy website does not support querying the database using BLASTP. Therefore, `cazy_webscraper` was used to facilitate a BLASTP comparison of the protein sequence of _tmgh3_ against the CAZy database. 

cazy_webscraper` was used to extract the GenBank protein sequences for all proteins in GH CAZy families of interest from the local CAZyme database and write them to a FASTA file.
```bash
cw_extract_protein_sequences \
  cazy_database.db genbank \
  --families GH1,GH2,GH3,GH11,GH26,GH30,GH43,GH51,GH52,GH54,GH116,GH120 \
  --fasta_file data/tmgh3_exploration/cazy_proteins_seqs.fasta \
  -f -n
```

The Python script `run_blastp_cazy.py` was used to query _tmgh3_ against the proteins from the GH protein sequences from CAZy GH families of interest using BLASTP. To repeat this analysis, run the following command from the root of the repository.
```bash
python3 scripts/tmgh3_exploration/run_blastp_cazy.py
```

The results were written to [`results/cazy_blastp_results.tsv`](https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/cazy_blastp_results.tsv).

The protein sequences of the 19 hits with sequence identity of equal to or greater than 70% against _tmgh3_ were written to the FASTA file `data/tmgh3_exploration/cazy_hits.fasta`.

## Compare NR and CAZy hits

Both the BLASTP query against the NR and CAZy databases returned 19 proteins from _Thermotoga_ with percentage identities of equal to or greater than 70% against _tmgh3_. 

The BLASTP query of _tmgh3_ against the CAZy database returned GenBank protein IDs not RefSeq protein IDs.

To determine if the 19 hits from the BLASTP NR query (step A) were the non-redundanrt protein sequence representatives of the 19 hits from the BLASTP CAZy query (step B), the Python script `run_blastp_nr_cazy.py` was used to perform a BLASTP analysis of the 19 hits from NR query (step A) against the 19 hits from querying CAZy (step B).

To repeat this analysis, run the following command from the root of the repository.
```bash
python3 scripts/tmgh3_exploration/run_blastp_nr_cazy.py
```

The resulting `tsv` file was written to [`results/nr_cazy_blastp_results.tsv`](https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/nr_cazy_blastp_results.tsv).

The protein sequences for the 15 of the 19 from NR shared 100% sequence identity with at least one protein from CAZy, the remaining proteins shared greater than 90% sequence identity with at least one protein from CAZy.

## Generation of a MSA of xylosidases

Previously _tmgh3_ had been queried against HHpred to find potential templates for molecular modelling. To explore the potential cause for HHpred returning many non-functionally relevant proteins and few xylosidases, the analysis using HHpred was repeated using an MSA of xylosdiase protein sequences.

To create the MSA the proteins sequences 19 hits from quering the NR database and the 19 hits from querying the CAZy database, which had greater than or equal to 70% sequence identity with _tmgh3_ were combined into a single fasta file. This is located at [`data/tmgh3_exploration/nr_and_cazy_hits.fasta`]().

The previous BLASTP query of the NR hits against the CAZy hits revealed several NR hits shared 100% sequence identity with hits from CAZy. Therefore, [`seqkit`](https://bioinf.shenwei.me/seqkit/) (v2.2.0) was used to remove redundant protein sequences based upon sequence.
```bash
seqkit rmdup -s data/tmgh3_exploration/nr_and_cazy_hits.fasta data/tmgh3_exploration/nr_cazy_hits_nonred.fasta
```

`MAFFT` [Katoh et al., 2002] (v7.505) was used to align the protein sequences. To repeat this analysis run the following command from the root of the repository.
```bash
mafft --thread 12 data/tmgh3_exploration/nr_cazy_hits_nonred.fasta > data/tmgh3_exploration/nr_and_cazy_hits_aligned.fasta
```

> Katoh K, Misawa K, Kuma K, Miyata T. MAFFT: a novel method for rapid multiple sequence alignment based on fast Fourier transform. Nucleic Acids Res. 2002 Jul 15;30(14):3059-66. doi: 10.1093/nar/gkf436. PMID: 12136088; PMCID: PMC135756.

## HHpred

HHpred was run using the default parameters (via the [HHpred webserver](https://toolkit.tuebingen.mpg.de/tools/hhpred)) and the MSA stored in `data/tmgh3_exploration/nr_and_cazy_hits_aligned.fasta`. 

> Söding J, Biegert A, Lupas AN. The HHpred interactive server for protein homology detection and structure prediction. Nucleic Acids Res. 2005 Jul 1;33(Web Server issue):W244-8. doi: 10.1093/nar/gki408. PMID: 15980461; PMCID: PMC1160169.

The results are stored in [`results/hhpred_results.hhr`](https://hobnobmancer.github.io/Foltanyi_et_al_2022/results/hhpred_results.hhr).

Using the MSA did not signficantly increase the number of functionally relevant hits returned by HHpred. In general, the results between the two queries were similar. This potentially reflects the limited knowledge pool for _Thermotoga_ glycoside hydrolase GH3 proteins.

## Interrogation of the CAZy database

A series of SQL commands were peformed to interrogoate the local CAZyme database. The commands are presented [here](https://hobnobmancer.github.io/Foltanyi_et_al_2022/sql_queries/), and all results are stored in the repository in the [`sql_queries/` dir](https://github.com/HobnobMancer/Foltanyi_et_al_2022/tree/master/sql_queries).
