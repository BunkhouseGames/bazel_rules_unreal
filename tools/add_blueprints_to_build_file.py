import sys
import pprint
import json

# content_overview_file_path is a json file that gets passed in in  this structure.
"""
{
    AssetType: [
        {
            "Name": ""
            "ProjectPath": "",
            "Type": ""
            ...
            ]
}
"""


project_root_folder_name = sys.argv[1]
content_overview_file_path = sys.argv[2]
output_file = sys.argv[3]

f = open(content_overview_file_path, "r")
data = json.load(f)
f.close()

def generate_build_action(asset_name, asset_path):

    return f"""
compile_blueprint(
    name = "{asset_name}",
    engine_executable = "unreal_executable",
    project_file = "unreal_project_file",
    blueprint = "{asset_path}")
    """

output_data = []
output_data.append("#### Generated actions! Do not modify bellow! ####")
blueprints_added = []

if "Blueprint" in data:
    for each_blueprint in data["Blueprint"]:
        if each_blueprint["Root"] != "Engine":
            if each_blueprint["Root"] == "Game":
                
                bazel_label_to_file = each_blueprint["Path"].split(".")[0] + ".uasset"
                bazel_label_to_file = "//" + bazel_label_to_file.replace("/Game/", project_root_folder_name + "/Content:")
                print(bazel_label_to_file)

                data = generate_build_action(each_blueprint["Name"], bazel_label_to_file)
                blueprints_added.append(data)

            # TODO add support for content in plugins ( We'll need to generate build files for the content files there)

output_data.extend(blueprints_added)

f = open(output_file, "w")
f.writelines(output_data)
f.close()