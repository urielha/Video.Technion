from distutils.core import setup
import py2exe
from os import path

scriptPath = path.dirname(path.realpath(__file__))
setup(console=[path.join(scriptPath, '..', 'download_panopto.py')])
