"""Execute and save the Stage 2 evaluation notebook with this interpreter."""
from pathlib import Path
import sys

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

root = Path(__file__).resolve().parent
path = root / "stage_2_evaluation_and_analysis.ipynb"
notebook = nbformat.read(path, as_version=4)
manager = KernelManager(kernel_name="python3")
manager.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
client = NotebookClient(notebook, km=manager, timeout=600,
                        resources={"metadata": {"path": str(root)}})
client.on_cell_executed = lambda cell_index, **kwargs: print(
    f"Executed cell {cell_index}", flush=True)
try:
    client.execute(cleanup_kc=True)
finally:
    nbformat.write(notebook, path)
print(f"Saved executed notebook: {path}")
