def run_commandlet_impl(ctx):

    # TODO This might cause problems if we have the same commandlet with different arguments
    commandlet_name = ctx.attr.commandlet

    output_file = ctx.actions.declare_file(commandlet_name + ".txt")  # file that will be generated
    bat = ctx.actions.declare_file(commandlet_name + ".bat")  # file that will contain the command

    # Fix the path to the bat file
    path_to_bat_file = bat.path.replace("/", "\\")

    # Assemble the command that will be executed
    # Path to unreal and the project file
    engine_plus_project_path = "\"" + ctx.executable.engine_executable.path.replace("/", "\\") + "\" " + "%cd%/" + ctx.files.project_file[0].path

    # Write the command into bat file
    ctx.actions.write(
        output = bat,
        content = engine_plus_project_path + " -abslog=" + "%cd%/" + output_file.path + " -run=" + ctx.attr.commandlet + "\nEXIT /B",
        is_executable = True,
    )

    path_to_bat_file = bat.path.replace("/", "\\")
    # Execute the pat file and making sure that the the blueprint we passed in gets flagged as an input so that Bazel detects any changes to it

    ctx.actions.run(
        outputs = [output_file],
        inputs = [],
        executable = "cmd.exe",
        tools = [bat],
        arguments = ["/C", path_to_bat_file],
    )

    # return the output file so that it can be used in other build steps
    return DefaultInfo(files = depset([output_file]))

def compile_blueprint_impl(ctx):
    # Get the name of the blueprint that we are processing
    blueprint_name = ctx.files.blueprint[0].basename.replace("." + ctx.files.blueprint[0].extension, "")

    # Declare the output file that will contain the log
    output_file = ctx.actions.declare_file(ctx.attr.unique_identifier + ".txt")

    # Declare the run file which will be executed
    bat = ctx.actions.declare_file(ctx.attr.unique_identifier + ".bat")

    # Path to unreal and the project file
    engine_plus_project_path = "\"" + ctx.executable.engine_executable.path.replace("/", "\\") + "\" " + "%cd%/" + ctx.files.project_file[0].path

    # The command that runs the test
    test_command = " -editortest -Execcmds=\"Automation SetFilter Stress, Automation list, Automation RunTest Project.Blueprints.Compile Blueprints." + blueprint_name + "\""

    #UE Arguments
    arguments = " -unattended -nosplash -nopause -nosplash -nullrhi"

    # Write the command into bat file
    ctx.actions.write(
        output = bat,
        content = engine_plus_project_path + " -abslog=" + "%cd%/" + output_file.path + test_command + arguments + " -testexit=\"Automation Test Queue Empty\"",
        is_executable = True,
    )

    path_to_bat_file = bat.path.replace("/", "\\")
    # Execute the pat file and making sure that the the blueprint we passed in gets flagged as an input so that Bazel detects any changes to it

    ctx.actions.run(
        outputs = [output_file],
        inputs = [ctx.files.blueprint[0]],
        executable = "cmd.exe",
        tools = [bat],
        arguments = ["/C", path_to_bat_file],
    )

    # return the output file so that it can be used in other build steps
    return DefaultInfo(files = depset([output_file]))

compile_blueprint = rule(
    implementation = compile_blueprint_impl,
    attrs = {
        "engine_executable": attr.label(
            allow_single_file = True,
            executable = True,
            cfg = "exec",
        ),
        "project_file": attr.label(
            allow_single_file = True,
        ),
        "blueprint": attr.label(
            allow_single_file = True,
        ),
        "unique_identifier": attr.string(),
    },
)

run_commandlet = rule(
    implementation = run_commandlet_impl,
    attrs = {
        "engine_executable": attr.label(
            allow_single_file = True,
            executable = True,
            cfg = "exec",
        ),
        "project_file": attr.label(
            allow_single_file = True,
        ),
        "commandlet": attr.string(),
        "arguments": attr.string(),
        "asset_files": attr.label_list(allow_files = True),
    },
)
