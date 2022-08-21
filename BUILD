load("@rules_pkg//pkg:zip.bzl", "pkg_zip")
load("@rules_python//python:defs.bzl", "py_binary")
load("@pip_install_package//:requirements.bzl", "requirement")

pkg_zip(
    name = "SentinelCLI_Pak",
    srcs = ["//tools:SentinelCLI"],
)

py_binary(
  name = "deploy_pak",
  srcs = ["deploy_pak.py"],
  deps = [requirement("Click")],
)
