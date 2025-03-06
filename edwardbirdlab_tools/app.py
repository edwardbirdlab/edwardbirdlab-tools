from edwardbirdlab_tools.ebird_tools.mod_clean import whole_process as module_clean
from edwardbirdlab_tools.ebird_tools.arg_parse import parse_args
from edwardbirdlab_tools.ebird_tools.get_containers import get_contaienrs
from edwardbirdlab_tools.ebird_tools.screen_duplicated_fastq import process_remove_reads


def main():
    # Parse the arguments
    args = parse_args()

    #

    # Use the parsed arguments
    tool_mode = args.mode

    if tool_mode == 'mod_clean':
        #Getting ARGs
        pipeline_dir = args.pipeline_dir
        workflow_dir = args.workflow_dir
        subworkflow_dir = args.subworkflow_dir
        module_dir = args.module_dir
        #Calling Module
        module_clean(pipeline_dir, workflow_dir, subworkflow_dir, module_dir)
    if tool_mode == 'get_conts':
        pipeline_dir = args.pipeline_dir
        module_dir = args.module_dir
        output = args.output
        get_contaienrs(pipeline_dir, module_dir, output)
    if tool_mode == 'fastq_dupfilt':
        input = args.input
        output = args.output
        process_remove_reads(input, output)
    else:
        print('Error: tool_mode must be "mod_clean", "get_conts", or "fastq_dupfilt"')


if __name__ == "__main__":
    main()