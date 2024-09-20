import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Process directories for the pipeline.')

    # Required arguments
    parser.add_argument('-m', '--mode', type=str, required=True, help='Mode: mod_clean')
    parser.add_argument('--pipeline_dir', type=str, required=True, help='Pipeline directory')

    # Optional arguments with default values
    parser.add_argument('--workflow_dir', type=str, default='workflows', help='Workflow directory (default: workflows)')
    parser.add_argument('--subworkflow_dir', type=str, default='subworkflows',
                        help='Subworkflow directory (default: subworkflows)')
    parser.add_argument('--module_dir', type=str, default='modules', help='Module directory (default: modules)')

    return parser.parse_args()