import argparse
import requests
import xml.etree.ElementTree as ET

def fetch_metadata(sample_id):
    url = f"https://www.ebi.ac.uk/ena/browser/api/xml/{sample_id}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch metadata for sample ID '{sample_id}'")

def parse_metadata(xml_data):
    metadata = {}
    root = ET.fromstring(xml_data)
    for child in root:
        if child.tag.endswith("SAMPLE"):
            for attr in child:
                if attr.tag.endswith("SAMPLE_ATTRIBUTES"):
                    for attribute in attr:
                        key = attribute.find("{*}TAG").text
                        value = attribute.find("{*}VALUE").text
                        metadata[key] = value
    return metadata
import json
def main():
    parser = argparse.ArgumentParser(description="Fetch metadata fields add add to fastq-run-info.json from fastq-dl")
    parser.add_argument("file", help="fastq-run-info.json file")
    parser.add_argument("--output", help="output file")

    args = parser.parse_args()
    # read json
    with open(args.file) as f:
        data = json.load(f)
    for sample in data:
        sample_id = sample["sample_accession"]
        metadata = get_data(sample_id)
        intersection = set(sample.keys()) & set(metadata.keys())
        if intersection:
            print(f"WARNING: Overwriting metadata fields: {intersection}")
        sample.update(metadata)
    # write json
    with open(args.output, "w") as f:
        json.dump(data, f, indent=4)



def get_data(sample_id):
    xml_data = fetch_metadata(sample_id)
    metadata = parse_metadata(xml_data)

    for key, value in metadata.items():
        print(f"{key}: {value}")
    return metadata 

if __name__ == "__main__":
    main()
