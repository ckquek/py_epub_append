import os
import zipfile

from enum import Enum

def filepathCleanup(filepath):
    print("   aaa filepath: ",filepath)
    cleaned_filepath = filepath.strip("'")
    print("   aaa cleaned_filepath: ",cleaned_filepath)
    filename = os.path.basename(cleaned_filepath)
    print("   aaa filename: ",filename)
    basename, file_ext = os.path.splitext(filename)
    print("   aaa basename: ",basename)
    print("   aaa file_ext: ",file_ext)
    return cleaned_filepath, filename, basename, file_ext

def printStuff(str):
    print("HELLO  " + str)