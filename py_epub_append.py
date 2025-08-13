import zipfile
from pathlib import Path
from os import path, makedirs
from shutil import rmtree

from epub_processing import eppath_setup, append_pages
from tools import filepathCleanup

raw_directory = input("Drag and drop epub:")
cleaned_directory = filepathCleanup(raw_directory)
directory = Path(cleaned_directory)
current_path = directory.parent
folder_name = directory.name
cleaned_filepath = str(current_path / folder_name)
print("folder_name:" + folder_name)
print(cleaned_filepath)


# set paths
page_tmplt_path = current_path / "template"
temp_path = current_path / "temp"
result_path = current_path / "result"
page_source_path = current_path / "pages"

# unzip
with zipfile.ZipFile(str(cleaned_filepath), "r") as zip_ref:
    try:
        rmtree(temp_path)
        print("% s removed successfully" % temp_path)
    except OSError as error:
        print(error)
        print("File path can not be removed")
    makedirs(temp_path)
    zip_ref.extractall(temp_path)

eppath_setup(page_tmplt_path)

append_pages(page_source_path, temp_path, page_tmplt_path, folder_name)

