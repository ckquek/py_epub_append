import zipfile
from pathlib import Path

from epub_processing import eppath_setup, append_pages


raw_directory = input("Drag and drop epub:")
print(raw_directory)
directory = Path(raw_directory)
current_path = directory.parent
folder_name = directory.name
print("folder_name:" + folder_name)

page_tmplt_path = current_path / "template"
print(page_tmplt_path)
eppath_setup(page_tmplt_path)

append_pages(directory, current_path, page_tmplt_path, folder_name)