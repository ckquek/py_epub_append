import xml.etree.ElementTree as ET
import os
import django
from django.conf import settings
from django.template.loader import get_template
from tools import filepathCleanup, text_to_html_paragraphs

def eppath_setup(page_tmplt_path):
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [page_tmplt_path],
        }
    ]
    settings.configure(TEMPLATES=TEMPLATES)
    django.setup()

def append_pages(directory, current_path, template_path, folder_name):
    page_detail_dict = [] 
    print(current_path)
    result_path = current_path / "result"
    print(result_path)
    oebps_path = result_path  / folder_name / "OEBPS"
    if not os.path.exists(oebps_path):
        os.makedirs(oebps_path)
    print(oebps_path)

    # Iterate over files in directory
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
                new_filename = basename + ".html"
                with open(oebps_path / new_filename, 'w') as writefile:
                    writefile.write(html_text)
    build_book(current_path, folder_name, template_path, page_detail_dict)

def build_page(title, data):
    template = get_template('page.html')
    print("Processing '" + title + "'")
    c = dict({"title": title, "body":data})
    render = template.render(c)
    return render
    
def build_book(current_path, folder_name, template_path,  page_detail_dict):   

    result_path = current_path / "result"
    print(result_path)
    print(page_detail_dict)
    xmlfile_path = template_path / "book.opf"
    print(template_path)
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
        
    print(result_path / folder_name / "book.opf")
    ET.indent(tree, '\t')
    tree.write(result_path / folder_name / "book.opf", encoding="utf-8", xml_declaration=True)