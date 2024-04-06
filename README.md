# Purpose

Finding Ping but starting with first principles  

1. Align mPing to Ping  
    - Find region that contains the left flanking SNP  
2. Align WGS reads for HEG4 to region that contains the SNP  
3. Filter reads based on SNP  
4. Trim reads to only keep portion that flanks Ping to the left  
5. Align these new reads to the reference genome  
6. See if Ping sites are recovered  

## Fastq

HEG4 fastq data is being used to test finding ping because we know the locations  
    - Reads were trimmed using fastp in previous project  
        * /rhome/nmath020/wessler_bigdata/rice/parental/HEG4/00_trim/trimmed/

## Alignment

### mPing to Ping

Commands to look at alignment between ping and mping  
    - Can see the SNP at base 16  
    - Ran in head directory (first_principles)  

module load fasta  
fasta36 -f -a -3 -O aln_out/mping_to_ping/mping_ping_aln.out lib/elements/mping.fa  lib/elements/ping.fa  

### Ping Flanking Sequence

The flanking sequence was obtained by looking at the alignment file above and selecting the 100 bp that  
contains the SNP the differs between Ping and mPing.  

### HEG4 Short Reads to Ping

module load minimap2  
minimap2 -a  -x sr fasta/left_flank_Ping.fa fastq/HEG4_2.1_p1.fq.gz -t 24 -o 01_aln_out/heg4_reads_to_Ping_flank/heg4_onlyPing_r2.sam  
minimap2 -a  -x sr fasta/left_flank_Ping.fa fastq/HEG4_2.1_p2.fq.gz -t 24 -o 01_aln_out/heg4_reads_to_Ping_flank/heg4_onlyPing_r2.sam  

### Filtering unaligned reads and making pileup of reads to Flanking Ping Sequence

Sort flanking Ping sequence is fasta directory:  
module load samtools  
samtools faidx left_flank_Ping.fa  

Create bam file with unaligned reads removed in 01_aln_out/heg4_reads_to_Ping_flank directory:  
samtools view -F 4 01_aln_out/heg4_reads_to_Ping_flank/heg4_onlyPing_r1.sam -OBAM -o 01_aln_out/heg4_reads_to_Ping_flank/heg4_to_ping_match_only_r1.bam  
samtools view -F 4 01_aln_out/heg4_reads_to_Ping_flank/heg4_onlyPing_r2.sam -OBAM -o 01_aln_out/heg4_reads_to_Ping_flank/heg4_to_ping_match_only_r2.bam  

Sort and index sorted bam file in 01_aln_out/heg4_reads_to_Ping_flank directory:  
samtools sort 01_aln_out/heg4_reads_to_Ping_flank/heg4_to_ping_match_only_r1.bam -o 01_aln_out/heg4_reads_to_Ping_flank/heg4_to_ping_match_only_r1.sort.bam  
samtools sort 01_aln_out/heg4_reads_to_Ping_flank/heg4_to_ping_match_only_r2.bam -o 01_aln_out/heg4_reads_to_Ping_flank/heg4_to_ping_match_only_r2.sort.bam  

samtools index 01_aln_out/heg4_reads_to_Ping_flank/heg4_to_ping_match_only_r1.sort.bam  
samtools index 01_aln_out/heg4_reads_to_Ping_flank/heg4_to_ping_match_only_r2.sort.bam  

Looking at alignment of reads against left flanking Ping (optional):  
    - A way to visualize alignment  
samtools tview aln_out/heg4_reads_to_Ping_flank/heg4_to_ping_match_only_r1.sort.bam --reference aln_out/mping_to_ping/left_flank_Ping.fa  

Creating mPileup file to see difference in basepairs for each read (optional):  
    - A way to check that Ping and mPing reads are being captured  
    - Expect to see more of the mPing SNP (G at position 16) compared to Ping SNP (A at position 16)  
 
 samtools mpileup 01_aln_out/heg4_reads_to_Ping_flank/heg4_to_ping_match_only_r1.sort.bam --reference fasta/left_flank_Ping.fa -o 02_pileup/heg4_to_ping_r1.pileup.out  
 samtools mpileup 01_aln_out/heg4_reads_to_Ping_flank/heg4_to_ping_match_only_r2.sort.bam --reference fasta/left_flank_Ping.fa -o 02_pileup/heg4_to_ping_r2.pileup.out  

### Parsing SAM file

 Want to filter alined reads  
  1. Keep reads that contain Ping SNP  
  2. Keep Ping reads that have genomic information (soft clipped regions to the left)  
      - Need to think about cutoffs we want to use  
  3. Use paired reads if the pair maps to genomic sequence  




### Parsing SAM file

 Want to filter alined reads  
  1. Keep reads that contain Ping SNP  
  2. Keep Ping reads that have genomic information (soft clipped regions to the left)  
      - Need to think about cutoffs we want to use  
  3. Use paired reads if the pair maps to genomic sequence  



python scripts/main_test.py 01_aln_out/heg4_reads_to_Ping_flank/heg4_to_ping_match_only_r1.sort.bam 03_filtered_reads/filtered_reads_r1.bam A 16  
python scripts/main_test.py 01_aln_out/heg4_reads_to_Ping_flank/heg4_to_ping_match_only_r2.sort.bam 03_filtered_reads/filtered_reads_r2.bam A 16  

- Had to rename the fastq files to include p1 and p2 in the name (want to fix this later)  
- Not sure if we need right flanking information?  

### Issues + Up next

The fastq files do appear to have trimmed reads, but many of the entries have no reads  
    - Think this is an issue when slicing the read string using the soft clipped value??  

Going to try to align these filtered and trimmed reads to the genome and see what happens  
    - Need to figure out the best tool and settings to find all possible locations for short read substrings  

Also want to put the above command line steps in a bash script 
