import pandas as pd
import os
import sys
import subprocess

os.makedirs("res", exist_ok=True)
for arg in sys.argv[1:]:
    # assuming the csv file is named 'data.csv'
    df = pd.read_csv(arg)

    # You can then access the data in the dataframe like this:
    for index, row in df.iterrows():
        file_id = os.path.basename(row['file_id']).split('.')[0]
        input_path = row['input_path']
        output_path = row['output_path']
        score = row['score'] * 10.0 / 3.0  # 30 questions for 100 points

        print(f'{file_id} input: {input_path} output: {output_path}  score: {score:.2f}')

        filename = os.path.basename(input_path)
        command = "convert '{}' -background Khaki -pointsize 105 label:'{} nota {}' +swap -gravity Center -append 'res/{}'".format(input_path, file_id, round(score, 1), filename)

        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output, error = process.communicate()

        if error:
            print(f"Error: {error}")
