"""
Genera un reporte comparativo basico.
"""

from pathlib import Path

from reports import build_markdown_report


def main():
    output_dir = Path("experiments/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_markdown_report({"status": "pending"})
    (output_dir / "comparison_report.md").write_text(report, encoding="utf-8")
    print("Reporte generado en experiments/results/comparison_report.md")


if __name__ == "__main__":
    main()
