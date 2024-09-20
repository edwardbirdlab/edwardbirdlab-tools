from nf_parse_tools.mod_clean import whole_process as module_clean
from nf_parse_tools.arg_parse import parse_args
from nf_parse_tools.get_containers import get_contaienrs


def main():
    # Parse the arguments
    args = parse_args()

    # Use the parsed arguments
    tool_mode = args.mode
    pipeline_dir = args.pipeline_dir
    workflow_dir = args.workflow_dir
    subworkflow_dir = args.subworkflow_dir
    module_dir = args.module_dir
    output = args.output

    if tool_mode == 'mod_clean':
        module_clean(pipeline_dir, workflow_dir, subworkflow_dir, module_dir)
    if tool_mode == 'get_conts':
        get_contaienrs(pipeline_dir, module_dir, output)
    else:
        print('Error: tool_mode must be "mod_clean" or "get_conts"')


if __name__ == "__main__":
    main()