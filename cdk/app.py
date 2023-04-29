#!/usr/bin/env python3
import aws_cdk as cdk
from cdk.cdk_stack import CdkStack
from resource_registry import registry, serialization

registry_args_description = {
    "deployment_id": "identifies a unique deployment of a specific service",
    "resource_name": "name of the resource",
}
registry_file_path = "./resource_names"
serializer = serialization.YamlSerializer()

name_registry = registry.NameRegistry(
    registry_args_description, {"deployment_id": "test_deployment"}
)
app = cdk.App()
CdkStack(
    app,
    "CdkStack",
    name_registry,
    env=cdk.Environment(region="eu-central-1"),
)

app.synth()
name_registry.serialize(registry_file_path, serializer)
