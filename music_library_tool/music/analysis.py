# -*- coding: utf-8 -*-

from music_library_tool.music.primary import is_music_file

import re
import json
import datetime
from collections import OrderedDict

from pathlib import Path

from mutagen import File
from mediafile import MediaFile


def _pretty_print_duration(duration_seconds):
    return datetime.timedelta(seconds=duration_seconds)


def compute_all_analysis(library):
    report_anomaly = OrderedDict()
    report_anomaly.update(list_albums_with_songs_longer_than_25min(library))
    report_anomaly.update(list_albums_with_less_than_5_songs(library))
    report_anomaly.update(list_albums_with_subfolders(library))
    report_anomaly.update(list_albums_with_no_metadata(library))
    report_anomaly.update(list_albums_no_flac(library))
    report_anomaly.update(list_filename_not_compliant(library))
    report_anomaly.update(list_corrupted_files(library))

    return json.dumps(report_anomaly, indent=4, ensure_ascii=False)


def get_stats_album(library):
    count_band = 0
    count_album = 0
    count_track = 0

    for band in library.bands:
        count_band += 1
        for album in band.albums:
            count_album += 1
            for _ in album.tracks:
                count_track += 1
    return


def list_albums_with_songs_longer_than_25min(library):
    albums = {}
    count = 0

    for band in library.bands:
        no_album = True
        albums.update({band.name: {}})

        for album in band.albums:
            no_track = True
            albums[band.name].update({album.name: {}})

            for track in album.tracks:
                file = File(track.path)

                if file.info.length > 1500:
                    count += 1
                    albums[band.name][album.name].update({
                        track.name: str(_pretty_print_duration(file.info.length))
                                })
                    no_track = False
                    no_album = False

            if no_track:
                del albums[band.name][album.name]

        if no_album:
            del albums[band.name]

    long_tracks = {"long_tracks": {"count": count, "albums": albums}}

    return long_tracks


def list_albums_with_less_than_5_songs(library):
    albums = {}
    count = 0

    for band in library.bands:
        no_album = True
        albums.update({band.name: []})

        for album in band.albums:

            if len(album.tracks) < 5:
                count += 1
                albums[band.name].append(album.name)
                no_album = False

        if no_album:
            del albums[band.name]

    short_albums = {"short_albums": {"count": count, "albums": albums}}
    return short_albums


def list_albums_with_subfolders(library):
    albums = {}
    count = 0

    for band in library.bands:
        no_album = True
        albums.update({band.name: []})

        for album in band.albums:
            path = Path(album.path)
            for item in path.iterdir():
                if item.is_dir():
                    count += 1
                    albums[band.name].append(album.name)
                    no_album = False
                    break

        if no_album:
            del albums[band.name]

    short_albums = {"subfolder_albums": {"count": count, "albums": albums}}
    return short_albums


def list_albums_with_unavailable_extensions(library):
    unavailable_extensions_albums = OrderedDict({"issue_type": "albums_with_unavailable_extensions"})
    
    list_unavailable_extensions = ["m4a", "wma"]

    albums = []
    for band in library.bands:
        for album in band.albums:
            for track in album.tracks:
                if track.name[-3:] in list_unavailable_extensions:
                    albums.append({"band": band.name, "album": album.name})
                    break

    unavailable_extensions_albums.update({"album": albums})
    return unavailable_extensions_albums


def list_albums_with_no_metadata(library):
    """no album title or no band information"""
    required_fields = ['title', 'album', 'artist', 'year', 'genre',
                       'images', 'length']

    albums = {}
    count = 0

    for band in library.bands:
        no_album = True
        albums.update({band.name: {}})

        for album in band.albums:
            no_track = True
            albums[band.name].update({album.name: {}})

            for track in album.tracks:
                file = MediaFile(track.path)

                values = [getattr(file, field) for field in required_fields]

                if None in values:
                    count += 1
                    albums[band.name][album.name].update({
                                    track.name: {
                                        "id title": file.title,
                                        "id album": file.album,
                                        "id artist": file.artist,
                                        "id genre": file.genre,
                                        "id year": file.year,
                                        "id images": len(file.images)
                                    }
                                })
                    no_track = False
                    no_album = False

            if no_track:
                del albums[band.name][album.name]

        if no_album:
            del albums[band.name]

    no_metadata_albums = {"no_metadata_albums": {"count":count, "albums": albums}}
    return no_metadata_albums


def list_albums_no_flac(library):
    albums = {}
    count = 0

    for band in library.bands:
        no_album = True
        albums.update({band.name: {}})

        for album in band.albums:
            no_track = True
            albums[band.name].update({album.name: {}})

            for track in album.tracks:
                file = MediaFile(track.path)

                if file.format != "FLAC":
                    count += 1
                    albums[band.name][album.name].update({
                                    track.name: file.format
                                })
                    no_track = False
                    no_album = False

            if no_track:
                del albums[band.name][album.name]

        if no_album:
            del albums[band.name]

    no_flac_albums = {"no_flac_albums": {"count": count, "albums": albums}}
    return no_flac_albums


def list_filename_not_compliant(library):
    albums = {}
    count = 0

    filename_pattern = re.compile('^\d+ - (.*)\.(.*)$')

    for band in library.bands:
        no_album = True
        albums.update({band.name: {}})

        for album in band.albums:
            no_track = True
            albums[band.name].update({album.name: []})

            for track in album.tracks:
                if not filename_pattern.match(track.name):
                    count += 1
                    albums[band.name][album.name].append(track.name)
                    no_track = False
                    no_album = False

            if no_track:
                del albums[band.name][album.name]

        if no_album:
            del albums[band.name]

    no_flac_albums = {"filename_not_compliant_albums": {"count": count, "albums": albums}}
    return no_flac_albums


def list_corrupted_files(library):
    albums = {}
    count = 0

    for band in library.bands:
        no_album = True
        albums.update({band.name: {}})

        for album in band.albums:
            no_track = True
            albums[band.name].update({album.name: []})

            for track in album.tracks:

                if not is_music_file(track.path):
                    count += 1
                    albums[band.name][album.name].append(track.name)
                    no_track = False
                    no_album = False

            if no_track:
                del albums[band.name][album.name]



    corrupted_file_albums = {"corrupted_file_albums": {"count": count, "albums": albums}}
    return corrupted_file_albums


def detect_duplicates(library):
    pass

analysis_type = {
    "long_tracks": list_albums_with_songs_longer_than_25min,
    "short_albums": list_albums_with_less_than_5_songs,
    "no_metadata_albums": list_albums_with_no_metadata,
    "no_flac_albums": list_albums_no_flac,
    "filename_not_compliant_albums": list_filename_not_compliant,
    "corrupted_file_albums": list_corrupted_files
}


def run_all(configs, library):
    albums = {}
    count = 0

    for band in library.bands:
        no_album = True
        albums.update({band.name: {}})

        for album in band.albums:
            no_track = True
            albums[band.name].update({album.name: {}})

            for config in configs:
                analysis_type[config](album)


        if no_album:
            del albums[band.name]


    return
