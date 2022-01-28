#!/usr/bin/env bash
#
# backtranslate.sh
#
# Backtranslate CDS sequences onto aligned proteins using T-Coffee

# Prepare output directory
mkdir -p sco_cds_aligned

# Backtranslate each single-copy orthologue set
for fname in sco_cds/*.fasta
do
  t_coffee -other_pg seq_reformat \
    -in ${fname} \
    -in2 sco_proteins_aligned/`basename ${fname%%.fasta}_aligned.fasta` \
    -action +thread_dna_on_prot_aln \
    -output fasta \
    > sco_cds_aligned/`basename ${fname%%.fasta}_aligned.fasta`
done