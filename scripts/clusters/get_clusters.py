#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) University of St Andrews 2020-2021
# (c) University of Strathclyde 2020-2021
# Author:
# Emma E. M. Hobbs

# Contact
# eemh1@st-andrews.ac.uk

# Emma E. M. Hobbs,
# Biomolecular Sciences Building,
# University of St Andrews,
# North Haugh Campus,
# St Andrews,
# KY16 9ST
# Scotland,
# UK

# The MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Extract information from clusters"""


import json

import pandas as pd

from tqdm import tqdm


# inputs
MMSEQ_TSV = "all_cazy_2022_01_13/mmseq_ec_clustering/mmseq_cluster_70_output.tsv"
# outputs
CSV_OUTOUT = "all_cazy_2022_01_13/mmseq_ec_clustering/mmseq_cluster_70_summaries.csv"
JSON_OUTPUT = "all_cazy_2022_01_13/mmseq_ec_clustering/clusters_70.json"


def main():
    mmseq_output = pd.read_table(MMSEQ_TSV)

    clusters = parse_mmseq(mmseq_output)

    get_cluster_info(clusters)

    with open(JSON_OUTPUT, "w") as fh:
        json.dump(clusters, fh)    


def parse_mmseq(mmseq_output):
    """Parse mmseq output into a dict.
    
    :param mmseq_output: pandas df containing mmseq output
    
    Return dict"""
    clusters = {}

    index = 0
    for index in tqdm(range(len(mmseq_output)), desc="Parsing MMseq"):
        row = mmseq_output.iloc[index]

        cluster_acc = row[0]
        member_acc = row[1]

        try:
            clusters[cluster_acc].add(member_acc)
        except KeyError:
            clusters[cluster_acc] = {member_acc}

    # convert sets to lists so can be serialised in a JSON file
    serialisable_clusters ={}
    for cluster in clusters:
        serialisable_clusters[cluster] = list(clusters[cluster])

    return serialisable_clusters


def get_cluster_info(clusters):
    """Extract information from the clusters and write to txt file.
    
    :param clusters: dict of mmseq output
    
    Return nothing
    """
    data = []

    # total number of clusters
    total_clusters = len(list(clusters.keys()))

    print(f"Total number of clusters: {total_clusters}")
    
    for cluster in clusters:
        new_data = [cluster]

        size = len(clusters[cluster])
        new_data.append(size)

        data.append(new_data)
    
    df = pd.DataFrame(data, columns=["cluster", "size"])

    df.to_csv(CSV_OUTOUT)

    return


if __name__ == "__main__":
    main()
