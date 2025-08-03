import os
import re
import zipfile

from enum import Enum

def filepathCleanup(filepath):
    pref_substr = filepath[:1]
    post_substr = filepath[-1:]
    cleaned_filepath = filepath
    if pref_substr == "'" and pref_substr == post_substr:
        cleaned_filepath = filepath[1:-1]
       
    folder_name = cleaned_filepath.rsplit("\\", 1)[1]
    return cleaned_filepath, folder_name

def text_to_html_paragraphs(text):
    # First, replace multiple newlines with a single newline,
    # so you don't get empty paragraphs
    text = re.sub(r'\n\s*\n', '\n', text)

    # Split the text into lines
    lines = text.split('\n')
    title = ""

    if lines[0].startswith("Chapter"):
        title = lines[0]
        lines[0] = "<b>" + lines[0] + "</b>"
    elif lines[0].startswith("<b>"):
        title = lines[0][3:-4]

    # Wrap each line in a <p> tag and join them
    return title, ''.join(f"<p>{line.strip()}</p>\n" for line in lines)
