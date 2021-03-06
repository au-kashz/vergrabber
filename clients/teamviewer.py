# -*- encoding: utf-8 -*-
# Copyright (c) Tomasz Krol tomek@kingu.pl
"""
Module to grab actual editions & versions of TeamViewer
"""
import copy
import urllib.request
import re
from datetime import datetime, date
from bs4 import BeautifulSoup

product = "TeamViewer"
user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46'


def getReleaseDate(edition):
	# Looking for release date

	# Looking for release's changelog url
	url = "https://community.teamviewer.com/t5/forums/filteredbylabelpage/board-id/Change_Logs_EN/label-name/windows"
	body = urllib.request.urlopen(url).read()

	soup = BeautifulSoup(body, "html5lib")
	chlogurl = soup.find("a", href=re.compile(edition))

	# Looking for release date in changelog
	try:
		body = urllib.request.urlopen("https://community.teamviewer.com/" + chlogurl['href']).read()
		soup = BeautifulSoup(body, "html5lib")

		value = soup.find("strong", string="Release date:").find_parent()
		value = re.search('\d+\-\d+\-\d+', value.get_text())

		result = datetime.strptime(value.group(), '%Y-%m-%d').date()  # date format example: 2019-03-23
	except:
		result = date.today()
		
	return result


def getEditions(template):
	result = []

	template.product = product
	template.ends = date.max
	template.stable = True
	template.latest = False

	# Looking for releases
	url = "https://www.teamviewer.com/en/download/windows/"
	request = urllib.request.Request(url, data=None, headers={'User-Agent': user_agent})

	body = urllib.request.urlopen(request).read()
	# body = urllib.request.urlopen("https://www.teamviewer.com/en/download/windows/").read()
	soup = BeautifulSoup(body, "html5lib")

	#Windows
	# Looking for tag with content of 3 digits blocks starting with tab eg. <tab>13.2.2344 ...
	found = soup.find(string=re.compile('\s\d+\.\d+\.\d+'))
	release = found.lstrip().rstrip()
	
	# Getting release data
	item = copy.copy(template)  # copy of Softver object

	# find version
	item.version = release
	value = re.search('\d+\.\d+', release)
	item.edition = value.group()

	# find release date
	item.released = getReleaseDate(item.version)

	# find release type
	item.latest = True

	result.append(item)

	return result

# if __name__ == "__main__":
# print(getEditions(Softver()))
