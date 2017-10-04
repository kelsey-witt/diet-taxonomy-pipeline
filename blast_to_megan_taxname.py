#!/usr/bin/env python

"""
This script is designed to take a blast .tab output file and process it into a format that is readable by 
MEGAN without the need for an outside taxonomy database. It uses 3 inputs: your blast file, a datafile that
assigns taxids to each accession, and a datafile that assigns scientific names to each taxid. Both datafiles are
accessible from ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/ (accession2taxid and taxdmp.zip),and it is recommended 
that the user downloads updated versions of these files (ncbi updates them regularly) whenever a new database is
created/used to ensure that all taxids are represented.

The blast input file should be in tabular format. The file must contain the read id, the accession number the read 
matched to, and the bitscore for MEGAN to process it correctly. The format that the script is written for is outfmt
8, but any tabular format with the above pieces of data will work (just revise the regex line in blast_hit_parse).

The datafiles have been processed for ease of access here. The accession2taxid file is just the accession
version and the taxid, separated by tabs, and the script accession_trimmer.py can do this for you. The names.dmp file
is just the taxid and the scientific name, separated by tabs, and you can do this using names_streamliner.py. Note that
the script leaves a few extra tabs and | dividers at the end, so I recommend removing them using a text editor with
regex capabilities
"""

import sys
import re
import csv

inFile = sys.argv[1] 

SeqIDs = []
Accessions = [] 
Bitscores = [] 
TaxIDs = []
Accessions_in_db = []

Acc_to_Tax = dict() 
TaxID_to_name = dict()
Acc_to_Sciname = dict()

acc_linecount = 0
names_linecount = 0

with open(inFile, 'r')as f: 
	for blast_line in f:
		blast_hit_parse = re.search(r"^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+(\S+).*", blast_line) #pulls out sequence ID, accession, % identity, length, and bit score 
		seqid = blast_hit_parse.group(1)
		acc = blast_hit_parse.group(2)
		pident = blast_hit_parse.group(3)
		match_len = blast_hit_parse.group(4)
		bitscore = blast_hit_parse.group(5)
		if pident >= 100.0 and match_len >= 75: #If a blast hit has > 100% match and > 75 bp length (otherwise, discard)
			SeqIDs.append(seqid) 
			Accessions.append(acc) 
			Bitscores.append(bitscore) 

Accession_set = set(Accessions) 

with open("nucl_gb.accession2taxid_AccTax.map", 'r')as f: 
	for acc_tax_line in f: 
		a = re.search(r"^(\S+)\s+(\S+).*", acc_tax_line) 
		accession_version = a.group(1) 
		taxid = a.group(2)
		if accession_version in Accession_set: 
			Acc_to_Tax[accession_version] = taxid 
			TaxIDs.append(taxid) 
#		if acc_linecount % 10000000  == 0:
#			print "Working on Accession line number %d" % (acc_linecount)
#		acc_linecount += 1
 
TaxIDs_set = set(TaxIDs) #makes a set of TaxIDs for faster processing
with open("names_streamlined.txt", 'r')as f: 
	for name_line in f: 
		a = re.search(r"^(\S+)\s+(.*)", name_line) 
		taxid = a.group(1) 
		sci_name = a.group(2)
		if taxid in TaxIDs_set: 
			TaxID_to_name[taxid] = sci_name 
#		if names_linecount % 1000000  == 0:
#			print "Working on Name line number %d" % (names_linecount)
#		names_linecount += 1

for acc_num in Accession_set:
	if acc_num in Acc_to_Tax.keys() and Acc_to_Tax[acc_num] in TaxID_to_name.keys():
		Accessions_in_db.append(acc_num)

for acc_num in Accessions_in_db: 
	Acc_to_Sciname[acc_num] = TaxID_to_name[Acc_to_Tax[acc_num]] 

output_file=inFile[0:-4]+".megan.csv" 
print output_file
with open(output_file, 'wb') as csvfile: 
	w = csv.writer(csvfile, delimiter=',')
	for seqnum in range(0,len(SeqIDs)): 
		if Accessions[seqnum] in Acc_to_Sciname.keys():
			file_row=[] #format: seqid, scientific name, bitscore
			file_row.append(SeqIDs[seqnum]) 
			file_row.append(Acc_to_Sciname[Accessions[seqnum]]) 
			file_row.append(Bitscores[seqnum]) 
			w.writerow(file_row) 
