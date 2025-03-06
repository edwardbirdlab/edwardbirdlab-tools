import os
import gzip
from tqdm import tqdm

def open_fastq(file_path):
    """Open a FASTQ file, handling both gzipped and uncompressed files."""
    if file_path.endswith(".gz"):
        return gzip.open(file_path, "rt")  # Open as text mode
    else:
        return open(file_path, "r")  # Open normally

def remove_duplicate_reads(input_fastq, output_fastq):
    seen_reads = set() # keeping track of the reads we have observed
    duplicate_count = 0  # Track number of duplicates
    total_reads = 0  # Track the total number of reads processed
    total_size = os.path.getsize(input_fastq)  # Get file size for progress tracking, this does not really work well....

    with open_fastq(input_fastq) as infile, open(output_fastq, "w") as outfile, tqdm(
        total=total_size, unit="B", unit_scale=True, desc="Processing Fastq - This bar is probably inaccurate:" # setting up the progess bar, dosent work well, but at least shows its running....
    ) as pbar:
        while True:
            pos = infile.tell()  # Get current file position for progress tracking
            header = infile.readline().strip()
            if not header:
                break  # End of file

            sequence = infile.readline().strip()
            plus = infile.readline().strip()
            quality = infile.readline().strip()

            read_name = header  # Extract read identifier
            total_reads += 1  # Increment total reads processed

            if read_name not in seen_reads:
                seen_reads.add(read_name)
                outfile.write(f"{header}\n{sequence}\n{plus}\n{quality}\n")
            else:
                duplicate_count += 1  # Count duplicates

            # Update progress
            if input_fastq.endswith(".gz"):
                pbar.update((len(header) + len(sequence) + len(plus) + len(quality)) / 6)  # Approximate uncompressed progress
            else:
                pbar.update(infile.tell() - pos)  # Accurate for uncompressed files

    # Calculate the percentage of removed reads
    if total_reads > 0:
        removal_percentage = (duplicate_count / total_reads) * 100
    else:
        removal_percentage = 0

    print(f"Finished processing. Removed {duplicate_count} duplicate reads.")
    print(f"Percentage of removed reads: {removal_percentage:.2f}%")

def process_remove_reads(input_fastq, output_fastq):
    remove_duplicate_reads_new(input_fastq, output_fastq)