import pysam

bam_file_path = "01_aln_out/heg4_reads_to_Ping_flank/heg4_to_ping_match_only_r1.sort.bam"

bam_file = pysam.AlignmentFile(bam_file_path, "rb")

left_flank_seq = ''
right_flank_seq = ''
left_flank_qual = ''
right_flank_qual = ''
read_pos = 0

for read in bam_file:
#    print(read)
    for operation, length in read.cigartuples:
#        print(operation, length)
        if operation == 4:
            print(operation, length)
            left_flank_seq += read.query_sequence[:(length - 1)]
    print(read)
    print(left_flank_seq)
    break

#for operation, length in read.cigartuples:
#    if operation == 4:  # Soft clipping
        # Need to think about the right way to slice out the portion of the read
#        left_flank_seq += read.query_sequence[:length]
#        right_flank_seq += read.query_sequence[read_pos:read_pos + length]
#        left_flank_qual += ''.join(chr(q + 33) for q in read.query_qualities[read_pos:read_pos + length])
#        right_flank_qual += ''.join(chr(q + 33) for q in read.query_qualities[read_pos:read_pos + length])
#    elif operation == 0:  # Match or Mismatch
#    read_pos += length
#    elif operation in [1, 2, 7, 8]:  # Insertion, Deletion, Soft clip on the right, Soft clip on the left
#        read_pos += length

#left_flank_fastq.write(f"@{read.query_name}_left\n{left_flank_seq}\n+\n{left_flank_qual}\n")
#right_flank_fastq.write(f"@{read.query_name}_right\n{right_flank_seq}\n+\n{right_flank_qual}\n")


