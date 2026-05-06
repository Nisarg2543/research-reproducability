import os
import sys
from pathlib import Path

import click
from rich.console import Console

console = Console()


@click.command()
@click.option("--path", default=".", show_default=True, help="Directory to audit")
@click.option("--output", default=None, help="Write report to this file (.md, .json, or .pdf)")
@click.option("--fix", is_flag=True, help="Auto-generate missing environment and documentation files")
@click.version_option(package_name="repro-check")
def main(path, output, fix):
    """Audit a research codebase for reproducibility issues."""
    from repro.checker import ReproChecker
    from repro.report import print_report, write_markdown, write_json, write_pdf

    target = Path(path).resolve()

    if not target.exists():
        console.print(f"[red]Error: Path does not exist: {path}[/red]")
        sys.exit(1)
    if not target.is_dir():
        console.print(f"[red]Error: Expected a directory, got a file: {path}[/red]")
        sys.exit(1)

    try:
        checker = ReproChecker(str(target))
        report = checker.run()
    except PermissionError as e:
        console.print(f"[red]Permission denied: {e}[/red]")
        if os.environ.get("REPRO_DEBUG"):
            raise
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[dim]Audit cancelled.[/dim]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        console.print("[dim]Set REPRO_DEBUG=1 for full traceback.[/dim]")
        if os.environ.get("REPRO_DEBUG"):
            raise
        sys.exit(1)

    print_report(report)

    if output:
        try:
            if output.endswith(".pdf"):
                write_pdf(report, output)
            elif output.endswith(".json"):
                write_json(report, output)
            else:
                write_markdown(report, output)
        except OSError as e:
            console.print(f"[red]Could not write output file: {e}[/red]")
            if os.environ.get("REPRO_DEBUG"):
                raise
            sys.exit(1)

    if fix:
        from repro.fixer import ReproFixer
        fixer = ReproFixer(target, report)
        generated = fixer.run()
        if generated:
            console.print(f"\n[green]Generated {len(generated)} file(s):[/green]")
            for f in generated:
                console.print(f"  [dim]+ {f}[/dim]")
            console.print("[dim]Review each file before committing.[/dim]")
        else:
            console.print("\n[dim]Nothing to fix — all files already present.[/dim]")


if __name__ == "__main__":
    main()
