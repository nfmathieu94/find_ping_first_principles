#!/bin/bash -l

module load fasta


TE_LIB=lib
OUTDIR=01_aln_out/mping_to_ping

# Run alignment between mPing and Ping 
# The 100 bp region containing SNP was manually selected to create fasta file 
fasta36 -f -a -3 -O $OUTDIR/mping_to_ping_aln.out $TE_LIB/mping.fa $TE_LIB/ping.fa

