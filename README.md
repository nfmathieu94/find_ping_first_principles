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
        - ```/rhome/nmath020/wessler_bigdata/rice/parental/HEG4/00_trim/trimmed/```

## Alignment

Start interactive job

```bash
srun --partition=batch --mem=40gb --cpus-per-task 8 --ntasks 1 --time 06:00:00 --pty bash -l
```

All code was ran in head working directory (find_ping_first_principles)

### mPing to Ping

Commands to look at alignment between ping and mping  
    - Can see the SNP at base 16  
    - Ran in head directory (find_ping_first_principles)  

```bash
bash pipeline/01_run_mping_ping_aln.sh
```

### Ping Flanking Sequence

The flanking sequence was obtained by looking at the alignment file above and selecting the 100 bp that  
contains the SNP the differs between Ping and mPing.  

### HEG4 Short Reads to Ping

Aligning HEG4 whole genome short reads to Ping substring containing SNP. 
Right now this is aligning _p1 and _p2 fastq files separately (might want to rethink this later?)

The following script:
    1. Indexes left flanking sequence (manually selected from 01_run_mping_ping_aln.sh output)
    2. Aligns HEG4 short reads to left flanking sequence that contains SNP
    3. Creates bam file that has unaligned reads removed
    4. Sorts bam files
    5. Indexes bam files
    6. Creates pipleup output (optional for visualization)

```bash
bash pipeline/02_aln_reads_to_ping_flank.sh
```

Looking at alignment of reads against left flanking Ping sequence (optional):   

```bash
samtools tview 01_aln_out/heg4_reads_to_Ping_flank/heg4_to_ping_match_only_p1.sort.bam --reference ping_flank/left_flank_Ping.fa
```


## Parsing SAM file

 Want to filter alined reads  
  1. Keep reads that contain Ping SNP  
  2. Only keep portion of read that belongs to the sequence flanking Ping to the left (soft clipped regions to the left)  
  3. Use paired read if the mate maps to genomic sequence
         - Need to work on this - NM 4.5.24


Ran this code to create fastq files with reads that belong to Ping and are trimmed to only have left flanking Ping region

```bash
python pipeline/03_get_trimmed_ping_reads.py 01_aln_out/heg4_reads_to_Ping_flank/heg4_to_ping_match_only_p1.sort.bam 03_filtered_reads/filtered_reads_p1.bam A 16
python pipeline/03_get_trimmed_ping_reads.py 01_aln_out/heg4_reads_to_Ping_flank/heg4_to_ping_match_only_p2.sort.bam 03_filtered_reads/filtered_reads_p2.bam A 16
```

Can run this for argument descriptions for python code:

```bash
python pipeline/03_get_trimmed_ping_reads.py --help
```

Then move .fastq files manually (need to fix above code so we don't have to do this) 

```bash
mv *.fastq 04_aln_to_genome_out 
```

- Not sure if we need right flanking information? - NM 4.5.24 

## Aligning Subreads To Reference Genome

The following script does:  
    1. Indexes reference genome  
    2. Aligns left flank p1 reads to genome (gives left p1 sam file)  
    3. Aligns left flank p2 reads to genome (gives left p2 sam file)  
    4. Aligns right flank p1 reads to genome (gives right p1 sam file)
    5. Aligns right flank p2 reads to genome (gives right p2 sam file)

Currently this is using bwa aln since processed subreads can be very short  
    - Should think about other tools and parameters to include  

```bash
bash pipeline/04_align_reads_to_genome.sh
```

Create concatenated file that has all read mapping locations:

```bash
bash pipeline/05_concat_read_locations.sh 
```

The above code creates this file:
04_aln_to_genome_out/combined_read_locations_with_filenames.tsv

### Validating Results

Compare all read mapping positions in concatenated file to the 7 known HEG4 ping locations.  
The known HEG4 locations are found here:

```
known_ping_loc/heg4_pings.csv
```

------------------------------


### Issues + Up next

The fastq files do appear to have trimmed reads, but many of the entries have no reads  
    - Think this is an issue when slicing the read string using the soft clipped value??  


Known ping locations are not being recovered using this current pipeline. - NM 4.9.2024

