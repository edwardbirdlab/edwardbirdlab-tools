#!/usr/bin/env python3

import os
import gzip
import csv
import pandas as pd
from tqdm import tqdm
from Bio.Seq import Seq

def open_fasta(file_path):
    return gzip.open(file_path, "rt") if file_path.endswith(".gz") else open(file_path, "r")

def analyze_orf(seq):
    START_CODON = "ATG"
    STOP_CODONS = {"TAA", "TAG", "TGA"}
    seq = str(seq)
    has_start = seq.startswith(START_CODON)
    has_stop = seq[-3:] in STOP_CODONS if len(seq) >= 3 else False

    if has_start:
        internal_stop = any(seq[i:i+3] in STOP_CODONS for i in range(3, len(seq) - 6, 3))
        return {"start_codon": True, "ends_with_stop": has_stop, "internal_stop_codons": internal_stop, "inferred_reading_frame": 1}
    elif has_stop:
        for frame in range(3):
            frame_seq = seq[frame:-3]
            codons = [frame_seq[i:i+3] for i in range(0, len(frame_seq) - 2, 3)]
            if all(codon not in STOP_CODONS for codon in codons):
                return {"start_codon": False, "ends_with_stop": has_stop, "internal_stop_codons": False, "inferred_reading_frame": frame + 1}
        return {"start_codon": False, "ends_with_stop": False, "internal_stop_codons": "Cannot determine", "inferred_reading_frame": 'N/A'}
    else:
        for frame in range(3):
            frame_seq = seq[frame:]
            codons = [frame_seq[i:i+3] for i in range(0, len(frame_seq) - 2, 3)]
            if all(codon not in STOP_CODONS for codon in codons):
                return {"start_codon": False, "ends_with_stop": False, "internal_stop_codons": False, "inferred_reading_frame": frame + 1}
        return {"start_codon": False, "ends_with_stop": False, "internal_stop_codons": "Cannot determine", "inferred_reading_frame": 'N/A'}

def fasta_generator(handle):
    header = None
    seq_lines = []
    for line in handle:
        line = line.strip()
        if line.startswith(">"):
            if header:
                yield header, "".join(seq_lines)
            header = line[1:]
            seq_lines = []
        else:
            seq_lines.append(line)
    if header:
        yield header, "".join(seq_lines)

def main(fasta, report, output):
    hamr_df = pd.read_csv(report, sep="\t")
    name_breaks = ['_allclass', '_scaffolds']
    seqs = set(hamr_df['input_sequence_id'])
    seqs.update(hamr_df['input_sequence_id'].apply(lambda x: x.rsplit("_", 1)[0]))

    total_size = os.path.getsize(fasta)

    with open_fasta(fasta) as infile, open(output, "w", newline="") as outfile, tqdm(
        total=total_size, unit="B", unit_scale=True, desc="Processing FASTA"
    ) as pbar:
        writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow([
            "samplename", "tool", "produced_orf", "gene_symbol", "coverage", "sequence_identity",
            "3'Start", "5'Stop", "3'_at_seq_end", "start_pos", "5'_at_seq_end", "end_pos",
            "total_len_queryseq", "sense", "Internal_stops", "Reading_Frame",
            "antimicrobial_agent", "drug_class", "input_sequence_id",
            "Reported_Sequence", "ORF", "Protein"
        ])

        for header, sequence in fasta_generator(infile):
            pos = infile.tell()
            read_name = header

            if read_name in seqs:
                subset_df = hamr_df[hamr_df['input_sequence_id'].apply(lambda x: x.startswith(read_name))]
                for _, row in subset_df.iterrows():
                    start = int(row['input_gene_start']) - 1
                    stop = int(row['input_gene_stop']) - 1
                    strand = row['strand_orientation']
                    full_len = len(sequence)

                    if strand == '-':
                        current_cd = Seq(sequence[start:stop]).reverse_complement()
                        Read_end = start <= 2
                        Read_start = (full_len - stop) <= 3
                    else:
                        current_cd = Seq(sequence[start:stop])
                        Read_start = start <= 2
                        Read_end = (full_len - stop) <= 3

                    result = analyze_orf(current_cd)

                    if result['inferred_reading_frame'] in [1, 2, 3]:
                        frame = int(result['inferred_reading_frame']) - 1
                        cd_seq = str(current_cd)[frame:]
                        cd_seq = cd_seq[:len(cd_seq) - len(cd_seq) % 3] if len(cd_seq) % 3 != 0 else cd_seq
                    else:
                        cd_seq = 'N/A'

                    if cd_seq != 'N/A':
                        dna_seq = Seq(cd_seq)
                        protein_seq = dna_seq.translate()
                        real_orf = len(cd_seq) >= 0.8 * len(current_cd)
                    else:
                        protein_seq = 'N/A'
                        real_orf = False

                    sample_name = row['input_file_name']
                    for break_str in name_breaks:
                        if sample_name.endswith(break_str):
                            sample_name = sample_name[:-len(break_str)]

                    writer.writerow([
                        sample_name,
                        row['reference_database_name'],
                        real_orf,
                        row['gene_symbol'],
                        row['coverage_percentage'],
                        row['sequence_identity'],
                        result['start_codon'],
                        result['ends_with_stop'],
                        Read_start,
                        start + 1,
                        Read_end,
                        stop + 1,
                        len(sequence),
                        strand,
                        result['internal_stop_codons'],
                        result['inferred_reading_frame'],
                        row['antimicrobial_agent'],
                        row['drug_class'],
                        read_name,
                        str(current_cd),
                        cd_seq,
                        str(protein_seq)
                    ])

            if fasta.endswith(".gz"):
                pbar.update((len(header) + len(sequence)) / 6)
            else:
                pbar.update(infile.tell() - pos)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Process FASTA + HAMR report to extract and validate ORFs.")
    parser.add_argument("--fasta", required=True, help="Input FASTA file (can be .gz)")
    parser.add_argument("--report", required=True, help="HAMR report TSV file")
    parser.add_argument("--output", required=True, help="Output CSV file path")
    cli_args = parser.parse_args()
    main(cli_args.fasta, cli_args.report, cli_args.output)