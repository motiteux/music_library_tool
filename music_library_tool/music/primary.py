# -*- coding: utf-8 -*-


from abc import ABCMeta
from pathlib import Path
import json

from pprint import pprint

import mutagen


def is_music_file(track):
    try:
        file = mutagen.File(track)
    except mutagen.MutagenError:
        return False
    return file is not None


class Library(object):
    def __init__(self, path):
        self.path = str(path)
        self.bands = []


class LibraryItemBase(metaclass=ABCMeta):
    def __init__(self, path, name):
        self.path = str(path)
        self.name = str(name)

    def __str__(self):
        return u'{0}:\n{1}'.format(self.__class__.__name__, self.to_json())

    def __repr__(self):     # must be unambiguous
        return repr(str(self))

    def to_json(self):
        try:
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        except AttributeError as err:
            print(self.__dict__)


class Band(LibraryItemBase):
    def __init__(self, path, name):
        super(Band, self).__init__(path, name)
        self.albums = self._set_items()

    def _set_items(self):
        path = Path(self.path)
        items = []

        for item in path.iterdir():
            if item.is_dir():
                items.append(Album(item, item.name, band=self.name))

        return items


class Album(LibraryItemBase):
    def __init__(self, path, name, band=None):
        super(Album, self).__init__(path, name)
        self.band = band
        self.tracks = self._set_items()

    def _set_items(self):
        path = Path(self.path)
        items = []

        for item in path.iterdir():
            if item.is_file() and is_music_file(item):
                items.append(Track(item, item.name, album=self.name, band=self.band))

        return items


class Track(LibraryItemBase):
    def __init__(self, path, name, album=None, band=None):
        super(Track, self).__init__(path, name)
        self.band = band
        self.album = album

        # try:
        #     self.id3 = mutagen.easyid3.EasyID3(self.path)
        # except mutagen.id3._util.ID3NoHeaderError as err:
        #     self.id3 = {}
