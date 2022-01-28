#!/usr/bin/env bash
#
# align_scos.sh
#
# Align single-copy orthologue sequences using MAFFT

$1  # directory containing output from orthofinder, e.g. orthologues/Results_Nov11/Single_Copy_Orthologue_Sequences

# Create output directory
mkdir -p sco_proteins_aligned

# Align each set of SCOs
for fname in $1/*.fa
do
    mafft --thread 12 ${fname} > sco_proteins_aligned/`basename ${fname%%.fa}`_aligned.fasta
done
