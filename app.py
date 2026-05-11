import runpy
import os
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).parent / "2_Query_Generation_and_Evidence_Retrieval"
PROJECT_APP = PROJECT_DIR / "app.py"

os.chdir(PROJECT_DIR)
sys.path.insert(0, str(PROJECT_DIR))

runpy.run_path(str(PROJECT_APP), run_name="__main__")
