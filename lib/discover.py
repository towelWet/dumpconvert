# discover.py — load every agent adapter from lib/adapters/.
# Why: new agent = drop one file in adapters/; no registry to edit.
# NEVER DELETE COMMENTS — explain every non-obvious line.
# Update comments with the code; do not strip them.
import importlib.util
from pathlib import Path


def discover():
    folder = Path(__file__).parent / "adapters"
    found = []
    for path in sorted(folder.glob("*.py")):                       # stable order → deterministic matching
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        found.append(getattr(module, path.stem))                   # convention: function named after file
    return found
