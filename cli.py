# -*- coding: utf-8 -*-

"""Console script for music_library_tool."""
import sys
from pathlib import Path

import click

from music_library_tool.libtool import compile_band_metrics


@click.command()
@click.argument('lib_input', type=click.Path())
@click.argument('output', type=click.File('w+'))
def cli(lib_input, output):
    """Get the music library path and output metrics.
    \b
        cli path_music_lib output.txt
    """
    path = Path(lib_input)

    reports = []
    for band in path.iterdir():
        if band.is_dir():

            reports.append('#######\n{0}'.format(compile_band_metrics(band)))

    output.write('\n'.join(reports))


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
