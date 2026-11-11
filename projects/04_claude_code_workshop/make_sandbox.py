"""Copy a clean fixture without overwriting earlier learner work."""

import argparse
from pathlib import Path
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("destination", type=Path)
args = parser.parse_args()
source = Path(__file__).parent / "starter"
shutil.copytree(source, args.destination)
print(f"Created {args.destination}")
