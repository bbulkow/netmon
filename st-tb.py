#!/usr/bin/env python3
#
# GOAL: invoke 'speedtest', send results to Adafruit.IO account for constant monitoring and visualization
# 
# speedtest is: sudo apt install speedtest-cli
# invoking with --json gives a nice pleasant JSON object in return.
#
# example response:
#   {
# 'download': 156505311.31652942, 
# 'upload': 3408657.2204077216, 
# 'ping': 23.74, 
# 'server': {'url': 'http://speedtest.fmt2.converseincode.net:8080/speedtest/upload.php', 
#		'lat': '37.5483', 
#		'lon': '-121.9886', 
#		'name': 'Fremont, CA', 
#		'country': 'United States', 
#		'cc': 'US', 
# 		'sponsor': 'Converse in Code Networks', 
#		'id': '27781', 
#		'host': 'speedtest.fmt2.converseincode.net:8080', 
#		'd': 20.702779323659193, 
#		'latency': 23.74 }, 
#	'timestamp': '2021-01-15T01:15:41.397896Z', 
#	'bytes_sent': 5242880, 
#	'bytes_received': 196271740, 
#	'share': None, 
#	'client': {
#			'ip': '73.241.172.238', 
#			'lat': '37.4446', 
#			'lon': '-122.1835', 
#			'isp': 'Comcast Cable', 
#			'isprating': '3.7', 
#			'rating': '0', 
#			'ispdlavg': '0', 
#			'ispulavg': '0', 
#			'loggedin': '0', 
#			'country': 'US'}
#  }
#

#
# ThingsBoard
# Device - 950Arnold
# DeviceID - e8183910-5794-11eb-940c-293b71ac913b
# Access Token XXX
#
# This is accessed through MQTT but also HTTP. Let's just try
# http. Apparently the cool kid way to do HTTP requests 




import subprocess
import json
import time

import requests

def speedtest():

	speedtest_ret = subprocess.run(['speedtest', '--json'], stdout=subprocess.PIPE, text=True)

	if speedtest_ret.returncode != 0:
		return( 0.0, 0.0, "", -1)

	
	speedtest_obj = json.loads(speedtest_ret.stdout)

	# print( "speedtest obj: ",speedtest_obj)

	print( "upload: ",speedtest_obj["upload"])

	print( "download: ", speedtest_obj["download"])

	print( "timestamp: ", speedtest_obj["timestamp"])

	return(speedtest_obj["upload"],speedtest_obj["download"],speedtest_obj["timestamp"], 0 )



THINGSBOARD_ACCESS_TOKEN = "XXX"


def log_datapoint(upload,download,timestamp):

	URI = 'https://thingsboard.cloud/api/v1/{}/telemetry'.format(THINGSBOARD_ACCESS_TOKEN)
	print(" load datapoint: URL is: ",URI)

	payload = {'upload': upload}

	print(" json object: ",payload)

	r = requests.post(URI, json=payload)
	if (r.status_code != 200):
		print(" upload to thinksboard failed: ",r.status_code)

	payload = {'download': download}
	requests.post(URI, json=payload)
	if (r.status_code != 200):
		print(" upload to thinksboard failed: ",r.status_code)


delay = 60.0 * 5.0

start = time.time()


while(True):
	print("delaying ",delay," seconds")
	time.sleep(delay);

	print("starting measurement")
	upload, download, timestamp, resultcode = speedtest()

	if resultcode == 0:
		print("starting upload")
		log_datapoint(upload,download,timestamp)
	else:
		print(' speedtest errored, try later ')
