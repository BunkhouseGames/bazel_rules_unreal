import sys
import json

input_path = sys.argv[1]
output_path = sys.argv[2]

# read the input file
s = open(input_path, "r")
lines = s.readlines()
s.close()

# parse the type and asset name logic out
assets = {}
for line in lines:
    if "LogContentValidation: " in line:
        line = line.replace("\n", "")
        asset_name = line.split(" ")[-1]
        asset_type = line.split(" ")[-2]
        if asset_type in assets:
            assets[asset_type].append(asset_name)
        else:
            assets[asset_type] = [asset_name]


f = open(output_path, "w")
f.write(json.dumps(assets, indent=4))
f.close()