# -*- coding: utf-8 -*-

# pay attention to run python 3!

from urllib.request import urlopen
import re
import os 
import sys
import io 

# import argparse

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

def download(url, toFile):
	print(toFile)
	print(u"downloading file: %s\n\t-> to: %s" % (url, toFile))
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
			number = int(input(u"%s (%d-%d):" % (txt, bounds[0], bounds[1])))
		except ValueError:
			print(u"ERROR: Please enter number!")
			continue

		if number < bounds[0] or number > bounds[1]:
			print(u"ERROR: Please enter number from %d to %d" % (bounds[0], bounds[1]))
			continue
		return number


def main(rssURL):
	content = readWeb(rssURL)

	files = re.findall("<item>\s+<title>([^<]*)</title>.*?<guid>([^<]*)</guid>", content, re.DOTALL)
	length = len(files)
	startIndex = getNumber("start download from", (1,length))
	stopIndex = getNumber("download till", (startIndex, length))
	prefix = input("Add prefix to the file? (press enter for none)") or ""
	outputDir = "."

	for f in files[startIndex - 1 : stopIndex]:
		dest = os.path.join(outputDir, u"%s%s.mp4" % (prefix, f[0]))
		# if not os.path.isfile(dest):
		download(f[1], dest)

def getRSSUrl(coursePageUrl): 
	urlComponents = re.match("https?://([^/]+)/Panopto.*folderID=(?:%22|\")([a-zA-Z0-9\-]{36})", coursePageUrl, re.I)
	if not urlComponents:
		raise ValueError(u"Could not parse the course url!\n Make sure it looks like this:" + \
						u"\n\thttps://panoptotech.cloud.panopto.eu/Panopto/Pages/Sessions/List.aspx#folderID=3cae3bb8-2422-4955-81db-44b63ecd63de" + \
						u"(with http OR https at the beginning)")
	panoptoUrl = urlComponents.group(1)
	courseId = urlComponents.group(2)
	return "http://%s/Panopto/Podcast/Podcast.ashx?courseid=%s&type=mp4" % (panoptoUrl, courseId)
	

if __name__ == '__main__':
	print(u"Welcome to Panopto downloader [Home page: https://github.com/urielha/Video.Technion]")
	print(u"")
	print(u"Please enter the linke to the course (e.g. https://panoptotech.cloud.panopto.eu/Panopto/.../...folderID=**")
	coursePageUrl = input(u"> ")
	rssURL = getRSSUrl(coursePageUrl)
	print(u"%s" % rssURL)
	
	main(rssURL)

	# parser = argparse.ArgumentParser(description='Download videos one by one from panopto.', epilog='Written by uriel, hope you enjoy it.')
	# parser.add_argument('rssURL', help='the RSS url of the Course in the Panopto')
	# parser.add_argument('prefix', nargs='?', default='', help='prefix of the filename')
	# parser.add_argument('-i', '--ignore', required=False, dest='ignoreTill', metavar='num', default=0, type=int, help='ignore x videos from the start (will automaticly ignore files that already exist)')
	# parser.add_argument('-d', '--download', required=False, dest='downloadTill', metavar='num', default=-1, type=int, help='download x videos and stop (default is download all)')
	# parser.add_argument('-o', '--output', required=False, dest='outputDir', metavar='output_dir', default='.', help='output directory (default is current)')
	# arguments = parser.parse_args()