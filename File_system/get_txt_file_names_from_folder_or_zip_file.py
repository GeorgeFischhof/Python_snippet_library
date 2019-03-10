
def get_txt_file_names(source):
    if os.path.isdir(source):
        return folders.get_txt_files_from_folder(source)
    elif os.path.isfile(source) and source.endswith('.zip'):
        return zipped_content.get_txt_files_from_zip(source)
    else:
        raise InvalidCurveSource(source)
