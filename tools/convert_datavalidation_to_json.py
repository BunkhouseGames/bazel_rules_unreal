import sys
import json

raw_data_validation_path = sys.argv[1]
content_overview_file = sys.argv[2]

# read the input file
s = open(raw_data_validation_path, "r")
lines = s.readlines()
s.close()


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

            asset = {
                "Name": asset_name,
                "Path": asset_path,
                "Type": asset_type,
                "Root": asset_location
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