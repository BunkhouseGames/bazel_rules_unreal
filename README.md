# Bazel rules for Unreal Engine 
The goal of this project is to provide utilities that leverage the power of Bazel build in projects based around unreal engine

## Project Status
The project is still in its infancy so there is much work to be done. At the moment you can 

- Run any UE commandlet and parse the output 
- List out all the assets in the project

## Getting started

    workspace(name = "root_workspace")
    load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
    load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

    git_repository(
        name = "rules_unreal",
        remote = "git@github.com:arctictheory/bazel_rules_unreal.git",
        commit = "23b4fce4ccbd966cc31572fbeb0bf2355ec743fa")

    new_local_repository(
        name = "unreal_engine",
        build_file = "@rules_unreal//ue5/engine:ue5_engine.BUILD",
        path = "ABSOLUTE-PATH-TO-UNREAL-ENGINE"
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


## Add the build file

    load("@rules_unreal//:rules/unreal_native_rules.bzl", "run_commandlet")
    load("@rules_unreal//:rules/unreal_content_rules.bzl", "convert_data_validation_to_json")

    alias(
        name = "unreal_project_file",
        actual = "@root_workspace//BazelTestProjectGame:BazelTestProjectGame.uproject",
    )

    alias(
        name = "unreal_executable",
        actual = "@unreal_engine//:Engine/Binaries/Win64/UnrealEditor-cmd.exe",
    )


    run_commandlet(
    name = "datavalidation",   
    engine_executable = "unreal_executable",
    project_file = "unreal_project_file",
    commandlet = "DataValidation"
    )

    convert_data_validation_to_json(
    name="generate_asset_list",
    deps = ["@root_workspace//:datavalidation"]
    )

