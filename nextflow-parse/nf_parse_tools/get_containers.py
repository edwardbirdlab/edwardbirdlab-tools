import os
import pandas as pd

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


def get_contaienrs(pipeline_dir, module_dir, output_csv):
    nf_files = get_nf_files(pipeline_dir + '/' + module_dir)
    nf_files

    paths = []
    conts = []

    for path in nf_files:
        with open(path) as file:
            text = file.read().split('\n')
            for line in text:
                words = line.split()
                if 'container' in words:
                    paths.append(path)
                    conts.append(words[1])

    conts_df = pd.DataFrame()
    conts_df['path'] = paths
    conts_df['cont'] = conts

    conts_df.to_csv(output_csv, index=False)
    print("CSV with list of Containers and corresponding modules was output to " + output_csv)