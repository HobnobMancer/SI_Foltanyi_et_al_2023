#!/usr/bin/env bash
#
# align_scos.sh
#
# Align single-copy orthologue sequences using MAFFT

# Create output directory
mkdir -p sco_proteins_aligned

# Align each set of SCOs
for fname in orthologues/Results_May28/Single_Copy_Orthologue_Sequences/*.fa
do
    mafft --thread 12 ${fname} > sco_proteins_aligned/`basename ${fname%%.fa}`_aligned.fasta
done
