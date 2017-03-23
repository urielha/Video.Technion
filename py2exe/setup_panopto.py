from distutils.core import setup
import py2exe
from os import path

setup(console=[path.join('..', 'download_panopto.py')])