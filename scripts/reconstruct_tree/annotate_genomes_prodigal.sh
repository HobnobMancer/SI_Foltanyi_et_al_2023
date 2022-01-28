#!/usr/bin/env bash
#
# annotate_genomes.sh
#
# Annotate genomes using prodigal

# Create output directories
mkdir genomes/proteins
mkdir genomes/cds
mkdir genomes/gbk

# Annotate genomes
for fname in genomes/*.fna
do
    prodigal \
      -a genomes/proteins/`basename ${fname%%fna}`faa \
      -d genomes/cds/`basename ${fname%%fna}`fasta \
      -i ${fname} \
      -o genomes/gbk/`basename ${fname%%fna}`gbk
done