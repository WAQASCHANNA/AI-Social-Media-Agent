import zipfile
import xml.etree.ElementTree as ET
import sys
import os

docx_path = r"g:\Data 02\Code Learning\Hackathon\Hack nation\12. AI Social Media Agent – Automated, Brand-Aware Content Creation for LinkedIn & Instagram.docx"

try:
    if not os.path.exists(docx_path):
        print(f"File not found: {docx_path}")
        sys.exit(1)

    with zipfile.ZipFile(docx_path) as z:
        xml_content = z.read('word/document.xml')
        tree = ET.fromstring(xml_content)
        
        # XML namespace for Word
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        
        text_parts = []
        for p in tree.findall('.//w:p', ns):
            texts = [node.text for node in p.findall('.//w:t', ns) if node.text]
            if texts:
                text_parts.append(''.join(texts))
        
        print('\n'.join(text_parts))

except Exception as e:
    print(f"Error reading docx: {e}")
