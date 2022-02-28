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
"""Identify CAZymes catalogued in CAZy

:args input_dir: Path to dir containing FASTA files to retrieve CAZymes from
:args cazy: Path to CAZy dict of annotations
:args output_dir: Path to output dir to write out proteins sequences not contained in CAZy
:args tab_annno_list: Path to tab deliminted list
:args force: force writing to existing output directory and output files
:args nodelete: do not delete content in already exisiting output directory
"""


import argparse
import logging
import pandas as pd
import sys

from pathlib import Path

from Bio import SeqIO
from cazy_webscraper.sql.sql_orm import (
  CazyFamily,
  Genbank,
  Session,
  get_db_connection,
)
from saintBioutils.utilities import file_io
from saintBioutils.utilities.file_io import get_paths
from saintBioutils.utilities.logger import config_logger
from tqdm import tqdm


COLUMN_NAMES = [
    "Genome",
    "Protein",
    "Family"
]
FAMILIES_OF_INTEREST = [
    "GH1",
    "GH2",
    "GH3",
    "GH11",
    "GH26",
    "GH30",
    "GH43",
    "GH51",
    "GH52",
    "GH54",
    "GH116",
    "GH120",
]


def main():
    parser = build_parser()
    args = parser.parse_args()

    # config and get logger
    config_logger(args)
    logger = logging.getLogger(__name__)

    # make output directory
    if args.output_dir is not None:
        file_io.make_output_directory(args.output_dir, args.force, args.nodelete)

    # retrieve dictionary of CAZy classifications
    if args.cazy is not None:
        if args.cazy.exists() is False:
            logger.error(
                f"Path to local CAZyme db ({args.cazy}) does not exist\n"
                "Check the correct path was provided\n"
                "Terminating program"
            )
            sys.exit(1)
        cazy_db_connection = get_db_connection(args.cazy, args, False)

    # get paths to FASTA files of protein sequences from extract_proteins_genomes
    fasta_files_paths = list(set(get_paths.get_file_paths(args.input_dir, suffixes='fasta')))

    if len(fasta_files_paths) == 0:
        logger.error(
            f"No FASTA files retrieved from\n"
            f"{args.input_dir}\n"
            "Check the correct dir was provided\n"
            "Terminating program"
        )
        sys.exit(1)

    print(f"Retrieved {len(fasta_files_paths)} FASTA file paths from {args.input_dir}")

    all_cazy_annotations = pd.DataFrame(columns=COLUMN_NAMES)

    # get CAZy family annotations from local CAZyme db
    for fasta_path in tqdm(fasta_files_paths, desc="Getting CAZy annotations", total=len(fasta_files_paths)):
        cazy_annotations = get_cazy_annotations(fasta_path, args, cazy_db_connection)

        all_cazy_annotations = all_cazy_annotations.append(cazy_annotations, ignore_index=True)
    
    output_path = args.output_dir / "all_cazy_annotations.csv"
    all_cazy_annotations.to_csv(output_path)


def get_cazy_annotations(fasta_path, args, cazy_db_connection):
    """Get the CAZy family annotations for each fasta file.

    Move empty fasta files to directory used as input for dbCAN.

    :param fasta_path: POSIX path to FASTA file
    :param args: cmd-line args parser
    :param cazy_db_connection: open sqlalchemy db session

    Return nothing.
    """
    # extract genomic accession from the file name
    genomic_accession = (
        str(fasta_path.name).split("_")[-2] + "_" + str(fasta_path.name).split("_")[-1]
    ).replace(".fasta", "")

    cazy_annotations = []  # list of nested lists [genome, protein, family]
    fams_annotations = []  # list of strings, f"{genome}\t{protein accession}" for proteins from fams of interest
    non_cazy_proteins = []  # list of SeqIO records that will be parsed by dbCAN

    for record in SeqIO.parse(fasta_path, 'fasta'):
        protein_acc = record.id

        # query the local CAZyme database
        with Session(bind=cazy_db_connection) as session:
            db_query = session.query(Genbank, CazyFamily).\
                join(CazyFamily, Genbank.families).\
                filter(Genbank.genbank_accession==protein_acc).\
                all()

        if len(db_query) == 0:
            non_cazy_proteins.append(record)

        else:
            for obj in db_query:
                fam = obj[1].family
                cazy_data = [genomic_accession, protein_acc, fam]
                cazy_annotations.append(cazy_data)
                if fam in FAMILIES_OF_INTEREST:
                    fams_annotations.append(f"{genomic_accession}\t{protein_acc}\n")

    # write out annotations of fams of interest to the tab-deliminted list
    with open(args.tab_annno_list, "a") as fh:
        for line in fams_annotations:
            fh.write(line)
    
    # compile all retrieve annotations into a df
    cazy_annotation_df = pd.DataFrame(cazy_annotations, columns=COLUMN_NAMES)

    # write out FASTA file of proteins not in CAZy, and will be parsed by dbCAN
    non_cazy_proteins_fasta = args.output_dir / f"{fasta_path.name}_non_cazy.fasta"
    SeqIO.write(non_cazy_proteins, non_cazy_proteins_fasta, 'fasta')

    summary = (
        f"From {genomic_accession}: {len(cazy_annotations)} CAZy proteins, "
        f"{len(non_cazy_proteins)} non-CAZy proteins, {len(fams_annotations)} from fams of interest"
    )

    print(summary)
    summary_path = args.output_dir / f"summary.txt"
    with open(summary_path, "a") as fh:
        fh.write(f"{summary}\n")

    return cazy_annotation_df


def build_parser():
    """Return ArgumentParser parser for script."""
    # Create parser object
    parser = argparse.ArgumentParser(
        prog="get_cazy_cazymes.py",
        description="Retrieve CAZy annotations of CAZymes",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Add positional arguments to parser

    parser.add_argument(
        "input_dir",
        type=Path,
        help="Path to dir containing fasta files to retrieve CAZy annotations from",
    )

    parser.add_argument(
        "cazy",
        type=Path,
        default=None,
        help="Path CAZy JSON file, keyed by protein accessions, valued by list of families",
    )

    parser.add_argument(
        "output_dir",
        type=Path,
        help="Path write out fasta files for parsing by dbCAN",
    )

    parser.add_argument(
        "tab_annno_list",
        type=Path,
        default=None,
        help="Path to write out tab deliminated list",
    )

    # Add optional arguments
    # Add option to force file over writting
    parser.add_argument(
        "-f",
        "--force",
        dest="force",
        action="store_true",
        default=False,
        help="Force file over writting",
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
    # Add option to prevent over writing of existing files
    # and cause addition of files to output directory
    parser.add_argument(
        "-n",
        "--nodelete",
        dest="nodelete",
        action="store_true",
        default=False,
        help="enable/disable deletion of exisiting files",
    )
    parser.add_argument(
        "--sql_echo",
        dest="sql_echo",
        action="store_true",
        default=False,
        help="Set sqlalchemy sql_echo to True, SQL will print out its log to the terminal",
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
