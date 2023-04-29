def resolve_physical_id(cdk_resource_construct, cdk_stack) -> str:
    node = cdk_resource_construct.node.default_child
    return cdk_stack.resolve((node.logical_id))
