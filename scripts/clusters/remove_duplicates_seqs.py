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
"""Remove protein sequences that appaer in both FASTAs, and retain the seqs in only one FASTA"""


import logging

from typing import List, Optional

from Bio import SeqIO
from saintBioutils.utilities.file_io import make_output_directory
from tqdm import tqdm


FAMILY_FASTA = "data/cluster_data/all_fam_seqs.fasta"
CLUSTERS_FASTA = "data/cluster_data/all_clusters.fasta"
REMAINING_FASTA = "data/cluster_data/remaining_fam_seqs.fasta"


def main():
    
    clustal_protein_accessions = set()
    for record in SeqIO.parse(CLUSTERS_FASTA, "fasta"):
        clustal_protein_accessions.add(record.id)
    print(f"Loaded {len(clustal_protein_accessions)} sequences from: {CLUSTERS_FASTA}")

    family_seqs = {}  # {acc: record}
    for record in SeqIO.parse(FAMILY_FASTA, "fasta"):
        family_seqs[record.id] = record
    print(f"Loaded {len(list(family_seqs.keys()))} sequences from: {FAMILY_FASTA}")

    protein_records = []
    for acc in tqdm(family_seqs, desc="Getting protein records"):
        if acc not in clustal_protein_accessions:
            protein_records.append(family_seqs[acc])

    print(f"Writing {len(protein_records)} to {REMAINING_FASTA}")
    SeqIO.write(protein_records, REMAINING_FASTA, "fasta")


if __name__ == "__main__":
    main()
