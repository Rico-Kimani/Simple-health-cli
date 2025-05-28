import typer
from myapp.db import Base, engine
from myapp.cli import app  # CLI app from cli.py

cli = typer.Typer()

@cli.command()
def init_db():
    """Initialize the database and create tables."""
    Base.metadata.create_all(bind=engine)
    typer.echo("✅ Database tables created.")

cli.add_typer(app)

if __name__ == "__main__":
    cli()
