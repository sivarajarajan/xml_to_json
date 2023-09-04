"""
Convert xml to json of specific template.
Replace the value of the json object with the value from the xml
"""

import os
import json
import xml.etree.ElementTree as ET

import mapping

CURRENT_DIR = os.path.abspath(os.curdir)
XML_SRC_DIR = os.path.join(CURRENT_DIR, 'src')
JSON_TEMPLATE = os.path.join(CURRENT_DIR,'renderer.json')
MAPPINGS = os.path.join(CURRENT_DIR,'mapping.py')

print(f"CURRENT_DIR : {CURRENT_DIR}")

def list_all_xml():
    src_list= [os.path.join(XML_SRC_DIR, filename) for filename in os.listdir(XML_SRC_DIR) if filename.endswith('.xml')]
    print(f"src list : {src_list}")
    return src_list

def main():
    src_list = list_all_xml()
    with open(JSON_TEMPLATE, 'r') as fp:
        json_data = json.load(fp)

    mappings = mapping.xml_2_json_mapping
    
    for src_xml in src_list:
        # print(os.path.exists(src_xml))
        tree = ET.parse(src_xml)
        root = tree.getroot()
        # print(root)

        for xml_k,json_k in mappings.items():
            #print(root.find(xml_k).text)
            
            keys = [k.replace("['", "").replace("']", "").replace("'","") for k in json_k.split("][")]
            print(f"{keys} - {root.find(xml_k).text}")

            value = json_data
            for key in keys[:-1]:
                #print(f"processing : {key}")
                value = value[key if not key.isdigit() else int(key)]
            value[keys[-1]] = root.find(xml_k).text

        # print(f"value = {value}")
        # print(f"json_data ; {json_data}")

        json_filename = os.path.basename(src_xml).replace("xml", "json")
        print(f"Output file : {json_filename}")
        json_object = json.dumps(json_data, indent=4)
        with open(os.path.join(CURRENT_DIR, "dest", json_filename), "w") as wp:
            wp.write(json_object)



if __name__ == "__main__":
    main()


