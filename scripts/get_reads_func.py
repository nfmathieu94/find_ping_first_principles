# Want to fix so prefix of input_file is incorporated in output file
def get_reads(input_file, output_file, snp_nt, snp_pos):
    bam_file_input = pysam.AlignmentFile(input_file, "rb")
    filtered_reads_bam = pysam.AlignmentFile(output_file, "wb", header=bam_file_input.header)

    for read in bam_file_input:
        if read.seq[snp_pos - 1] == snp_nt:  # Assuming 1-based indexing, need to check this
            filtered_reads_bam.write(read)

    bam_file_input.close()
    filtered_reads_bam.close()

    print(f'Filtered read file {output_file} created')

    # Index the output BAM file
    pysam.index(output_file)

    print(f'Index file for {output_file} created')

# Want to add p1 or p2 in fastq output name
def extract_soft_clipped_sequences(read, left_flank_fastq, right_flank_fastq):
    left_flank_seq = ''
    right_flank_seq = ''
    left_flank_qual = ''
    right_flank_qual = ''
    read_pos = 0

    for operation, length in read.cigartuples:
        if operation == 4:  # Soft clipping
            if read.is_reverse:  # Check if the read is aligned to the reverse strand
                left_flank_seq += read.query_sequence[-length:]  # Extract soft-clipped portion from the end
                left_flank_qual += ''.join(chr(q + 33) for q in read.query_qualities[-length:])
            else:
                right_flank_seq += read.query_sequence[:length]  # Extract soft-clipped portion from the beginning
                right_flank_qual += ''.join(chr(q + 33) for q in read.query_qualities[:length])
        elif operation == 0:  # Match or Mismatch
            read_pos += length
        elif operation in [1, 2, 7, 8]:  # Insertion, Deletion, Soft clip on the right, Soft clip on the left
            read_pos += length

    left_flank_fastq.write(f"@{read.query_name}_left\n{left_flank_seq}\n+\n{left_flank_qual}\n")
    right_flank_fastq.write(f"@{read.query_name}_right\n{right_flank_seq}\n+\n{right_flank_qual}\n")


