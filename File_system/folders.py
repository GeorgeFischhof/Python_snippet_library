
import glob
import os
import sys

import datetime_helper
from datetime_helper import DateTimeFormat


def create_output_folder_platform_timestamp(root_folder):
    platform = sys.platform
    now = datetime_helper.get_now(dt_format=DateTimeFormat.COMPACT_WITH_US)['datetime_str']
    output_folder = os.path.sep.join((root_folder, 'test_output_%s_%s' % (platform, now)))
    os.makedirs(output_folder, exist_ok=True)

    return output_folder


def create_debug_folder(root_folder):
    debug_folder = os.path.sep.join((root_folder, 'debug'))
    os.makedirs(debug_folder, exist_ok=True)

    return debug_folder


def remove_trailing_delimiter_from_folder(folder_name):
    return os.path.normpath(folder_name)


def get_last_subfolder(folder_name):
    folder = remove_trailing_delimiter_from_folder(folder_name)
    return os.path.basename(folder)


def get_folder_with_trail_separator(folder_name):
    return remove_trailing_delimiter_from_folder(folder_name) + os.path.sep


def get_txt_files_from_folder(folder_name) -> list:
    txt_files = glob.glob(get_folder_with_trail_separator(folder_name) + '*.txt')
    return sorted(txt_files)


def get_filename_from_full_path(full_path):
    if os.path.isfile(full_path):
        return os.path.basename(full_path)
    else:
        return ''
