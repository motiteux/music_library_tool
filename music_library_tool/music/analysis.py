# -*- coding: utf-8 -*-

import json
from collections import OrderedDict

from mutagen import File
from mediafile import MediaFile


def compute_all_analysis(library):
    report_anomaly = list_albums_with_songs_longer_than_25min(library)
    report_anomaly.update(list_albums_with_less_than_5_songs(library))
    report_anomaly.update(list_albums_with_no_metadata(library))

    return json.dumps(report_anomaly)


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
    long_tracks = OrderedDict({"issue_type": "long_tracks"})

    albums = []
    for band in library.bands:
        for album in band.albums:
            for track in album.tracks:
                file = File(track.path)
                if file.info.length > 1500:
                    albums.append({"band": track.band, "album": track.album})
                    break

    long_tracks.update({"album": albums})
    return long_tracks


def list_albums_with_less_than_5_songs(library):
    short_albums = OrderedDict({"issue_type": "short_albums"})

    albums = []
    for band in library.bands:
        for album in band.albums:
            if len(album.tracks) < 5:
                albums.append({"band": band, "album": album})
                break

    short_albums.update({"album": albums})
    return short_albums


def list_albums_with_no_metadata(library):
    """no album title or no band information"""
    no_metadata_albums = OrderedDict({"issue_type": "no_metadata_albums"})

    required_fields = ['title', 'album', 'artist', 'albumartist', 'length']

    albums = []
    for band in library.bands:
        for album in band.albums:
            for track in album.tracks:
                file = MediaFile(track.path)

                fields = file.fields()

                if not len([value for value in fields if value in required_fields]):
                    albums.append({"band": band, "album": album})
                    break

    no_metadata_albums.update({"album": albums})
    return no_metadata_albums
