# -*- coding: utf-8 -*-

# pay attention to run python 3!

from urllib.request import urlopen
import re
import os 
import sys
import io 

import argparse

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

def main(arguments):
	rssURL = arguments.rssURL
	prefix = arguments.prefix
	ignoreTill = arguments.ignoreTill
	downloadTill = arguments.downloadTill
	outputDir = arguments.outputDir

	with urlopen(rssURL) as opener:
		content = opener.read().decode()

	files = re.findall("<item>\s+<title>([^<]*)</title>.*?<guid>([^<]*)</guid>", content, re.DOTALL)
	i = 1
	downloaded = 0
	for f in files:
		if downloadTill >= 0 and downloaded >= downloadTill:
			return

		dest = os.path.join(outputDir, u"%s%s.mp4" % (prefix, f[0]))
		if i > ignoreTill and not os.path.isfile(dest):
			download(f[1], dest)
			downloaded += 1
		i += 1


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Download videos one by one from panopto.', epilog='Written by uriel, hope you enjoy it.')
	parser.add_argument('rssURL', help='the RSS url of the Course in the Panopto')
	parser.add_argument('prefix', nargs='?', default='', help='prefix of the filename')
	parser.add_argument('-i', '--ignore', required=False, dest='ignoreTill', metavar='num', default=0, type=int, help='ignore x videos from the start (will automaticly ignore files that already exist)')
	parser.add_argument('-d', '--download', required=False, dest='downloadTill', metavar='num', default=-1, type=int, help='download x videos and stop (default is download all)')
	parser.add_argument('-o', '--output', required=False, dest='outputDir', metavar='output_dir', default='.', help='output directory (default is current)')
	
	arguments = parser.parse_args()
	main(arguments)