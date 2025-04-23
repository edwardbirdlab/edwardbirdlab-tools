import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(description='This provides several tools I have made for different purposes')

    # Create subparsers for each mode (module)
    subparsers = parser.add_subparsers(dest='mode', help='Choose the mode of operation')

    # Subcommand for 'mod_clean'
    mod_clean_parser = subparsers.add_parser('mod_clean', help='Module for cleaning')
    mod_clean_parser.add_argument('--pipeline_dir', type=str, help='Pipeline directory', required=True)
    mod_clean_parser.add_argument('--workflow_dir', type=str, default='workflows', help='Workflow directory (default: workflows)')
    mod_clean_parser.add_argument('--subworkflow_dir', type=str, default='subworkflows', help='Subworkflow directory (default: subworkflows)')
    mod_clean_parser.add_argument('--module_dir', type=str, default='modules', help='Module directory (default: modules)')
    mod_clean_parser.add_argument('-o', '--output', type=str, help='Output file Path', required=True)

    # Subcommand for 'get_cont'
    get_cont_parser = subparsers.add_parser('get_conts', help='Get containers')
    get_cont_parser.add_argument('--pipeline_dir', type=str, help='Pipeline directory', required=True)
    get_cont_parser.add_argument('--module_dir', type=str, default='modules', help='Module directory (default: modules)')
    get_cont_parser.add_argument('-o', '--output', type=str, help='Output file Path', required=True)

    # Subcommand for 'fastq_dupfilt'
    fastq_dupfilt_parser = subparsers.add_parser('fastq_dupfilt', help='Filter duplicated reads due to concat errors. Takes a FastQ file, uncompressed or in gzip format')
    fastq_dupfilt_parser.add_argument('-i', '--input', type=str, help='input fastq', required=True)
    fastq_dupfilt_parser.add_argument('-o', '--output', type=str, help='output fastq name, Output will not be gzipped', required=True)

    # Subcommand for 'harm_analyze'
    harm_analyze_parser = subparsers.add_parser('harm_analyze', help='Filter duplicated reads due to concat errors. Takes a FastQ file, uncompressed or in gzip format')
    harm_analyze_parser.add_argument('-s', '--seqs', type=str, help='input sequence fasta/fasta.gz', required=True)
    harm_analyze_parser.add_argument('-r', '--report', type=str, help='input hamronization report', required=True)
    harm_analyze_parser.add_argument('-o', '--output', type=str, help='output csv filename', required=True)

    args = parser.parse_args()

    return args
