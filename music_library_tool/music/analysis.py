# -*- coding: utf-8 -*-

import json
from collections import OrderedDict

from mutagen import File


def compute_all_analysis(library):
    report_long_track = list_albums_with_songs_longer_than_25min(library)
    return report_long_track


def get_stats_album(library):
    count_band = 0
    count_album = 0
    count_track = 0
    test = 'dfsfsd'
    print(str(test))
    for band in library.bands:
        count_band += 1
        for album in band.albums:
            count_album += 1
            for _ in album.tracks:
                count_track += 1
    return


def list_albums_with_songs_longer_than_25min(library):
    long_tracks = OrderedDict({"issue_type": "long_tracks"})

    albums =[]
    for band in library.bands:
        for album in band.albums:
            for track in album.tracks:
                file = File(track.path)
                if file.info.length > 1500:
                    albums.append({"band": track.band, "album": track.album})
                    break

    long_tracks.update({"album": albums})
    return json.dumps(long_tracks, indent=4)


def list_albums_with_less_than_5_songs(library):
    return {}


def list_albums_with_no_metadata(library):
    """no album title or no band information"""
    return {}
