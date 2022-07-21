import sys
import pprint
import json

asset_data = sys.argv[1]
out = sys.argv[2]

f = open(asset_data, "r")
data = json.load(f)
f.close()

def generate_build_action(bp_name, stripped):

    return f"""
compile_blueprint(
    name = "{bp_name}",
    engine_executable = "unreal_executable",
    project_file = "unreal_project_file",
    blueprint = "{stripped}")
    """

output_data = []
output_data.append("#### Generated actions! Do not modify bellow! ####")

if "Blueprint" in data:
    for each_blueprint in data["Blueprint"]:
        if each_blueprint.lower().startswith("/game/"):
            bp = each_blueprint.lower().replace("/game/", "//BazelTestProjectGame/Content:")
            bp_name = bp.split(".")[-1]
            stripped = bp.split(".", 1)[0] + ".uasset"

            output_data.append(generate_build_action(bp_name, stripped))

f = open(out, "w")
f.writelines(output_data)
f.close()