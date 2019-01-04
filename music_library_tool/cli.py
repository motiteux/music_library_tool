# -*- coding: utf-8 -*-

"""Console script for music_library_tool."""
import sys
from pathlib import Path

import click
import music_library_tool as mlt



@click.command()
@click.argument('lib_input', type=click.Path())
@click.argument('output', type=click.File('w+'))
def cli(lib_input, output):
    """Get the music library path and output metrics.
    \b
        cli path_music_lib output.txt
    """
    path = Path(lib_input)
    for album in path.iterdir():
        if album.is_dir():
            output.write(mlt.get_album_metrics(album))

@click.command()
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
def inout(input, output):
    while True:
        chunk = input.read(1024)
        if not chunk:
            break
        output.write(chunk)


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
