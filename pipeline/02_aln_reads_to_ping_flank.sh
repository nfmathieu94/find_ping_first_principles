#!/bin/bash -l

module load minimap2
module load samtools

FASTA=ping_flank/left_flank_Ping.fa
FASTQ_p1=heg4_fastq/HEG4_2.1_p1.fq.gz
FASTQ_p2=heg4_fastq/HEG4_2.1_p2.fq.gz
ALN_DIR=01_aln_out/heg4_reads_to_Ping_flank

SAM_FILE_p1=heg4_onlyPing_p1
SAM_FILE_p2=heg4_onlyPing_p2
BAM_FILE_p1=heg4_to_ping_match_only_p1
BAM_FILE_p2=heg4_to_ping_match_only_p2

PILEUP_OUT=02_pileup_out

# Indexing fasta with Ping subsequence
samtools faidx $FASTA

# Align HEG4 WGS short reads to Ping subsequence
minimap2 -a -x sr $FASTA $FASTQ_p1 -t 24 -o $ALN_DIR/$SAM_FILE_p1.sam
minimap2 -a -x sr $FASTA $FASTQ_p2 -t 24 -o $ALN_DIR/$SAM_FILE_p2.sam

# Create BAM files from alignment that have unaligned reads removed
samtools view -F 4 $ALN_DIR/$SAM_FILE_p1.sam -o $ALN_DIR/$BAM_FILE_p1.bam
samtools view -F 4 $ALN_DIR/$SAM_FILE_p2.sam -o $ALN_DIR/$BAM_FILE_p2.bam

# Sort and index bam files
samtools sort $ALN_DIR/$BAM_FILE_p1.bam -o $ALN_DIR/$BAM_FILE_p1.sort.bam
samtools sort $ALN_DIR/$BAM_FILE_p2.bam -o $ALN_DIR/$BAM_FILE_p2.sort.bam

samtools index $ALN_DIR/$BAM_FILE_p1.sort.bam
samtools index $ALN_DIR/$BAM_FILE_p2.sort.bam

# Run pileup to visualize mPing and Ping reads (optional step)
samtools mpileup $ALN_DIR/$BAM_FILE_p1.sort.bam --reference $FASTA -o $PILEUP_OUT/$SAM_FILE_p1.pileup.out
samtools mpileup $ALN_DIR/$BAM_FILE_p2.sort.bam --reference $FASTA -o $PILEUP_OUT/$SAM_FILE_p2.pileup.out
