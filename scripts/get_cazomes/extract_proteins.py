#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) University of St Andrews 2021
# (c) University of Strathclyde 2021
# (c) The James Hutton Insitute 2021
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
"""Script for extracting protein sequences from genomic assemblies for single ortholog search"""


import argparse
import logging
import shutil
import sys

from pathlib import Path

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from tqdm import tqdm

from saintBioutils.utilities.logger import config_logger
from saintBioutils.utilities.file_io import make_output_directory
from saintBioutils.utilities.file_io import get_paths


def main():
    """Coordinate the retrieval of protein annotations from GenBank (.gbff) files.
    Including building parser, logger and output directory.
    Return dataframe of protein data.
    """
    parser = build_parser()
    args = parser.parse_args()

    config_logger(args)
    logger = logging.getLogger(__package__)

    make_output_directory(args.output_dir, args.force, args.nodelete)

    # get paths to genomic assemblies
    genomic_assembly_paths = get_paths.get_file_paths(args.input_dir, suffixes='genomic.gbff')

    if len(genomic_assembly_paths) == 0:
        logger.error(
            f"Found 0 assemblies in {args.input_dir}\n"
            "Check the path is correct. Terminating program"
        )
        sys.exit(1)

    empty_asssemblies = []

    # create fasta files
    for assembly_path in genomic_assembly_paths:
        assem_path = compile_fasta(assembly_path, args)
        if assem_path is not None:
            empty_asssemblies.append(assem_path)
    
    # move assemblies with no CDS features to a dir to be parsed by prokka and dbCAN
    for assembly_path in tqdm(empty_asssemblies):
        filename = assembly_path.name
        target_path = args.dbcan_dir / filename
        shutil.copy(assembly_path, target_path)


def compile_fasta(assembly_path, args):
    """Create a fasta file of the proteins contained in the genomic assembly.

    :param assembly_path: Path to genomic assembly
    :param args: cmd-line args parser

    Return nothing.
    """
    logger = logging.getLogger(__name__)

    no_proteins_path = args.output_dir / "genomes_with_no_proteins.log"

    # compile fasta name species.fasta
    name_fragments = (assembly_path.name).split("_")
    genomic_accession = name_fragments[0] + name_fragments[1]
    genomic_accession = genomic_accession.replace("GCA", "GCA_")

    species = ""

    with open(assembly_path, "rt") as handle:
        for gb_record in SeqIO.parse(handle, "genbank"):
            for (index, feature) in enumerate(gb_record.features):
                if feature.type == "source":
                    species = get_record_feature(feature, "organism", "", genomic_accession)
                    if species != "":
                        break
            if species != "":
                break

    fasta_species = species.replace(" ", "_")
    fasta_path = f"{fasta_species}_{genomic_accession}.fasta"

    output_path = args.output_dir / fasta_path

    proteins = []

    with open(assembly_path, "rt") as handle:  # unzip the genomic assembly
        for gb_record in SeqIO.parse(handle, "genbank"):
            for (index, feature) in enumerate(gb_record.features):
                # Parse over only protein encoding features (type = 'CDS')
                if feature.type == "CDS":
                    protein_accession = get_record_feature(feature, "protein_id", "", genomic_accession)

                    product = get_record_feature(feature, "product", protein_accession, genomic_accession)

                    gene_id = get_record_feature(feature, "protein_id", protein_accession, genomic_accession)

                    if protein_accession == "":
                        protein_accession = gene_id

                    seq = get_record_feature(feature, "translation", protein_accession, genomic_accession)
                    if seq == "":
                        continue

                    new_record = SeqRecord(Seq(seq), id=protein_accession, name=product)
                    proteins.append(new_record)

    logger.warning(f"{len(proteins)} proteins in genomic assembly {genomic_accession}")

    if len(proteins) == 0:
        with open(no_proteins_path, "a") as fh:
            fh.write(f"{genomic_accession}\n")
        return assembly_path

    SeqIO.write(list(proteins), output_path, 'fasta')

    return


def get_record_feature(feature, qualifier, accession, genomic_accession):
    """Retrieve data from BioPython feature object.

    :param feature: BioPython feature object representing the curernt working protein
    :param qualifier: str, data to be retrieved
    :accession_number: str, accession of the protein being parsed.

    Return feature data.
    """
    logger = logging.getLogger(__name__)

    try:
        data = feature.qualifiers[qualifier][0]
        return data
    except KeyError:
        if qualifier == "protein_id":
            logger.warning(
                f"Failed to the protein id for {accession} in {genomic_accession}\n"
                "The ene_id will be written in its place"
            )
        else:
            logger.warning(
            f"Failed to retrieve feature {qualifier}\n" 
            f"for protein {accession} in {genomic_accession}\n"
            "Returning an empty string it its place."
        )
        return ""


def build_parser():
    """Return ArgumentParser parser for script."""
    # Create parser object
    parser = argparse.ArgumentParser(
        prog="extract_proteins.py",
        description="Retrieve protein annotations from GenBank files",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Add positional arguments to parser

    # Specify path to input dataframe
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Path to input dir containing genomic assemblies",
    )
    # Specify path to directory containing GenBank files
    parser.add_argument(
        "output_dir",
        type=Path,
        help="Path to output directory",
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
