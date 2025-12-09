import os
import sys
import shutil
import subprocess
import re
import pandas as pd
from rich.console import Console
from rich.table import Table
import json

def copy_files(source_dir, dest_dir):
    """Copies all files from source_dir to dest_dir, overwriting if necessary."""
    os.makedirs(dest_dir, exist_ok=True)
    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)
        destination_file = os.path.join(dest_dir, filename)
        if os.path.isfile(source_file):
            shutil.copy2(source_file, destination_file)
            # print(f"Copied {source_file} to {destination_file}")

source_dir_mcq_block_0 = "upb/mcq_block_0"
source_dir_mcq_block_012 = "upb/mcq_block_012"
dest_dir = "inputs/partial"

# 1. Initial copy to inputs/partial
copy_files(source_dir_mcq_block_0, dest_dir)

# 3. Create variant directories and copy/process answer_key.csv
for variant in ["A", "B", "C", "D", "E", "F"]:
    variant_base_dir = os.path.join("inputs", variant) # Corrected path for variant directories
    os.makedirs(variant_base_dir, exist_ok=True)
    
    # Copy files from mcq_block_012 to the new variant directory
    copy_files(source_dir_mcq_block_012, variant_base_dir)

    # Process answer_key.csv in the variant directory
    answer_key_csv_path = os.path.join(variant_base_dir, "answer_key.csv")
    if os.path.exists(answer_key_csv_path):
        try:
            df = pd.read_csv(answer_key_csv_path)
            if "Nr" in df.columns and variant in df.columns:
                # Select 'Nr' and the current variant column
                processed_df = df[["Nr", variant]]
                # Rename the variant column to 'answer'
                #processed_df = processed_df.rename(columns={variant: "answer"})
                processed_df.to_csv(answer_key_csv_path, index=False)
                print(f"Processed {answer_key_csv_path} for variant {variant}")
            else:
                print(f"Warning: 'Nr' or '{variant}' column not found in {answer_key_csv_path}, skipping processing.")
        except Exception as e:
            print(f"Error processing {answer_key_csv_path}: {e}")



console = Console()

print("\nRunning OMRChecker and parsing output...")

command = ["python3", "main.py", "-i", dest_dir]
process = subprocess.run(command, capture_output=True, text=True, check=True)
output = process.stdout

# Regex to find the image file path
image_path_regex = re.compile(r"INFO\s+\(\d+\)\s+Opening image:\s+\'(.*?)\'\s+Resolution:")

# Regex to find the \\\\\\\'Marked\\\\\\\\\' value for \\\\\\\'Nr\\\\\\\\\' from the table
marked_variant_regex = re.compile(r"│\s*Nr\s*│\s*([A-F])\s*│")

results = []
current_image = None
looking_for_variant = False # State to indicate we are looking for a variant after an image

for line in output.splitlines():
    image_match = image_path_regex.search(line)
    if image_match:
        current_image = os.path.basename(image_match.group(1))
        looking_for_variant = True
        print(f"Found image: {current_image}\r", file=sys.stderr, flush=True)
        continue # Start looking for the variant in subsequent lines
    
    if looking_for_variant:
        variant_match = marked_variant_regex.search(line)
        if variant_match:
            variant = variant_match.group(1)
            if current_image: # Ensure an image was found before adding result
                results.append({"File": current_image, "Variant": variant})
            current_image = None # Reset for the next image
            looking_for_variant = False # Reset state, found variant for current image

# Display results in a table
if results:
    table = Table(title="OMRChecker Results")
    table.add_column("Input File")
    table.add_column("Variant")

    for row in results:
        table.add_row(row["File"], row["Variant"])
    
    console.print(table)
else:
    print("No OMRChecker results found or parsed.")

# New code to move files from inputs/partial to inputs/<variant>
if results:
    print("\nOrganizing files from inputs/partial into variant directories...")
    for row in results:
        file_name = row["File"]
        variant = row["Variant"]
        
        # The variant directories are now directly under 'inputs/'
        variant_target_dir = os.path.join("inputs", variant)
        
        source_file_path = os.path.join(dest_dir, file_name)
        destination_file_path = os.path.join(variant_target_dir, file_name)
        
        if os.path.exists(source_file_path):
            shutil.copy(source_file_path, destination_file_path)
        #    print(f"Copied {file_name} to {variant_target_dir}/")
        else:
            print(f"Warning: {file_name} not found in {dest_dir}, skipping move.")
else:
    print("No files to organize.")

