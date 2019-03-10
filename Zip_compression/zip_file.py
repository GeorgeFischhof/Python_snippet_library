
def read_all_lines_from_zipped_file(zip_file_name, inner_file_name):
    with zipfile.ZipFile(zip_file_name) as input_zip:
        with input_zip.open(inner_file_name) as input_file:
            all_lines = str(input_file.read(), encoding='utf-8').splitlines()

    return all_lines


def get_txt_files_from_zip(zip_file_name) -> list:
    with zipfile.ZipFile(zip_file_name) as input_zip:
        txt_files = [file_name for file_name in input_zip.namelist() if file_name.endswith('.txt')]

    return txt_files

import os
import zipfile

import folders


def zip_txt_files(folder_name) -> dict:
    """Zips *.txt files in last subfolder, next to txt files, zip file is named as last subfolder,
    the txt files in the zip will have no path

    :return: {'zip_file_name': 'zip_file_name', 'success': boolean}
    """

    folder_with_trail_separator = folders.get_folder_with_trail_separator(folder_name)
    zip_file_name = folder_with_trail_separator + folders.get_last_subfolder(folder_name) + '.zip'

    zip_result = {'zip_file_name': zip_file_name}

    txt_files_with_path = folders.get_txt_files_from_folder(folder_name)
    with zipfile.ZipFile(zip_file_name, 'w', compression=zipfile.ZIP_BZIP2) as output_zip:
        for txt_file in txt_files_with_path:
            output_zip.write(txt_file, arcname=folders.get_filename_from_full_path(txt_file))
        test_result = output_zip.testzip()
    if test_result is None:
        zip_result['success'] = True
    else:
        zip_result['success'] = False

    return zip_result


def zip_txt_files_in_several_subfolders(root_folder_name):
    """First level subfolders of the root_folder_name are passed to zip_txt_files function

    :return: list of dicts {'zip_file_name': 'zip_file_name', 'success': boolean}
    """

    zip_results = list()
    folder_entries = os.listdir(root_folder_name)
    for entry in folder_entries:
        full_path = root_folder_name + os.path.sep + entry
        if os.path.isdir(full_path):
            zip_result = zip_txt_files(full_path)
            zip_results.append(zip_result)

    return zip_results