import sys
import json

raw_data_validation_path = sys.argv[1]
content_overview_file = sys.argv[2]

# read the input file
s = open(raw_data_validation_path, "r")
lines = s.readlines()
s.close()

asset_identifiers = []

def parse_data_validation(raw_data_validation_path):
    # parse the type and asset name logic out
    assets = {}

    for line in lines:
        if "LogContentValidation: " in line:
            line = line.replace("\n", "")

            asset_path = line.split(" ")[-1]
            asset_name = asset_path.split(".")[-1]
            asset_type = line.split(" ")[-2]
            asset_location = asset_path.split("/")[1]
            
            asset_identifiers.append(asset_name)

            if asset_identifiers.count(asset_name) > 1:
                asset_identifier = asset_name + "_" + str(asset_identifiers.count(asset_name)) + "_dup"
            else:
                asset_identifier = asset_name

            asset = {
                "name": asset_name,
                "path": asset_path,
                "type": asset_type,
                "root": asset_location,
                "asset_identifier": asset_identifier
                }

            if asset_type in assets:
                assets[asset_type].append(asset)
            else:
                assets[asset_type] = [asset]
    
    return assets

content_overview_data = parse_data_validation(raw_data_validation_path)

f = open(content_overview_file, "w")
f.write(json.dumps(content_overview_data, indent=4))
f.close()