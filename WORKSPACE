workspace(name = "bazel-rules-urneal-workspace")
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# This is the path to a PRE-COMPILED unreal engine project
new_local_repository(
    name = "unreal_engine",
    build_file = "//bazel_rules:ue5_engine.BUILD",
    path = "" # MUST SET PATH TO UNREAL ENGINE
    )

# Add a path to the root of the project (Note that the project MUST contain a BUILD file)
local_repository(
    name = "unreal_project",
    path = "" # MUST SET PATH TO PROJECT
    )

http_archive(
    name = "rules_python",
    sha256 = "9fcf91dbcc31fde6d1edb15f117246d912c33c36f44cf681976bd886538deba6",
    strip_prefix = "rules_python-0.8.0",
    url = "https://github.com/bazelbuild/rules_python/archive/refs/tags/0.8.0.tar.gz",
)

load("@rules_python//python:repositories.bzl", "python_register_toolchains")

python_register_toolchains(
    name = "python3_9",
    python_version = "3.9",
)

load("@python3_9//:defs.bzl", "interpreter")
load("@rules_python//python:pip.bzl", "pip_install")

pip_install(
    name = "pip_install_package",
    python_interpreter_target = interpreter,
    requirements = "//:requirements.txt",
)
