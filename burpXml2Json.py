#!/usr/bin/python3

import xml.etree.ElementTree as ET
import json
import argparse

# Quick script made to converts Burp Exported XML files into JSONL files for easier integration in your workflows

# Example usage:
# BurpXml2Json.py -f burp_export.xml                                           # Convert XML to JSONL, output to burp_export.xml.jsonl
# python BurpXml2Json.py -f burp_export.xml -o burp_recon.jsonl                # Convert XML to JSONL, output to burp_recon.jsonl  
# python BurpXml2Json.py -f burp_export.xml -o burp_export.jsonl -v            # Convert XML to JSONL, verbose output  


class burpXml2json:
    def __init__(self, input_filename, output_filename, verbose=False):
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.verbose = verbose

    def readXml(self):
        tree = ET.parse(self.input_filename)
        root = tree.getroot()
        return root

    def writeOutput(self, output):
        with open(self.output_filename, 'w') as f:
            f.write(output)

    def convertToJson(self, root):
        output = ''
        for item in root:
            item_data = {}
            for elem in item:
                item_data[elem.tag] = elem.text
                for attr_key, attr_value in elem.attrib.items():
                    item_data[f'{elem.tag}_{attr_key}'] = attr_value
            json_line = json.dumps(item_data)
            output += json_line + '\n'
            if self.verbose:
                print(json_line)
        return output


    def run(self):
        root = self.readXml()
        output = self.convertToJson(root)
        self.writeOutput(output)
        return output, self.output_filename

    


if __name__ == "__main__":
    argparse = argparse.ArgumentParser(description='Convert Burp Export XML to JSONL')
    argparse.add_argument('-f', '--input', required=True, help='Input XML file')
    argparse.add_argument('-o', '--output', help='Output JSONL file')
    argparse.add_argument('-v', '--verbose', action='store_true', help='Output to stdout')
    args = argparse.parse_args()

    if args.output:
        output_filename = args.output
    else:
        output_filename = args.input + '.jsonl'

    try:
        output= burpXml2json(args.input, output_filename, args.verbose).run()

    except Exception as e:
        print(e)
