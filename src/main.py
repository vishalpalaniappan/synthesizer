
import sys
from pathlib import Path
from Synthesizer import Synthesizer

def main(argv):
    # Read the narrative
    root_dir = Path(__file__).resolve().parent.parent
    narrative_dir = root_dir / "narratives"
    with open(narrative_dir / "coffee_shop.json", "r") as f:
        narrative = f.read()

    synthesizer = Synthesizer()
    synthesizer.generateOutput()

if "__main__" == __name__:
    sys.exit(main(sys.argv))
