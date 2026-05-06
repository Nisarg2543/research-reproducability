import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich import box

from .checker import ReproReport, Issue

console = Console()

SEVERITY_COLOR = {
    "critical": "bold red",
    "high": "red",
    "medium": "yellow",
    "low": "dim",
}

SEVERITY_ICON = {
    "critical": "✗",
    "high": "⚠",
    "medium": "~",
    "low": "·",
}


def print_report(report: ReproReport):
    score = report.score
    score_color = "green" if score >= 80 else "yellow" if score >= 50 else "red"

    console.print()
    console.print(Panel(
        f"[bold]Reproducibility Audit[/bold]\n"
        f"Path: {report.path}\n"
        f"Score: [{score_color}]{score}/100[/{score_color}]",
        box=box.ROUNDED,
    ))

    if not report.issues:
        console.print("[green]✓ No issues found. This codebase looks reproducible![/green]")
        return

    for severity in ["critical", "high", "medium", "low"]:
        issues = report.by_severity(severity)
        if not issues:
            continue

        color = SEVERITY_COLOR[severity]
        icon = SEVERITY_ICON[severity]
        console.print(f"\n[{color}]{icon} {severity.upper()} ({len(issues)})[/{color}]")

        for issue in issues:
            console.print(f"  [{color}]{issue.category}[/{color}] — {issue.file}")
            console.print(f"    {issue.message}")
            console.print(f"    [dim]Fix: {issue.fix}[/dim]")

    console.print()


def write_markdown(report: ReproReport, output_path: str):
    lines = [
        f"# Reproducibility Audit Report",
        f"",
        f"**Path**: `{report.path}`  ",
        f"**Score**: {report.score}/100",
        f"",
    ]

    if not report.issues:
        lines.append("No issues found. ✓")
    else:
        for severity in ["critical", "high", "medium", "low"]:
            issues = report.by_severity(severity)
            if not issues:
                continue
            icon = SEVERITY_ICON[severity]
            lines.append(f"## {icon} {severity.capitalize()} Issues\n")
            for issue in issues:
                lines.append(f"**{issue.category}** — `{issue.file}`  ")
                lines.append(f"{issue.message}  ")
                lines.append(f"*Fix: {issue.fix}*\n")

    Path(output_path).write_text("\n".join(lines))
    console.print(f"[green]Report written to {output_path}[/green]")


def write_json(report: ReproReport, output_path: str):
    data = {
        "path": report.path,
        "score": report.score,
        "issues": [
            {
                "severity": i.severity,
                "category": i.category,
                "file": i.file,
                "message": i.message,
                "fix": i.fix,
            }
            for i in report.issues
        ],
    }
    Path(output_path).write_text(json.dumps(data, indent=2))
    console.print(f"[green]Report written to {output_path}[/green]")


def write_pdf(report: ReproReport, output_path: str):
    if not shutil.which("pandoc"):
        console.print("[yellow]pandoc not found — writing Markdown instead.[/yellow]")
        md_path = output_path.replace(".pdf", ".md")
        write_markdown(report, md_path)
        return
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False) as f:
        tmp_md = f.name
    write_markdown(report, tmp_md)
    result = subprocess.run(
        ["pandoc", tmp_md, "-o", output_path],
        capture_output=True,
        text=True,
    )
    Path(tmp_md).unlink(missing_ok=True)
    if result.returncode != 0:
        console.print(f"[red]pandoc error: {result.stderr}[/red]")
    else:
        console.print(f"[green]Report written to {output_path}[/green]")
