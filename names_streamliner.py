import sys
import re

infile = sys.argv[1]

outfile = infile[:-4] + "_streamlined.txt"

with open(outfile, 'w') as g:
    with open(infile) as f:
        for line in f:
            if "scientific" in line:
                filter_taxid_sciname = re.search('(\d+)\t\|\t([^|\t]+)\t\|.+', line)
                taxid = filter_taxid_sciname.group(1)
                sciname = filter_taxid_sciname.group(2)
                newline = taxid + "\t" + sciname + "\n"
                g.write(newline)
