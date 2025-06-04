import pandas as pd
import os
import sys
import subprocess

# assuming the csv file is named 'data.csv'
df = pd.read_csv(sys.argv[1])

# You can then access the data in the dataframe like this:
for index, row in df.iterrows():
    file_id = row['file_id']
    input_path = row['input_path']
    output_path = row['output_path']
    score = row['score']

    print(f'file_id: {file_id}, input_path: {input_path}, output_path: {output_path}, score: {score}')

    filename = os.path.basename(input_path)
    command = "convert '{}' -background Khaki -pointsize 150 label:'nota {}' +swap -gravity Center -append 'res/{}'".format(input_path, round(score, 1), filename)

    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    if error:
        print(f"Error: {error}")

