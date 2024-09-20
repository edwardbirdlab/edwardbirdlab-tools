import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(description='This provides sever tools for cleaning nextflow pipelines')

    # Required arguments
    parser.add_argument('-m', '--mode', type=str, required=True, help='Mode: mod_clean, get_cont')
    parser.add_argument('--pipeline_dir', type=str, required=True, help='Pipeline directory')

    # Optional arguments with default values
    parser.add_argument('--workflow_dir', type=str, default='workflows', help='Workflow directory (default: workflows)')
    parser.add_argument('--subworkflow_dir', type=str, default='subworkflows',
                        help='Subworkflow directory (default: subworkflows)')
    parser.add_argument('--module_dir', type=str, default='modules', help='Module directory (default: modules)')
    parser.add_argument('-o', '--output', type=str, help='Output file Path')

    args = parser.parse_args()

    # Set the default for -o if it was not provided
    if args.output is None:
        args.output = os.path.join(args.pipeline_dir, 'containers.csv')

    return args
