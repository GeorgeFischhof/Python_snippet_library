
import zipfile

with zipfile.ZipFile('d:/path/to/zip_file_to_create_bz2.zip', 'w',
                     compression=zipfile.ZIP_BZIP2) as output_zip:
    output_zip.write('d:/path/to/original/file.txt')



# https://pymotw.com/3/zipfile/