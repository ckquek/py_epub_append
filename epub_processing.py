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


def append_pages(page_source_path, source_path, dest_path, folder_name):
    page_detail_dict = []
    oebps_path = dest_path / "OEBPS"
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
    build_book(dest_path, folder_name, source_path, page_detail_dict)

def build_page(title, data):
    template = get_template('page.html')
    # print("Processing '" + title + "'")
    c = dict({"title": title, "body":data})
    render = template.render(c)
    return render
    
def build_book(dest_path, folder_name, source_path, page_detail_dict):
    book_namespace = {"ns" : "http://www.idpf.org/2007/opf"}
    bookopf_path = source_path / "book.opf"
    tocncx_path = source_path / "toc.ncx"
    
    book_tree = ET.parse(bookopf_path)
    book_root = book_tree.getroot()
    book_manifest = book_root.find('ns:manifest', book_namespace)
    book_spine = book_root.find('ns:spine', book_namespace)

    toc_namespace = {"ncx": "http://www.daisy.org/z3986/2005/ncx/"}
    toc_tree = ET.parse(tocncx_path)
    toc_root = toc_tree.getroot()
    toc_navmap = toc_root.find('ncx:navMap', toc_namespace)
    toc_navpoint = toc_navmap.findall("ncx:navPoint", toc_namespace)
    toc_playorder = len(toc_navpoint)
    print(ET.tostring(toc_root, encoding="UTF-8"))

    for page_detail in page_detail_dict:
        man_item = ET.SubElement(book_manifest, 'item')
        # print(page_detail['page_filename'])
        man_item.attrib['id'] = page_detail['page_filename']
        man_item.attrib['href'] = "OEBPS/" + page_detail['page_filename'] + ".html"
        man_item.attrib['media-type'] = "application/xhtml+xml"
    
        spine_item = ET.SubElement(book_spine, 'itemref')
        spine_item.attrib['idref'] = page_detail['page_filename']
        spine_item.attrib['linear'] = "yes"

        navPoint = ET.SubElement(toc_navmap, 'navPoint')
        navPoint.attrib['id'] = page_detail['page_filename']
        toc_playorder += 1
        navPoint.attrib['playOrder'] = str(toc_playorder)
        navLabel = ET.SubElement(navPoint, 'navLabel')
        nav_text = ET.SubElement(navLabel, 'text')
        nav_text.text = page_detail['title']
        content = ET.SubElement(navPoint, 'content')
        content.attrib['src'] = "OEBPS/" + page_detail['page_filename'] + ".html"
    

    ET.indent(book_tree, '\t')
    book_tree.write(dest_path / "book.opf", encoding="utf-8", xml_declaration=True)
    ET.indent(toc_tree, '\t')
    toc_tree.write(dest_path / "toc.ncx", encoding="utf-8", xml_declaration=True)