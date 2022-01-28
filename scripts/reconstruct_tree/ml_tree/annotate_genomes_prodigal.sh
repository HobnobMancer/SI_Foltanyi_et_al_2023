#!/usr/bin/env bash
#
# annotate_genomes.sh
#
# Annotate genomes using prodigal

$1  # directory containing downloaded genomes

# Create output directories
mkdir $1/proteins
mkdir $1/cds
mkdir $1/gbk

# Annotate genomes
for fname in $1/*.fna
do
    prodigal \
      -a $1/proteins/`basename ${fname%%fna}`faa \
      -d $1/cds/`basename ${fname%%fna}`fasta \
      -i ${fname} \
      -o $1/gbk/`basename ${fname%%fna}`gbk
done