"""Config Reader to read test data from JSON."""
import os
import json


def load_env_variable(key):
    """Read data from the settings.json file.

    parameters:
        :param key: The property name (key) to load

    Returns:
        Response: Value of property (key).
    """
    settings = None
    with open(os.path.join(
        os.path.dirname(os.path.abspath(__file__)
                        ), 'setting.json')) as f:
        settings = json.load(f)

    return settings[key]


def load_schema(value):
    """Load json schema from schema definition file.

    parameters:
        :param value: The schema name to load

    Returns:
        Response: schema
    """
    schema = None
    with open(os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'schema.json')) as f:
        schema = json.load(f)

    return schema[value]
