import sys
import pprint

build_file_path = sys.argv[1]
files_in_project = sys.argv[2]

f = open(build_file_path, "r")
lines = f.readlines()
f.close()

pprint.pprint(lines)