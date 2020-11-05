"""
This script was written by Kelsey Witt Dillon in November 2017. It is designed to take a blast tab file
and convert it to the csv format accepted by MEGAN6, filtering the data for length, percent identity,
and taxa it matches.

The input files needed are a custom blast tab file, the categories.dmp file from the NCBI Taxonomy ftp,
and a streamlined names file from the NCBI Taxonomy ftp. The blast tab file has the following columns:
query sequence ID, match sequence ID, query length, match length, percent match, bit score, match taxonomic
ID, match scientific name. The names file is streamlined to reduce excess information using names_streamliner.py
to make names_streamlined.txt
"""
import sys
import re
import csv

taxids = set()
species_level_taxids = {}
taxnames = {}
query = "null"
blast_hits = []
genus_set = set()

query_length_cutoff = sys.argv[2]
pident_cutoff = 100.00

taxid_check_infile = "../Projects/Coprolite_Diet_Construction/Tax_Reference_Files/categories.dmp"
taxnames_infile = "../Projects/Coprolite_Diet_Construction/Tax_Reference_Files/names_streamlined.txt"
blast_tab_infile = sys.argv[1]
megan_outfile = blast_tab_infile[0:-4] + "." + str(query_length_cutoff) + ".megan.csv"

def add_blast_info(line):
    read_name = line[0] 
    bitscore = line[5]
    if line[6] in species_level_taxids.keys():
        taxname = taxnames[species_level_taxids[line[6]]]
    else:
        taxname = line[7]
    blast_hits.append([read_name,taxname,bitscore])
    if re.match("(\S+)\s\S+.*", line[7]) is not None:
        genus_pull = re.search("(\S+)\s\S+.*", line[7])
        genus = genus_pull.group(1)
        genus_set.add(genus)
    else:
        genus_set.add("no_genus")

with open(blast_tab_infile) as f:
    for blast_line in f:
        blast_line = blast_line.strip()
        blast_line = blast_line.split("\t")
        taxid_raw = blast_line[6] 
        taxids.add(taxid_raw) 

with open(taxid_check_infile) as g:
    for tax_line in g:
        tax_line = tax_line.strip()
        tax_line = tax_line.split("\t")
        if tax_line[2] in taxids and tax_line[2] != tax_line[1]: #if one of the taxa in my list has a taxid lower than genus species
            species_level_taxids[tax_line[2]] = tax_line[1]

with open(taxnames_infile) as h:
    for name_line in h:
        name_line = name_line.strip()
        name_line = name_line.split("\t")
        if name_line[0] in species_level_taxids.values(): 
            taxnames[name_line[0]] = name_line[1] #key is taxid, value is taxname

with open(megan_outfile, 'w', newline='') as csvfile:
    w = csv.writer(csvfile, delimiter=",")
    with open(blast_tab_infile) as j:
        for blast2_line in j:
            blast2_line=blast2_line.strip()
            blast2_line = blast2_line.split("\t")
            if int(blast2_line[2]) == int(blast2_line[3]) and int(blast2_line[3]) >= int(query_length_cutoff) and float(blast2_line[4]) == float(pident_cutoff): #make these numbers variables
                if blast2_line[0] == query:
                    add_blast_info(blast2_line)
                else:
                    #print(genus_set)
                    if len(genus_set) == 1:
                        for hit in blast_hits:
                            write_line = hit
                            w.writerow(write_line)
                    query = blast2_line[0]
                    blast_hits = []
                    genus_set=set()
                    add_blast_info(blast2_line)
    #print(genus_set)
        if len(genus_set) == 1:
            for hit in blast_hits:
                write_line = hit
                w.writerow(write_line)