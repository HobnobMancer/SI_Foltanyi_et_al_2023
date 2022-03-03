#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) University of St Andrews 2022
# (c) University of Strathclyde 2022
# (c) James Hutton Institute 2022
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
"""Script for invoking dbCAN"""


import argparse
import pandas as pd

from pathlib import Path

from tqdm import tqdm

from saintBioutils.utilities.file_io import make_output_directory
from saintBioutils.utilities.file_io import get_paths


FAMILIES_OF_INTEREST = [
    "GH3",
]


def main():
    parser = build_parser()
    args = parser.parse_args()

    make_output_directory(args.tab_annno_list.parent, args.force, args.nodelete)

    # get the path to output directories
    output_dir = list(set(get_paths.get_dir_paths(args.input_dir)))

    print(f"Retrieved {len(output_dir)} directories from {args.input_dir}")

    for dir_path in tqdm(output_dir, desc="Parsing dbCAN output"):
        parse_dbcan(dir_path, args)


def parse_dbcan(dir_path, args):
    """Parse output from dbCAN and get proteins from fams of interest.
    
    :param dir_path: Path, path to output directory
    
    Return nothing."""
    overview_path = dir_path / "overview.txt"
    genomic_accession = dir_path.name

    proteins_of_interest = []  # list of strings, f"{genome}\t{protein accession}" for proteins from fams of interest

    dbcan_df = pd.read_csv(overview_path, sep='\t', header=0)

    index = 0
    for index in tqdm(range(len(dbcan_df)), desc="Parsing dbCAN overview.txt file"):
        row = dbcan_df.iloc[index]
        protein_accession = row['Gene ID']

        tools = row["#ofTools"]
        if tools < 2:  # no consensus prediction found
            continue

        annotations = {}
        for tool in ['HMMER', 'eCAMI', 'DIAMOND']:
            outputs = row[tool].split("+")
            for result in outputs:
                fam = result.split("(")[0]
                fam = fam.split("_")[0]
                try:
                    annotations[tool].add(fam)
                except KeyError:
                    annotations[tool] = {fam}

        hmmer_ecami_consensus = list(set(annotations['HMMER']) & set(annotations['eCAMI']))
        ecami_diamond_consensus = list(set(annotations['eCAMI']) & set(annotations['DIAMOND']))
        hmmer_diamond_consensus = list(set(annotations['HMMER']) & set(annotations['DIAMOND']))

        # get the CAZyme domains predicted by all prediction tools
        all_consensus = list(set(annotations['HMMER']) & set(annotations['eCAMI']) & set(annotations['DIAMOND']))

        # combine all consensus results
        combined_consensus = (
            hmmer_ecami_consensus + ecami_diamond_consensus + hmmer_diamond_consensus + all_consensus
        )
        # remove duplicate entries
        combined_consensus = list(set(combined_consensus))

        if (annotations['HMMER'] == annotations['eCAMI']) or (annotations['HMMER'] == annotations['DIAMOND']) or (annotations['eCAMI'] == annotations['DIAMOND']):
            for fam in combined_consensus:
                if fam in FAMILIES_OF_INTEREST:
                    proteins_of_interest.append(f"{genomic_accession}\t{protein_accession}\n")
                    
    # write out annotations of fams of interest to the tab-deliminted list
    with open(args.tab_annno_list, "a") as fh:
        for line in proteins_of_interest:
            fh.write(line)


def build_parser():
    """Return ArgumentParser parser for script."""
    # Create parser object
    parser = argparse.ArgumentParser(
        prog="get_dbcan_cazymes.py",
        description="Get proteins from CAZy families of interest",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Add positional arguments to parser

    parser.add_argument(
        "input_dir",
        type=Path,
        help="Path to directory containing FASTAs to be parsed by dbCAN",
    )

    parser.add_argument(
        "tab_annno_list",
        type=Path,
        default=None,
        help="Path to write out tab deliminated list",
    )

    # Add option to specific directory for log to be written out to
    parser.add_argument(
        "-l",
        "--log",
        type=Path,
        metavar="log file name",
        default=None,
        help="Defines log file name and/or path",
    )

    # Add option to specify verbose logging
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="Set logger level to 'INFO'",
    )

    return parser


if __name__ == "__main__":
    main()