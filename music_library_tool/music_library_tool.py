# -*- coding: utf-8 -*-

"""Main module."""


def get_album_metrics(album_path):
    report_json = list()
    report_json.append('{0}'.format(album_path.name))

    print(report_json)

    return '\n'.join(report_json)
