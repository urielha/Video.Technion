import sys
from cx_Freeze import setup, Executable
from os import path

scriptPath = path.dirname(path.realpath(__file__))
scriptPath = path.join(scriptPath, '..', 'download_panopto.py')

setup(  name = "download_panopto",
        version = "2.0",
        description = "Download videos from Technion Panopto",
        executables = [Executable(scriptPath)])