def get_project_overview_impl(ctx):

    output_file = ctx.actions.declare_file("project_overview.json")
    input_file = ctx.attr.deps[0].files.to_list()[0]

    ctx.actions.run(
        outputs = [output_file],
        inputs = [input_file],
        executable = ctx.executable._build_tool,
        arguments = [input_file.path, output_file.path],
    )

    return DefaultInfo(files=depset([output_file]))

def inject_blueprints_to_build_file_impl(ctx):
    output_file = ctx.actions.declare_file("generated_buildfile_blueprints.txt")

    ctx.actions.run(
        outputs = [output_file],
        inputs = [ctx.file.project_overview_file],
        executable = ctx.executable._build_tool,
        arguments = [ctx.attr.project_folder_name, ctx.file.project_overview_file.path, output_file.path]
    )

    return DefaultInfo(files=depset([output_file]))


get_project_overview = rule( 
    implementation=get_project_overview_impl,
    attrs={
        "deps" : attr.label_list(),
        "_build_tool": attr.label(
            executable = True,
            cfg = "exec",
            default = "//tools:parse_data_validation"
        ),
    }
)

inject_blueprints_to_build_file = rule(
    implementation = inject_blueprints_to_build_file_impl,
    attrs = {
        "_build_tool": attr.label(
            executable = True,
            cfg = "exec",
            default = "//tools:parse_data_validation"
        ),
        "project_folder_name" : attr.string(),
        "project_overview_file" : attr.label(allow_single_file=True),
    }
)