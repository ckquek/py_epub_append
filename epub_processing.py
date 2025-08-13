import xml.etree.ElementTree as ET
import os
import django
from django.conf import settings
from django.template.loader import get_template
from tools import filepathCleanup, text_to_html_paragraphs, sorted_alphanumeric

from pathlib import Path

def eppath_setup(page_tmplt_path):
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [page_tmplt_path],
        }
    ]
    settings.configure(TEMPLATES=TEMPLATES)
    django.setup()

def append_pages(page_source_path, current_path, template_path, folder_name):
    page_detail_dict = []
    oebps_path = current_path / "OEBPS"
    path = str(page_source_path.absolute())
    # Iterate over files in page_source_path
    listdir = sorted_alphanumeric(os.listdir(path))
    for name in listdir:
        # print(name)
        # Open file
        basename, ext = os.path.splitext(name)
        if ext == ".txt":
            # oebps populating
            with open(os.path.join(page_source_path, name)) as f:
                # print(f"Content of {name}")
                title, p_text = text_to_html_paragraphs(f.read())
                
                page_detail = {"title":title, "page_filename":basename}
                page_detail_dict.append(page_detail)
                html_text = build_page(title, p_text)
                new_filename = basename + ".html"
                with open(oebps_path / new_filename, 'w') as writefile:
                    writefile.write(html_text)
    build_book(current_path, folder_name, template_path, page_detail_dict)

def build_page(title, data):
    template = get_template('page.html')
    # print("Processing '" + title + "'")
    c = dict({"title": title, "body":data})
    render = template.render(c)
    return render
    
def build_book(current_path, folder_name, template_path, page_detail_dict):
    namespaces = {"ns" : "http://www.idpf.org/2007/opf"}
    xmlfile_path = template_path / "book.xml"
    tree = ET.parse(xmlfile_path)
    root = tree.getroot()
    manifest = root.find('ns:manifest', namespaces)
    spine = root.find('ns:spine', namespaces)

    for page_detail in page_detail_dict:
        man_item = ET.SubElement(manifest, 'item')
        # print(page_detail['page_filename'])
        man_item.attrib['id'] = page_detail['page_filename']
        man_item.attrib['href'] = "OEBPS/" + page_detail['page_filename'] + ".html"
        man_item.attrib['media-type'] = "application/xhtml+xml"
    
        spine_item = ET.SubElement(spine, 'itemref')
        spine_item.attrib['idref'] = page_detail['page_filename']
        spine_item.attrib['linear'] = "yes"
        
    ET.indent(tree, '\t')
    tree.write(current_path / "book.opf", encoding="utf-8", xml_declaration=True)