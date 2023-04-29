from resource_registry import registry
import app


def test_output_registry_can_be_read():
    test_registry = registry.NameRegistry(app.registry_args_description)

    test_registry.parse(app.registry_file_path, app.serializer)

    assert "CdkQueue" in test_registry.retrieve(
        {"deployment_id": "test_deployment", "resource_name": "CdkQueue"}
    )
