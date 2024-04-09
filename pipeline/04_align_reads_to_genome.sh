#!/bin/bash -l

module load bwa


GENOME=ref_genome/MSU_r7.fa
FASTQ_DIR=03_filtered_reads
FASTQ_LEFT_P1=03_filtered_reads/left_flank_p1.fastq
FASTQ_LEFT_P2=03_filtered_reads/left_flank_p2.fastq
FASTQ_RIGHT_P1=03_filtered_reads/right_flank_p1.fastq
FASTQ_RIGHT_P2=03_filtered_reads/right_flank_p2.fastq
ALN_OUT=04_aln_to_genome_out

# Index reference genome

# Check if genome is indexed
if [ ! -f $GENOME.sa ]; then
  bwa index $GENOME
fi


# Aligning left flank p1 reads and make sam file
bwa aln $GENOME $FASTQ_LEFT_P1 > $ALN_OUT/left_flank_p1.sai
bwa samse $GENOME $ALN_OUT/left_flank_p1.sai $FASTQ_DIR/left_flank_p1.fastq > $ALN_OUT/left_flank_p1.sam


# Align left flank p2 reads and make sam file
bwa aln $GENOME $FASTQ_LEFT_P2 > $ALN_OUT/left_flank_p2.sai
bwa samse $GENOME $ALN_OUT/left_flank_p2.sai $FASTQ_DIR/left_flank_p2.fastq > $ALN_OUT/left_flank_p2.sam

# Align right flank p1 reads and make sam file
bwa aln $GENOME $FASTQ_RIGHT_P1 > $ALN_OUT/right_flank_p1.sai
bwa samse $GENOME $ALN_OUT/right_flank_p1.sai $FASTQ_DIR/right_flank_p1.fastq > $ALN_OUT/right_flank_p1.sam


# Align right flank p2 reads and make sam file
bwa aln $GENOME $FASTQ_RIGHT_P2 > $ALN_OUT/right_flank_p2.sai
bwa samse $GENOME $ALN_OUT/right_flank_p2.sai $FASTQ_DIR/right_flank_p2.fastq > $ALN_OUT/right_flank_p2.sam
