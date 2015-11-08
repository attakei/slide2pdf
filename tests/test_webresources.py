# -*- coding:utf8 -*-
"""
"""
from __future__ import unicode_literals
from deck2pdf import webresources, errors
from pytest import raises
from . import test_dir


__author__ = 'attakei'


def test_resolve_path():
    from deck2pdf.webresources import resolve_path
    assert resolve_path('http://example.com') == 'http://example.com'
    assert resolve_path('https://example.com') == 'https://example.com'
    assert resolve_path('tests/testslide/index.rst') == 'file://{}/{}'.format(test_dir, 'testslide/index.rst')
    raises(errors.ResourceNotFound, resolve_path, ('not_found'))


class WebResourceTests(object):
    def test_not_found(self):
        raises(errors.ResourceNotFound, webresources.WebResource, (__file__+'not_found'))

    def test_is_local(self):
        res = webresources.WebResource(__file__)
        assert res.is_local
        assert res.url.startswith('file://')
