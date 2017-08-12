# -*- coding: utf-8 -*-

# pay attention to run python 3!

from urllib.request import urlopen
import re
import os 
import sys
import io 

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

def download(url, toFile):
	print(toFile)
	print(u"downloading file: {}\n\t-> to: {}".format(url, toFile))
	chunkSize = 1024*512
	response = urlopen(url)
	f = open(toFile, 'wb')
	while True:
		buff = response.read(chunkSize)
		if not buff:
			break
		f.write(buff)
	print(u"finish")
	f.close()
	response.close()

def readWeb(url):
	content = ""
	with urlopen(url) as opener:
		content = opener.read().decode()
	return content

def getNumber(txt, bounds):
	while(True):
		try:
			number = int(input(u"{} ({}-{}):".format(txt, bounds[0], bounds[1])))
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
	return "http://%s/Panopto/Podcast/Podcast.ashx?courseid=%s&type=mp4" % (panoptoUrl, courseId)


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
	startIndex = arguments.startIndex if arguments.startIndex > 0 else getNumber("start download from", (1,length))
	stopIndex = arguments.endIndex if arguments.endIndex > 0 else getNumber("download till", (startIndex, length))
	prefix = arguments.prefix if arguments.prefix else input("Add prefix to the file? (press enter for none) ") or ""
	outputDir = arguments.outputDir

	for f in files[startIndex - 1 : stopIndex]:
		dest = os.path.join(outputDir, u"{}{}.mp4".format(prefix, f[0]))
		download(f[1], dest)

WELCOME = u"Welcome to Panopto downloader!\n[Home page: https://github.com/urielha/Video.Technion]"
EPILOG = u"Written by Uriel"
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=WELCOME, epilog=EPILOG)
	parser.add_argument('courseUrl', nargs='?', default='', help='the url of the Course in the Panopto (should contain "folderID")')
	parser.add_argument('-p', '--prefix', required=False, dest='prefix', default='', help='prefix of the filename')
	parser.add_argument('-s', '--startIndex', required=False, dest='startIndex', metavar='NUM', default=0, type=int, help='index of the first video to download (default is the very first one)')
	parser.add_argument('-e', '--endIndex', required=False, dest='endIndex', metavar='NUM', default=0, type=int, help='index of the last video (default is to download till the last one)')
	parser.add_argument('-o', '--output', required=False, dest='outputDir', metavar='OUTPUT_DIR', default='.', help='output directory (default is current)')
	arguments = parser.parse_args()
	
	try:
		main(arguments)
	except Exception as ex:
		print(ex)
	input("Press Enter to continue...")
