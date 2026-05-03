"""iakg — root Click group."""

import click

from .cmd_download import download
from .cmd_ingest import ingest


@click.group()
def cli() -> None:
    """iakg — download and ingest Internet Archive books as knowledge graphs."""


cli.add_command(download)
cli.add_command(ingest)
