#!/bin/bash -l

cd 04_aln_to_genome_out

# Concatenate all SAM files, remove header lines, extract fields 3 and 4, and add file name as the last column
for file in *.sam; do
    grep -v "^@" "$file" | cut -f 3,4 | awk -v file="$file" '{print $0"\t"file}'
done | sort -k 1n -k 2n > combined_read_locations_with_filenames.tsv

