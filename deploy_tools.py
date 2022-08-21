from importlib.metadata import requires
import sys
import zipfile
import os
import shutil
import subprocess

from pathlib import Path

import click

def _convert_output_string_to_absolute_path(output_string):
    return Path(output_string.split(": ")[1].replace("[", "").replace("]", "")).absolute()

def copy_files_to_target_directory(files, target_directory):

    if Path(target_directory).exists():
        shutil.rmtree(Path(target_directory).absolute())

    for source_zip_file in files:
        with zipfile.ZipFile(source_zip_file, 'r') as zip_ref:
            zip_ref.extractall(target_directory)

def run_build_action(action):

    package_path = action.split(":")[0]
    build_action = action.split(":")[1]

    cmd = ["./bazel.exe", "build", f"{package_path}:{build_action}"]
    print("Running: " " ".join(cmd))

    a = subprocess.call(cmd)

def get_output_path_for_build_action(action):

    package_path = action.split(":")[0]
    build_action = action.split(":")[1]

    cmd = ["./bazel.exe", "aquery", f"{package_path}:{build_action}"]
    print("Running: " + " ".join(cmd))

    a = subprocess.check_output(cmd).decode(sys.stdout.encoding)
    files = []
    is_correct_action = False
    for line in a.split("\n"):

        if line.lower().startswith("action"):
            if  build_action.lower() in line.lower():
                is_correct_action = True
            else:
                is_correct_action = False

        if line.startswith("  Outputs") and is_correct_action:
            path = _convert_output_string_to_absolute_path(line)

            # Skip the manifest file
            if path.suffix == ".zip":
                files.append(path)

    return files

@click.command()
@click.option('--build_action', required=True)
@click.option('--target_directory', required=True)
def hello(build_action, target_directory):
    """Simple program that greets NAME for a total of COUNT times."""

    run_build_action(build_action)
    files = get_output_path_for_build_action(build_action)
    copy_files_to_target_directory(files, target_directory)

if __name__ == '__main__':
    hello()