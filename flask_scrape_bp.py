## run with python chromevideos.py NUMBER STRING,
## where STRING = the name of the video you would search.

from selenium import webdriver
from re import finditer
from selenium.webdriver.chrome.options import Options
import time
from datetime import date
import os
import sys
import subprocess
from flask import Flask
from flask_cors import CORS
from flask import request
from flask import jsonify

app = Flask(__name__)
CORS(app)

def findMatchIter(regexString, matchString, offset):
	for match in finditer(regexString, matchString):
		return match.group()[offset:]
		
def returnAllMatchesInIter(regexString, matchString, offset, array):
	for match in finditer(regexString, matchString):
		array.append(match.group()[offset:])
	return array
	
def getqueryresults(args):
## online : queries an active server : be careful
	
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(chrome_options=chrome_options)

	driver.get("https://www.npmjs.com/packages")
	querystring = str(driver.page_source.encode('utf-8'))


###

	# we could add custom search as an argument, it really depends on what the task is.
	queryreturnarray = []
	queryarray = returnAllMatchesInIter(r'"https://.+?(?=")', querystring, 7, queryreturnarray)	
	return queryreturnarray

@app.route("/")
def main():
	# The s parameter is the url for the page source code. Not used here but kept for reference.
	args = request.args.get('s')
	queryreturnarray = getqueryresults(args)
	result_dict = {}
	try:
		count = 0
		for index, x in enumerate(queryreturnarray):
			if "name" not in x:
				result_dict["resultno" + str(count)] = queryreturnarray[index]
				count += 1
	except Exception as e:
		print(e)
	return jsonify(result_dict)
