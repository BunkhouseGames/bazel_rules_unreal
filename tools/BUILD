load("@rules_python//python:defs.bzl", "py_binary")
load("@pip_install_package//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_binary(
  name = "SentinelCLI",
  srcs = ["SentinelCLI.py"],
  deps = [requirement("Click")]
)
