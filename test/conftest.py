# test/conftest.py

import sys
from pathlib import Path

# Add the project root to PYTHONPATH for all tests
root = Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))
