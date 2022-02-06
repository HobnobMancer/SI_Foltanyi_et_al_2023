61 lines (55 sloc)  1.78 KB
   
#!/usr/bin/env bash

# (c) University of St Andrews 2020-2021
# (c) University of Strathclyde 2020-2021
# (c) James Hutton Institute 2020-2021
#
# Author:
# Emma E. M. Hobbs
#
# Contact
# eemh1@st-andrews.ac.uk
#
# Emma E. M. Hobbs,
# Biomolecular Sciences Building,
# University of St Andrews,
# North Haugh Campus,
# St Andrews,
# KY16 9ST
# Scotland,
# UK
#
# The MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# cluster_gh3.sh
#
# Use MMseq2 with minimum 80% sequence identity and coverage to cluster GH3 protein sequences
# and find potential homologs with similar functions

# create a MMseq2 databasae (DB)
mmseqs createdb all_cazy_2022_01_13/gh3_protein_seq.fasta gh3_mmseq_db

# run cluster
mmseqs cluster gh3_mmseq_db gh3_mmseq_db_clustered tmp --min-seq-id 0.8 -c 0.8

# create tsv output 
mmseqs createtsv gh3_mmseq_db gh3_mmseq_db gh3_mmseq_db_clustered gh3_mmseq_db_clustered.tsv
