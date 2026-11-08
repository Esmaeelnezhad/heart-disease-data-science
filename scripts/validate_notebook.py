"""Execute the canonical notebook from a clean kernel; fail on errors or missing outputs."""

from pathlib import Path
import shutil
from tempfile import TemporaryDirectory

import nbformat
from nbclient import NotebookClient


root = Path(__file__).resolve().parents[1]
path = root / "heart_disease.ipynb"
notebook = nbformat.read(path, as_version=4)
nbformat.validate(notebook)
expected_reports = {
    "cv_results.csv", "test_metrics.csv", "site_validation.csv", "subgroups.csv",
    "permutation_importance.csv", "summary.png", "evaluation.png",
    "distributions.png", "feature_importance.png",
}
# A fresh directory prevents committed reports from hiding missing output generation.
with TemporaryDirectory(prefix="heart-disease-validation-") as directory:
    run_root = Path(directory)
    shutil.copy2(root / "heart_disease_uci.csv", run_root)
    NotebookClient(
        notebook, timeout=600, kernel_name="python3",
        resources={"metadata": {"path": str(run_root)}},
    ).execute()
    for name in expected_reports:
        report = run_root / "reports" / name
        assert report.is_file() and report.stat().st_size > 0, f"Missing or empty report: {name}"
    shutil.copytree(run_root / "reports", root / "reports", dirs_exist_ok=True)
code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
assert code_cells and all(cell.execution_count is not None for cell in code_cells)
assert not any(output.output_type == "error" for cell in code_cells for output in cell.outputs)
nbformat.write(notebook, path)
print(f"Validated and executed {len(code_cells)} code cells: {path.name}")
