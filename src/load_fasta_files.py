from Bio import SeqIO

# # List of FASTA files to combine
fasta_files = [
    'hepatitis_b_part1.fasta', 'hepatitis_b_part2.fasta', 'hepatitis_b_part3.fasta', 'hepatitis_b_part4.fasta',
    'hepatitis_c_1.fasta', 'hepatitis_c_2.fasta', 'hepatitis_c_3.fasta',
    'hepatitis_d.fasta', 'hepatitis_e.fasta'
]

# Output file for combined sequences
output_file = "combined_hepatitis_sequences.fasta"

# Combine all FASTA files
with open(output_file, "w") as outfile:
    total_samples = 0
    for fasta_file in fasta_files:
        with open(fasta_file) as infile:
            for record in SeqIO.parse(infile, "fasta"):
                # Write each record in the required format
                outfile.write(f">{record.description}\n{str(record.seq)}\n")
                total_samples += 1

# Print total number of samples
print(f"Total number of samples: {total_samples}")


### Combining all virus fasta files
def combine_fasta_files(output_file, *input_files):
    with open(output_file, 'w') as out_fasta:
        for fasta_file in input_files:
            with open(fasta_file, 'r') as infile:
                for line in infile:
                    out_fasta.write(line)

# Example usage
input_files = ["covid.fasta", "dengue.fasta", "hepatitis.fasta", "influenza.fasta", "mers.fasta"]  # Replace with your actual file paths
output_file = "combined_data.fasta"  # This is the file where the combined data will be saved

combine_fasta_files(output_file, *input_files)

print(f"All FASTA files combined into {output_file}")


### Getting the total dataset size
def count_samples_in_fasta(file_path):
    count = 0
    with open(file_path, 'r') as fasta_file:
        for line in fasta_file:
            if line.startswith('>'):
                count += 1
    return count

# Example usage
fasta_file_path = "hepatitis2.fasta"  # Replace with your actual file path
total_samples = count_samples_in_fasta(fasta_file_path)
print(f"Total number of samples in {fasta_file_path}: {total_samples}")


### Combining all fasta files and also removing the duplicates
def combine_fasta_files_remove_duplicates(output_file, *input_files):
    sequences = set()  # Set to store unique sequences
    current_seq = []   # List to collect sequence lines
    current_header = None

    with open(output_file, 'w') as out_fasta:
        for fasta_file in input_files:
            with open(fasta_file, 'r') as infile:
                for line in infile:
                    line = line.strip()
                    if line.startswith(">"):  # It's a header line
                        if current_seq:
                            # Join the collected sequence lines and add to set
                            seq_str = ''.join(current_seq)
                            if seq_str not in sequences:
                                sequences.add(seq_str)
                                out_fasta.write(current_header + '\n')
                                out_fasta.write(seq_str + '\n')
                        # Reset for the new sequence
                        current_seq = []
                        current_header = line
                    else:
                        current_seq.append(line)
                
                # Process the last sequence in the file
                if current_seq:
                    seq_str = ''.join(current_seq)
                    if seq_str not in sequences:
                        sequences.add(seq_str)
                        out_fasta.write(current_header + '\n')
                        out_fasta.write(seq_str + '\n')

# Example usage
input_files = [
    'hepatitis_b_part1.fasta', 'hepatitis_b_part2.fasta', 'hepatitis_b_part3.fasta', 'hepatitis_b_part4.fasta',
    'hepatitis_c_1.fasta', 'hepatitis_c_2.fasta', 'hepatitis_c_3.fasta',
    'hepatitis_d.fasta', 'hepatitis_e.fasta'
]  # Replace with your actual file paths
output_file = "combined_hepatitis_data_no_duplicates.fasta"  # This is the file where the combined data will be saved

combine_fasta_files_remove_duplicates(output_file, *input_files)

print(f"All FASTA files combined into {output_file}, duplicates removed.")