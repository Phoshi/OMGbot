# -*- coding: utf-8 -*-
import urllib2
def bitly(URL):
	short=urllib2.urlopen("http://api.bit.ly/v3/shorten?login=phoshi&apiKey=R_905d6833c92fbea28e1df7b14c0dd396&uri="+urllib2.quote(URL)+"&format=json").read()
	short=short.split(',')
	print short,"asdf"
	try:
		return short[3].split('"')[3].replace('\/','/')
	except:
		return URL