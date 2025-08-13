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
       
    return cleaned_filepath

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

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)
