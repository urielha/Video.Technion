# -*- coding: utf-8 -*-

# pay attention to run python 3!

from urllib.request import urlopen
from time import time
import re
import os
import sys
import io
import ssl
import traceback

import argparse

# -*- coding: utf-8 -*-

# pay attention to run python 3!

from urllib.request import urlopen
from time import time
import re
import os
import sys
import io
import ssl

import argparse

# ~~~~~~~~~~~~~~~~~~ encoding stuff ~~~~~~~~~~~~~~~
# DOESN'T NEEDED: run in console: "chcp 1255" before the script
# sys.stdout = codecs.getwriter('cp1255')(sys.stdout.buffer, 'strict') - didn't work well because the buffering mechanism

# This class is to normalize filenames (such as hebrew) so they won't be scrumbled
# Maybe we don't need this anymore
class stdoutWrapper(io.TextIOWrapper):
    def __init__(self, encoding, error):
        super(stdoutWrapper, self).__init__(sys.stdout.buffer, encoding,
                                            error, newline='\n',
                                            write_through=True)
    def write(self, s):
        super(stdoutWrapper, self).write(s)
        sys.stdout.flush()

sys.stdout = stdoutWrapper('cp1255', 'strict')
# print(sys.stdout.encoding)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getDownloadProgress(startTime, total):
    PROGRESS_STR = u"\tDownloaded: {:7.2f}MB, Total: {:7.2f}MB [{:3.0f}%], Speed: {:7.2f}KB/s [ETA: {:02d}:{:02d}] "
    MAX_REMAIN_SEC = 99*60+59
    totalMB = total/1024/1024

    def getProgress_aux(current):
        current = max(1, current)
        duration = time() - startTime
        duration = max(1, duration)

        downloadedMB = current/1024/1024
        progress = 100 * current / total
        speed = current/1024/duration
        remainSecs = max(0, min(MAX_REMAIN_SEC, duration * (total / current - 1)))
        STR = PROGRESS_STR.format(downloadedMB, totalMB, progress, speed, int(remainSecs / 60), int(remainSecs % 60))
        return STR
    return getProgress_aux

def download(url, toFile):
    print(u"downloading file: {}\n\t-> to: {}".format(url, toFile))

    chunkSize = 1024*4 # Bytes
    printFrequency = 0.2 # Seconds
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1) # don't verify certificate
    response = urlopen(url, context=gcontext)

    totalFileSize, downloaded = response.length, 0.0
    getProgressStr = getDownloadProgress(time(), totalFileSize)
    f = open(toFile, 'wb')
    lastPrint = 0
    while True:
        if time() - lastPrint > printFrequency:
            print(getProgressStr(downloaded), end='\r')
            lastPrint = time()

        buff = response.read(chunkSize)
        if not buff:
            break
        f.write(buff)
        downloaded += len(buff)
    print(getProgressStr(downloaded))
    print(u"finish\n")
    f.close()
    response.close()

def readWeb(url):
    content = ""
    with urlopen(url) as opener:
        content = opener.read().decode()
    return content

def getNumber(txt, bounds, default):
    while True:
        try:
            numberStr = input(u"{} ({}-{}, default is {}): ".format(txt, bounds[0], bounds[1], default))
            number = int(default if not numberStr else numberStr)
        except ValueError:
            print(u"ERROR: Please enter number!")
            continue

        if number < bounds[0] or number > bounds[1]:
            print(u"ERROR: Please enter number from {} to {}".format(bounds[0], bounds[1]))
            continue
        return number


def getRSSUrl(coursePageUrl): 
    RE_COURSE_URL = "https?://([^/]+)/Panopto.*folderID=(?:%22|\")?([a-zA-Z0-9\-]{36})"

    urlComponents = re.match(RE_COURSE_URL, coursePageUrl, re.I)
    if not urlComponents:
        print(u"Could not parse the course url!\n Make sure it looks like this:" + \
                u"\n\thttps://panoptotech.cloud.panopto.eu/Panopto/Pages/Sessions/List.aspx#folderID=3cae3bb8-2422-4955-81db-44b63ecd63de" + \
                u"\n\t(with http OR https at the beginning)")
        return ''
    panoptoUrl = urlComponents.group(1)
    courseId = urlComponents.group(2)
    return "http://{}/Panopto/Podcast/Podcast.ashx?courseid={}&type=mp4".format(panoptoUrl, courseId)


def main(arguments):
    RE_VIDEO_RSS = "<item>\s+<title>([^<]*)</title>.*?<guid>([^<]*)</guid>"
    global WELCOME
    print(WELCOME)

    rssURL = '' if not arguments.courseUrl else getRSSUrl(arguments.courseUrl)
    while not rssURL:
        print(u"\nPlease enter the link to the course (e.g. https://panoptotech.cloud.panopto.eu/Panopto/.../...folderID=**")
        arguments.courseUrl = input(u"> ")
        rssURL = getRSSUrl(arguments.courseUrl)
    
    print("")
    content = readWeb(rssURL)

    files = re.findall(RE_VIDEO_RSS, content, re.DOTALL)
    length = len(files)
    startIndex = arguments.startIndex if arguments.startIndex > 0 else getNumber("Start download from", (1, length), 1)
    stopIndex = arguments.endIndex if arguments.endIndex > 0 else getNumber("Download till", (startIndex, length), length)
    outputDir = arguments.outputDir if arguments.outputDir else input("Output directory (press Enter for current dir: {}) ".format(os.getcwd()))
    prefix = arguments.prefix if arguments.prefix else input("Add prefix to the files? (press Enter for none) ") or ""

    # Start downloading!
    for f in files[startIndex - 1 : stopIndex]:
        dest = os.path.join(outputDir, u"{}{}.mp4".format(prefix, f[0]))
        download(f[1], dest)

WELCOME = u"Welcome to Panopto downloader!\n[Home page: https://github.com/urielha/Video.Technion]"
EPILOG = u"Written by Uriel"
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=WELCOME, epilog=EPILOG)
    parser.add_argument('courseUrl',
                        nargs='?', default='', help='the url of the Course in the Panopto (should contain "folderID")')
    parser.add_argument('-p', '--prefix',
                        required=False, dest='prefix', default='', help='prefix of the filename')
    parser.add_argument('-s', '--startIndex',
                        required=False, dest='startIndex', metavar='NUM', default=0, type=int,
                        help='index of the first video to download')
    parser.add_argument('-e', '--endIndex',
                        required=False, dest='endIndex', metavar='NUM', default=0, type=int,
                        help='index of the last video')
    parser.add_argument('-o', '--output',
                        required=False, dest='outputDir', metavar='OUTPUT_DIR', default='',
                        help='output directory')
    arguments = parser.parse_args()
    
    try:
        main(arguments)
    except Exception as ex:
        traceback.print_exc()
    input('Press Enter to continue...')
