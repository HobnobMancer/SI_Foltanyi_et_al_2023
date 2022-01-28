#!/usr/bin/env bash
#
# raxml_ng_build_tree.sh
#
# Build maximum parsimony tree using raxml-ng, with
# bootstrap support

mkdir tree

raxml-ng --check \
  --msa concatenated_cds/concatenated.fasta \
  --model concatenated_cds/concatenated.part \
  --prefix tree/01_check

raxml-ng --parse \
  --msa concatenated_cds/concatenated.fasta \
  --model concatenated_cds/concatenated.part \
  --prefix tree/02_parse

raxml-ng \
  --msa concatenated_cds/concatenated.fasta \
  --model concatenated_cds/concatenated.part \
  --threads 8 \
  --seed 38745 \
  --prefix tree/03_infer

raxml-ng --bootstrap \
  --msa concatenated_cds/concatenated.fasta \
  --model concatenated_cds/concatenated.part \
  --threads 8 \
  --seed 38745 \
  --bs-trees 100 \
  --prefix tree/04_bootstrap
