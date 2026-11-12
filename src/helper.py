import json
from pathlib import Path

schema_path = Path(__file__).resolve().parent.parent / "schema" / "artha.schema.json"
with open(schema_path, "r", encoding="utf-8") as f:
    schema_data = json.load(f)

def get_primitive_schema(primitiveName: str):
    '''
        This is a bit crude, I am searching the schema to find the schema for
        the particular node I am visiting. Then I use the schema to find out
        what kind of primitive it is and take the relevant step. In a future change
        I will establish the primitive schemas in definitions and use them, so that
        it can be accessed directly.
    '''
    data = schema_data

    def search(node):
        if isinstance(node, dict):
            if node.get("$id") == f"./{primitiveName}.schema.json":
                return node
            for value in node.values():
                result = search(value)
                if result: return result
        elif isinstance(node, list):
            for item in node:
                result = search(item)
                if result: return result
        return None

    return search(data)