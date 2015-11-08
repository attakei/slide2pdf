# -*- coding:utf8 -*-
"""Capturing engins
"""
import os
import logging
import importlib
import shutil
from .. import errors
from ..webresources import WebResource


Logger = logging.getLogger('deck2pdf.captures')

TEMP_CAPTURE_DIR = '.deck2pdf'


def find_engine(name):
    try:
        import_ = importlib.import_module('.{}'.format(name), 'deck2pdf.captures')
        return import_.CaptureEngine
    except ImportError:
        return None


class CaptureEngine(object):
    """Slide capturing engine (abstract)
    """
    def __init__(self, url):
        self._web_resource = WebResource(url)
        self._slide_captures = []

    @property
    def url(self):
        return self._web_resource.url

    @property
    def save_dir(self):
        current_dir = os.path.abspath(os.getcwd())
        return os.path.join(current_dir, TEMP_CAPTURE_DIR)

    def capture_all(self):
        """Capture all pages of slide
        """
        raise NotImplementedError()

    def capture_page(self, page_options):
        """Capture per page of slide, and save as pdf
        """
        raise NotImplementedError()

    def start(self):
        shutil.rmtree(self.save_dir, True)
        os.makedirs(self.save_dir)
        self._web_resource.init()

    def end(self):
        pass