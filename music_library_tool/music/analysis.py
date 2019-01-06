# -*- coding: utf-8 -*-

import json

from mutagen import File


def get_album_with_long_track(library):
    long_tracks = []
    for band in library.bands:
        for album in band.albums:
            for track in album.tracks:
                file = File(track.path)
                if file.info.length > 1500:
                    long_tracks.append({"band": track.band, "album": track.album})
                    break

    return json.dumps(long_tracks, default=lambda o: o.__dict__, sort_keys=True, indent=4)
