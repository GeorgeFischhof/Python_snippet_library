
from pathlib import Path


def create_dir(dir_name):
    directory = Path(dir_name)
    directory.mkdir(exist_ok=True)


def remove_dir(dir_name):
    directory = Path(dir_name)
    directory.rmdir()

def get_existing_folder_with_substring(root_folder, substring):
    existing_folder_name = ''
    for dir_path, dir_names, file_names in os.walk(root_folder):
        for name in dir_names:
            if substring.upper() in name.upper():
                existing_folder_name = dir_path + name
    return existing_folder_name
