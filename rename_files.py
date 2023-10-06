import os
import re
from pathlib import Path

# Constants for pattern and filename components
PATTERN = r''
FILENAME_TEMPLATE = "{number}_{name}.{extension}"

def rename_files_in_directory(directory_path, new_directory_path):
    try:
        os.makedirs(new_directory_path, exist_ok=True)
        files_to_rename = [(filename, convert_filename(directory_path, new_directory_path, filename)) for filename in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, filename))]
        
        for old_filename, new_filename in files_to_rename:
            if new_filename:
                old_filepath = os.path.join(directory_path, old_filename)
                new_filepath = os.path.join(new_directory_path, new_filename)
                i = 1
                while os.path.exists(new_filepath):
                    # If the file already exists, add 'Copy' and a number at the beginning
                    new_filename = f"Copy_{i}_" + new_filename
                    new_filepath = os.path.join(new_directory_path, new_filename)
                    i += 1
                os.rename(old_filepath, new_filepath)
    except OSError as e:
        print(f"An error occurred: {e}")

def convert_filename(directory_path, new_directory_path, old_filename):
    match = re.match(PATTERN, old_filename, re.IGNORECASE)
    
    if match:
        number = match.group(1)
        name = ' '.join(match.group(2).split())  # Remove extra spaces
        extension = match.group(3)
        
        new_filename = FILENAME_TEMPLATE.format(
            number=number,
            name=name.replace('– ', ''),
            extension=extension
        )
        return new_filename
    else:
        return None

if __name__ == "__main__":
    # Get the current directory
    current_directory = Path.cwd()

    # Specify the new directory to save the renamed files
    new_directory = current_directory / "renamed_files"

    # Rename all files in the directory and save to the new directory
    rename_files_in_directory(current_directory, new_directory)
