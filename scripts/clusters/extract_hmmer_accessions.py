#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) University of St Andrews 2022
# (c) University of Strathclyde 2022
# (c) James Hutton Institute 2022
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
"""Extract GenBank accessions from HMMER output and write to file. Also, add the relevant protein sequences 
to the protein pool"""


from Bio import SeqIO, SearchIO
from tqdm import tqdm


HMMER_OUTPUT = "supplementary/cluster_data/ec_hmm_search_results"  # output from HMMER3 hmmsearch
CLUSTERS_FASTA = "data/cluster_data/all_clusters.fasta"  # fasta file of protein sequences in the clusters of interest
REMAINING_FASTA = "data/cluster_data/remaining_fam_seqs.fasta"  # fasta file of proteins from families of interest that are not in the clusters
FINAL_FASTA = "data/cluster_data/expanded_protein_pool.fasta"


def main():
    
    hmmer_accessions = get_hmmer_accessions()

    cluster_records = []
    for record in SeqIO.parse(CLUSTERS_FASTA, "fasta"):
        cluster_records.append(record)
    print(f"Loaded {len(cluster_records)} sequences from: {CLUSTERS_FASTA}")

    protein_records = {}
    for record in SeqIO.parse(REMAINING_FASTA, "fasta"):
        protein_records[record.id] = record
    print(f"Loaded {len(list(protein_records.keys()))} sequences from {REMAINING_FASTA}")

    for acc in tqdm(hmmer_accessions, desc="Adding hmmsearch hits to the protein pool"):
        cluster_records.append(protein_records[acc])

    print(f"Writing {len(cluster_records)} to {FINAL_FASTA}")
    SeqIO.write(cluster_records, FINAL_FASTA, "fasta")


def get_hmmer_accessions():
    """Load and parse hmmsearch output, extracting the accessions of protein hits.
    
    Return set of GenBank protein accessions."""
    for result in SearchIO.parse(HMMER_OUTPUT, "hmmer3-text"):
        hmmer_text = result

    hmmer_accessions = set()
    for item in hmmer_text.items:
        hmmer_accessions.add(item[0])
    
    return hmmer_accessions


if __name__ == "__main__":
    main()
