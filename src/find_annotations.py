#!/usr/bin/env python3

import argparse
import os
import webbrowser

from sources import deltablast
from sources import uniprot
from sources import kegg
from sources import go

from plots import multi_pie
from utils.tools import select_data

###################################################################################################
# Argument parser.
parser = argparse.ArgumentParser(description="Find similar proteins using Delta Blast and suggests\
                                              GO annotations and KEGG routes associated to them.")
_ = parser.add_argument("protein",
                        action="store",
                        nargs="?",
                        help="Protein to analyze")

_ = parser.add_argument("min_identity",
                        action="store",
                        type=float,
                        help="Minimum identity score to consider (Default: 75)")

_ = parser.add_argument("min_support",
                        action="store",
                        type=int,
                        help="Minimum support degree to consider (amount of sequences sharing an\
                              annotation (Default: 10)")

_ = parser.add_argument("-f",
                        "--file",
                        action="store",
                        help="Specify dblast output file with list of similar proteins")

_ = parser.add_argument("-o",
                        "--outfile",
                        action="store",
                        help="Specify output filename and path. An additional .svg file will be\
                              created.")

args = parser.parse_args()

if args.protein is None and args.file is None:
    parser.error("Specify either a protein accession or a dblast output file.")
    exit(1)
###################################################################################################


if args.file:
    print(f"* Running with file [{args.file}]", end=" ")
    name = os.path.splitext(os.path.basename(args.file))[0]

elif args.protein:
    name = os.path.splitext(os.path.basename(args.protein))[0]
    print(f"* Running with accession [{name}]", end=" ")


out = os.path.splitext(args.outfile)[0] if args.outfile is not None else name
if not os.path.exists(os.path.split(out)[0]) and os.path.split(out)[0]:
    raise Exception('Invalid output path!')
else:
    if not os.path.exists(out):
        os.makedirs(out)
    outfile=f"{out}/{os.path.split(out)[1]}"

print(f"(Min identity score: [{args.min_identity}], Min support score: [{args.min_support}]).")
print(f"* Writing results to {out}/")


###################################################################################################
# Process start

# Read data from file or performs a delta blast.
if args.file:
    dblast_data = deltablast.read_dblast_file(args.file)

elif args.protein:
    deltablast.do_dblast_query(args.protein)
    dblast_data = deltablast.read_dblast_file(f"{args.protein}.tsp")

# Selects rows with given identity score.
selected_data = select_data(dblast_data, "% identity", args.min_identity)

# Find proteins in uniProt, extract GO list and KEGG accession.
uniprot_data = uniprot.search_uniprot(selected_data["subject acc.ver"], ["go", "database(kegg)"])

# Accumulate GO data.
go_list = go.accumulate_go(uniprot_data['Gene ontology (GO)'])

# Finds KEGG accessions, extract description and ID.
kegg_list = kegg.search_kegg(uniprot_data["Cross-reference (kegg)"])

# Draw charts.
multi_pie.plot(go_list, kegg_list, args.min_support, args.min_identity, name, outfile)

webbrowser.open(f"{outfile}.html")
