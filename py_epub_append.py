import tools
import os
import re
import xml.etree.ElementTree as ET
import zipfile

import django
from django.conf import settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['text/template'],
    }
]
settings.configure(TEMPLATES=TEMPLATES)
django.setup()
from django.template.loader import get_template

# Trim the quotes and clean up the filepath
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


def build_page(title, data):
    template = get_template('page.html')
    print("Processing '" + title + "'")
    c = dict({"title": title, "body":data})
    render = template.render(c)
    return render
    
def build_book():
    print(page_detail_dict)
    xmlfile_path = page_tmplt_path + "book.opf"
    tree = ET.parse(xmlfile_path)
    root = tree.getroot()
    manifest = root.find('manifest')
    spine = root.find('spine')
    
    for page_detail in page_detail_dict:
        print(page_detail)
        man_item = ET.SubElement(manifest, 'item')
        print(page_detail['page_filename'])
        man_item.attrib['id'] = page_detail['page_filename']
        man_item.attrib['href'] = "OEBPS/" + page_detail['page_filename'] + ".html"
        man_item.attrib['media-type'] = "application/xhtml+xml"
    
        spine_item = ET.SubElement(spine, 'itemref')
        spine_item.attrib['idref'] = page_detail['page_filename']
        spine_item.attrib['linear'] = "yes"
        
    print(result_path + "/" + folder_name + "/book.opf")
    ET.indent(tree, '\t')
    tree.write(result_path + "/" + folder_name + "/book.opf", encoding="utf-8", xml_declaration=True)

raw_directory = input("Enter folder path:")
#raw_directory = 'text/pg'
directory, folder_name = filepathCleanup(raw_directory)
print(directory)
print(folder_name)

page_tmplt_path = "text/template/"
write_path = "text/result/"
#folder_name = input("Project name:")

current_path = os.getcwd()
result_path = current_path + '/result'
oebps_path = result_path + '/' + folder_name + '/OEBPS'
if not os.path.exists(oebps_path):
    os.makedirs(oebps_path)

# Iterate over files in directory
page_detail_dict = []
for name in os.listdir(directory):
    # Open file
    basename, ext = os.path.splitext(name)
    if ext == ".txt":
        # oebps populating
        with open(os.path.join(directory, name)) as f:
            print(f"Content of {name}")
            title, p_text = text_to_html_paragraphs(f.read())
            
            page_detail = {"title":title, "page_filename":basename}
            page_detail_dict.append(page_detail)
            html_text = build_page(title, p_text)
            with open(oebps_path + '/' + basename + '.html', 'w') as writefile:
                writefile.write(html_text)

build_book()
# with open(path, 'r') as textfile:
#     contents = textfile.read()
#     html_text = text_to_html_paragraphs(contents)

#     with open('result/' + basename + '.html', 'w') as writefile:
#         writefile.write(html_text)