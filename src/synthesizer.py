import ast
import sys
import json
from pathlib import Path
from helper import get_primitive_schema

def main(argv):
    # Read the narrative
    root_dir = Path(__file__).resolve().parent.parent
    narrative_dir = root_dir / "narratives"
    with open(narrative_dir / "coffee_shop.json", "r") as f:
        narrative = f.read()

    # Test accessing schema
    found = get_primitive_schema("import")
    print(found)

if "__main__" == __name__:
    sys.exit(main(sys.argv))
