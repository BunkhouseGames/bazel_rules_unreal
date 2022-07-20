def convert_data_validation_to_json_impl(ctx):

    output_file = ctx.actions.declare_file("out.json")
    input_file = ctx.attr.deps[0].files.to_list()[0]

    ctx.actions.run(
        outputs = [output_file],
        inputs = [input_file],
        executable = ctx.executable._build_tool,
        arguments = [input_file.path, output_file.path],
    )

    return DefaultInfo(files=depset([output_file]))

def inject_blueprints_to_build_file_impl(ctx):
    bat = ctx.actions.declare_file("out.bat")
    
    ctx.actions.write(
        output = bat,
        content = "call " + ctx.executable._build_tool.path,
        is_executable = True,
        )
    
    return DefaultInfo(executable=bat)


convert_data_validation_to_json = rule( 
    implementation=convert_data_validation_to_json_impl,
    attrs={
        "deps" : attr.label_list(),
        "_build_tool": attr.label(
            executable = True,
            cfg = "exec",
            default = "//:convert_datavalidation_to_json"
        ),
    }
)

inject_blueprints_to_build_file = rule(
    implementation = inject_blueprints_to_build_file_impl,
    executable = True,
    attrs = {
        "build_file": attr.label(allow_single_file = True),
        "_build_tool": attr.label(
            executable = True,
            cfg = "exec",
            default = "//:add_blueprint_to_build_file"
        ),
    }
)