import argparse
import pysam
import os

def get_reads(input_file, output_file, snp_nt, snp_pos):
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Create output directory if it doesn't exist
        bam_file_input = pysam.AlignmentFile(input_file, "rb")
        filtered_reads_bam = pysam.AlignmentFile(output_file, "wb", header=bam_file_input.header)

        for read in bam_file_input:
            if read.seq[snp_pos - 1] == snp_nt:
                filtered_reads_bam.write(read)

        bam_file_input.close()
        filtered_reads_bam.close()

        print(f'Filtered read file {output_file} created')

        # Index the output BAM file
        pysam.index(output_file)

        print(f'Index file for {output_file} created')
    except Exception as e:
        print(f"Error: {e}")

def extract_soft_clipped_sequences(read, left_flank_fastq, right_flank_fastq, prefix):
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

    left_flank_fastq.write(f"@{prefix}_left\n{left_flank_seq}\n+\n{left_flank_qual}\n")
    right_flank_fastq.write(f"@{prefix}_right\n{right_flank_seq}\n+\n{right_flank_qual}\n")

def main():
    parser = argparse.ArgumentParser(description="Extract reads containing a specific SNP at a given position")
    parser.add_argument("input_file", type=str, help="Input BAM file containing aligned reads")
    parser.add_argument("output_file", type=str, help="Output BAM file containing reads of interest")
    parser.add_argument("snp_nt", type=str, help="Specific nucleotide of interest (A, C, G, or T)")
    parser.add_argument("snp_pos", type=int, help="Position in read where SNP occurs (1-based)")

    args = parser.parse_args()

    # Extracting prefix from input file name
    input_prefix = os.path.splitext(os.path.basename(args.input_file))[0]

    get_reads(args.input_file, args.output_file, args.snp_nt, args.snp_pos)

    bam_file = pysam.AlignmentFile(args.output_file, "rb")

    # Modifying output file names based on 'p1' or 'p2'
    if 'p1' in input_prefix:
        left_output = "left_flank_p1.fastq"
        right_output = "right_flank_p1.fastq"
    elif 'p2' in input_prefix:
        left_output = "left_flank_p2.fastq"
        right_output = "right_flank_p2.fastq"
    else:
        left_output = "left_flank.fastq"
        right_output = "right_flank.fastq"

    left_flank_fastq = open(left_output, "w")
    right_flank_fastq = open(right_output, "w")

    for read in bam_file:
        extract_soft_clipped_sequences(read, left_flank_fastq, right_flank_fastq, input_prefix)

    left_flank_fastq.close()
    right_flank_fastq.close()
    bam_file.close()

if __name__ == "__main__":
    main()

