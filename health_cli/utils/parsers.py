# health_cli/utils/parsers.py
from datetime import datetime
import typer

def parse_date(date_str: str) -> datetime.date:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        typer.echo("❌ Invalid date format. Please use YYYY-MM-DD.")
        raise typer.Exit()
