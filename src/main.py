
import sys
import json
import requests
from pathlib import Path
from Synthesizer import Synthesizer

def fetchLatestSchema(root_dir):
    '''
        Fetch the latest schema from the server.
    '''
    url = "https://vishalpalaniappan.github.io/artha-primitives/img/artha.schema.json"
    save_path = root_dir / "schema" / "artha.schema.json"

    save_path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    # Save to disk
    save_path.write_bytes(response.content)
    print(f"Saved schema to: {save_path}")
    
    return json.loads(response.content)


def main(argv):
    '''
        Fetch the schema, read the narrative and run the synthesizer.
    '''
    root_dir = Path(__file__).resolve().parent.parent

    # Fetch the latest schema
    schema = fetchLatestSchema(root_dir)

    # Read the narrative
    with open(root_dir / "narratives" / "coffee_shop.json", "r") as f:
        arthaIR = json.loads(f.read())

    synthesizer = Synthesizer(arthaIR, schema)
    synthesizer.generateOutput()

    print("Finished synthesizing narrative.")

if "__main__" == __name__:
    sys.exit(main(sys.argv))
