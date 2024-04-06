
# Function to get reads based on a SNP at certain position
def get_reads(input_file, output_file, snp_nt, snp_pos):
    bam_file_input = pysam.AlignmentFile(input_file, "rb")
    filtered_reads_bam = pysam.AlignmentFile(output_file, "wb", header=bam_file_input.header)

    for read in bam_file_input:
        if read.seq[snp_pos - 1] == snp_nt:  # Assuming 1-based indexing
            filtered_reads_bam.write(read)

    bam_file_input.close()
    filtered_reads_bam.close()

    print(f'Filtered read file {output_file} created')

# Function to get flanking (soft clipped) reads
def extract_flanking_sequences(read, reference, left_flank_file, right_flank_file):
    left_flank = ''
    right_flank = ''
    ref_pos = read.reference_start
    read_pos = 0

    for operation, length in read.cigartuples:
        if operation == 4:  # Soft clipping
            left_flank += read.query_sequence[read_pos:read_pos + length]
            right_flank += reference[ref_pos:ref_pos + length]
        elif operation == 0:  # Match or Mismatch
            read_pos += length
            ref_pos += length
        elif operation in [1, 2, 7, 8]:  # Insertion, Deletion, Soft clip on the right, Soft clip on the left
            read_pos += length
        elif operation in [5, 6]:  # Hard clip, padding
            pass

    left_flank_file.write(f">{read.query_name}_left\n{left_flank}\n")
    right_flank_file.write(f">{read.query_name}_right\n{right_flank}\n")


