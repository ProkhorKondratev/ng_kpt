import lxml.etree as ET
import re
import zipfile
from collections import Counter
from io import BytesIO


class XMLParser:
    @staticmethod
    def fix_sk_id(arc_path: str):
        temp_archive = BytesIO()

        with zipfile.ZipFile(arc_path, 'r') as src_archive:
            with zipfile.ZipFile(temp_archive, 'w', zipfile.ZIP_DEFLATED) as dst_archive:
                for obj in src_archive.infolist():
                    if obj.file_size > 1000 and obj.filename.endswith('.xml'):
                        with src_archive.open(obj) as file:
                            xml_content = file.read()
                            root = ET.fromstring(xml_content)

                            XMLParser.replace_sk_id(root=root)
                            # sk_ids, errors = XMLParser.replace_sk_id(root=root)
                            # common_id = XMLParser.find_most_common_sk_id(sk_ids=sk_ids)
                            # XMLParser.fix_errors(errors=errors, common_id=common_id)

                            dst_archive.writestr(obj, ET.tostring(root, encoding='utf-8', xml_declaration=True))
                    else:
                        dst_archive.writestr(obj, src_archive.read(obj))

        with open(arc_path, 'wb') as f:
            f.write(temp_archive.getvalue())

    @staticmethod
    def replace_sk_id(root):
        sk_ids = []
        errors = []

        pattern = re.compile(r'мск\s*-?\s*(\d{2})[^\d]*?(\d)', re.IGNORECASE)
        correct_format = re.compile(r'^[1-9]\d[.,\s-]*([1-9]|[1-9]\d)$')

        for elem in root.findall('.//sk_id'):
            if elem.text:
                if correct_format.match(elem.text):
                    sk_ids.append(elem.text)
                elif elem.text.lower().startswith("мск"):
                    match = pattern.search(elem.text)
                    if match:
                        transformed_text = f"{match.group(1)}.{match.group(2)}"
                        elem.text = transformed_text
                        sk_ids.append(transformed_text)
                    else:
                        errors.append(elem)
                else:
                    errors.append(elem)

        return sk_ids, errors

    @staticmethod
    def find_most_common_sk_id(sk_ids):
        counter = Counter(sk_ids)
        most_common_sk_id, _ = counter.most_common(1)[0]
        return most_common_sk_id

    @staticmethod
    def fix_errors(errors, common_id):
        for elem in errors:
            if elem.text != common_id:
                elem.text = common_id
