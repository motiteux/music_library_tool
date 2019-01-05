# -*- coding: utf-8 -*-

"""Main module."""

from abc import ABCMeta, abstractmethod
from .utils import list_formatter


def compile_band_metrics(band_path):
    """Compile all information and quality metrics for a band.

       Keyword arguments:
        band_path -- pathlib.Path to the directory holding all albums of a band
    """
    band = Band(band_path)
    report_band_header = band
    report_band = report_band_header

    return report_band


class MusicItemBase(metaclass=ABCMeta):
    def __init__(self, path):
        self.path = path
        self.name = path.name
        self.items = []
        self._set_items()

    def _set_items(self):
        for item in self.path.iterdir():
            if item.is_dir():
                self.items.append(item.name)

    @abstractmethod
    def __repr__(self):
        pass


class Band(MusicItemBase):
    def __init__(self, path_band):
        super().__init__(path_band)

    def __repr__(self):
        return "Band: {artist} and its albums: {albums}".format(artist=self.name,
                                                                albums=list_formatter(self.items, "albums"))


class Album(MusicItemBase):
    def __init__(self, path_band):
        super().__init__(path_band)
