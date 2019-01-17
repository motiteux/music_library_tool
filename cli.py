# -*- coding: utf-8 -*-

"""Console script for music_library_tool."""
import sys
from pathlib import Path

import click
import mutagen


from collections import Counter

from music_library_tool.music.primary import Band, Library
from music_library_tool.music.analysis import compute_all_analysis


@click.command()
@click.argument('lib_input', type=click.Path())
@click.argument('output', type=click.File('w+'))
def cli(lib_input, output):
    """Get the music library path and output metrics.
    \b
        cli path_music_lib output.txt
    """
    path = Path(lib_input)

    library = Library(path)

    for band in path.iterdir():
        if band.is_dir():
            band = Band(band)
            library.bands.append(band)
            output.write(band.to_json())
            output.flush()

    output.write("\n###############   ANOMALY  ###############\n")

    output.write(compute_all_analysis(library))


@click.command()
@click.argument('input_track', type=click.Path())
def test_file(input_track):
    path = Path(input_track)

    file = mutagen.File(path)

    print(file.info is None)


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
