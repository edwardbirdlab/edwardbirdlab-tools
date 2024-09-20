from nf_parse_tools.mod_clean import whole_process as module_clean
from nf_parse_tools.arg_parse import parse_args


def main():
    # Parse the arguments
    args = parse_args()

    # Use the parsed arguments
    tool_mode = args.mode
    pipeline_dir = args.pipeline_dir
    workflow_dir = args.workflow_dir
    subworkflow_dir = args.subworkflow_dir
    module_dir = args.module_dir

    if tool_mode == 'mod_clean':
        module_clean(pipeline_dir, workflow_dir, subworkflow_dir, module_dir)


if __name__ == "__main__":
    main()