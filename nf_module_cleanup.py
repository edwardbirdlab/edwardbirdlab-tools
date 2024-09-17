#!/usr/bin/env python3

import os
import shutil
import argparse

def get_nf_files(folder):
    nf_files = []
    for entry in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, entry)) and entry.endswith('.nf'):
            nf_files.append(os.path.join(folder, entry))
        if os.path.isdir(os.path.join(folder, entry)):
            new_files = get_nf_files(os.path.join(folder, entry))
            for file in new_files:
                nf_files.append(file)
    return nf_files

def get_workflows(pipeline_dir, workflow_dir):
    nf_workflows = get_nf_files(pipeline_dir+ '/' + workflow_dir)
    print(pipeline_dir + ' contains these workflows: \n')
    for wf in nf_workflows:
        print(wf)
    return nf_workflows

def get_used_files(pipeline_dir, workflows):
    # Creating list to store subworkflows and modules that are used
    used_modules = []
    used_subworkflows = []
    
    for workflow in workflows:
        #print("Subworkflows in: " + workflow.split('\\')[-1])
        with open(workflow) as file:
            text = file.read().split('\n')
            for line in text:
                if line.split(' ')[0] == "include":
                    #print(line.split(' ')[-1])
                    subworkflow = line.split(' ')[-1][4:]
                    used_subworkflows.append(subworkflow.split('/')[-1][:-1])
    
                    #print('modules used in: ' + subworkflow)
                    with open(workflow.split('/')[0] + '/' + subworkflow[:-1]) as file:
                        sw_text = file.read().split('\n')
                        for line in sw_text:
                            if line.split(' ')[0] == "include":
                                #print(line.split(' ')[-1])
                                used_modules.append(line.split(' ')[-1].split('/')[-1][:-1])
    return [used_subworkflows, used_modules]


def get_unused_files(pipeline_dir, subworkflow_dir, module_dir, used_sub, used_mod):
## Creating list of subworkflows to move to unused
    unused_subworkflows = []
    unused_modules = []
    
    for sub in os.listdir(pipeline_dir + '/' + subworkflow_dir):
        if sub not in used_sub:
            print(sub + ' is not used in this pipeline and will be scheduled for archival')
            unused_subworkflows.append(sub)
    
    print('---------------------------------------------------------------')

    
    for mod in os.listdir(pipeline_dir + '/' + module_dir):
        if mod not in used_mod:
            unused_modules.append(mod)

    return [unused_subworkflows, unused_modules]

def create_archive_structure(pipeline_dir): 
    # Define the directory paths
    main_dir = pipeline_dir + '/Archive_NFParser'
    sub_dirs = ["modules", "subworkflows"]
    
    # Create the main directory
    os.makedirs(main_dir, exist_ok=True)
    
    # Create subdirectories inside the main directory
    for sub_dir in sub_dirs:
        os.makedirs(os.path.join(main_dir, sub_dir), exist_ok=True)
    
    print("Directory structure created (or already exists).")

def move_file_with_suffix(src_file, dest_dir):
    # Get the base name and extension of the file
    base_name, ext = os.path.splitext(os.path.basename(src_file))
    dest_file = os.path.join(dest_dir, os.path.basename(src_file))
    
    # Check if the file already exists
    counter = 1
    while os.path.exists(dest_file):
        # Modify the file name with a suffix (e.g., -1, -2, etc.)
        dest_file = os.path.join(dest_dir, f"{base_name}-{counter}{ext}")
        counter += 1

    # Move the file
    shutil.move(src_file, dest_file)
    print(f"Moved: {src_file} to {dest_file}")

def archive_files(pipeline_dir, source_dir, file_list, archive_folder):
    if len(file_list) > 0:
        for file in file_list:
            move_file_with_suffix(pipeline_dir + '/' + source_dir + '/' + file, pipeline_dir + '/Archive_NFParser/' + archive_folder)
    else:
        print('There were no unused files in ' + source_dir + ' so no files were moved')

def whole_process(pipeline_dir, workflow_dir, subworkflow_dir, module_dir):
    workflows = get_workflows(pipeline_dir, workflow_dir)
    used_files = get_used_files(pipeline_dir, workflows)
    unused_files = get_unused_files(pipeline_dir, subworkflow_dir, module_dir, used_files[0], used_files[1])
    create_archive_structure(pipeline_dir)
    archive_files(pipeline_dir, subworkflow_dir, unused_files[0], subworkflow_dir)
    archive_files(pipeline_dir, module_dir, unused_files[1], module_dir)

def parse_args():
    parser = argparse.ArgumentParser(description='Process directories for the pipeline.')
    
    # Required argument
    parser.add_argument('--pipeline_dir', type=str, required=True, help='Pipeline directory')
    
    # Optional arguments with default values
    parser.add_argument('--workflow_dir', type=str, default='workflows', help='Workflow directory (default: workflows)')
    parser.add_argument('--subworkflow_dir', type=str, default='subworkflows', help='Subworkflow directory (default: subworkflows)')
    parser.add_argument('--module_dir', type=str, default='modules', help='Module directory (default: modules)')

    return parser.parse_args()

    return parser.parse_args()

# Main function
def main():
    # Parse the arguments
    args = parse_args()
    
    # Use the parsed arguments
    pipeline_dir = args.pipeline_dir
    workflow_dir = args.workflow_dir
    subworkflow_dir = args.subworkflow_dir
    module_dir = args.module_dir

    whole_process(pipeline_dir, workflow_dir, subworkflow_dir, module_dir)

if __name__ == "__main__":
    main()