# /usr/bin/env python
# -*- coding: utf-8 -*-
"""extract_cds.py

Script to match aligned single-copy orthologue protein sequences from
MAFFT alignments with the corresponding CDS sequences, prior to
backtranslation/threading with t-coffee.
"""
import os

from pathlib import Path

from Bio import SeqIO
from tqdm import tqdm

# PROTDIR contains the MAFFT alignments
PROTDIR = Path("orthologues/Results_May28/Single_Copy_Orthologue_Sequences")

# CDSDIR contains the CDS/proteome for each genome
CDSDIR = Path("genomes/cds")

# OUTDIR is the location to which CDS sequences corresponding to the
# protein alignments will be written
OUTDIR = Path("sco_cds")

# The protein sequences have IDs in the form NC_004547.2_1; this is not
# enough to identify the corresponding genome sequence/CDS file. We take
# a brute force approach and load all CDS into memory
print("Loading CDS sequences into memory.")
seqdict = {}
for cdsfpath in tqdm(CDSDIR.iterdir()):
    seqdict.update(SeqIO.to_dict(SeqIO.parse(cdsfpath, "fasta")))
print(f"Loaded {len(seqdict)} CDS sequences.")

# We iterate over the SCO protein files, and extract the corresponding
# CDS sequences for each, then write these to OUTDIR
print(f"Writing extracted CDS files to {OUTDIR}")
os.makedirs(OUTDIR, exist_ok=True)  # Create output directory, if needed
for protfpath in tqdm(PROTDIR.iterdir()):
    with (OUTDIR / protfpath.stem).with_suffix(".fasta").open("w") as ofh:
        cds = [seqdict[_.id] for _ in SeqIO.parse(protfpath, "fasta")]
        fixed_cds = []
        for _ in cds:
            if str(_.seq[-3:]) not in ("TAA", "TAG", "TGA"):
                fixed_cds.append(_)
            else:
                fixed_cds.append(_[:-3])
        SeqIO.write(
            fixed_cds,
            ofh,
            "fasta",
        )