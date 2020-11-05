# diet-taxonomy-pipeline
### This pipeline is designed to identify taxa from BLAST results of metagenomic data, primarily to determine diet.

This workflow removes adapters, trims, and assembles raw metagenomic reads, performs a BLAST search of all reads against the nt (nucleotide) database, identifies the taxa present using MEGAN, and verifies the presence of those taxa using BLAST of individual DNA reads. The full workflow is outlined in Diet_Taxonomy_Pipeline_Instructions.txt, and all python scripts written for the workflow are included here.

To see the pipeline for analysis of the microbiome using this data, <link here>.

### Required Software
Sequence read processing
* [Clumpify](https://github.com/BioInfoTools/BBMap/blob/master/sh/clumpify.sh)
* [AdapterRemoval](https://github.com/MikkelSchubert/adapterremoval)
* [Fastx_toolkit](http://hannonlab.cshl.edu/fastx_toolkit/)
* [fastqtofasta.pl](https://github.com/PombertLab/Genomics/blob/master/FASTQtoFASTA.pl)
* [ABySS](https://github.com/bcgsc/abyss)

Taxon identification
* [blast+](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download)
* [MEGAN 6.0 Community Edition](https://software-ab.informatik.uni-tuebingen.de/download/megan6/welcome.html)
* Python3

Contact: Kelsey E. Witt (kelsey_witt_dillon@brown.edu)
