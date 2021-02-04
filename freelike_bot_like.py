# Bosslike Bot liker
# 		this program use selenium module for autoliking at bosslike.ru
#		@author: 	2021, Andrey Stroganov
#		@contact:	https://github.com/snakoner/ 
#		This program is free to use
#

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys

import selenium
import time
import sys
import random
import datetime
import os
import constant


def rand_time(min, max):
	'''
	@brief: function to get random float from {[min, max] + noise}, where noise < 1
	
		@min: 	minimal value
		@max: 	maximum value
	'''
	noise = random.randint(0,100)/100.0
	return random.randint(min, max) + noise


def rand_time_noisy(time):
	return float(time) + random.randint(0,100)/100.

def read_user_data(filename):
	'''
	@brief: function to get user's auth data

		@filename: 	source file with user's auth data
	'''
	data = []
	with open(filename, 'r') as f:
		data = f.read().splitlines()
	return data[0], data[1]

def auth_freelike(browser, iuname, ipass):
	'''
	@brief: function to auth on bosslike.ru

		@browser: 	actual browser object
		@username:	username to set
		@password:	password to set (plain text, no md5)
	'''
	browser.get('https://freelikes.online/')
	insta_btn = browser.find_elements_by_xpath('//i[@class="socico instaico"]')
	if len(insta_btn):
		insta_btn[0].click()
	time.sleep(rand_time_noisy(1))
	input_insta = browser.find_elements_by_id('linkinsta')
	time.sleep(rand_time_noisy(1))
	input_insta[0].send_keys(iuname)
	time.sleep(rand_time_noisy(.5))
	next_button = browser.find_elements_by_xpath('//button[@onclick="logininsta();"]')
	if len(next_button):
		next_button[0].click()
	time.sleep(rand_time_noisy(5))
	randphrase = browser.find_element_by_id('randphrase').text
	time.sleep(rand_time_noisy(1))
	if not randphrase:
		return 

	main_window = browser.current_window_handle
	browser.execute_script("window.open('https://www.instagram.com/accounts/login/', '_blank');");
	time.sleep(rand_time_noisy(.8))
	chwd = browser.window_handles
	for x in chwd:
		if x!=main_window:
			browser.switch_to.window(x)


	time.sleep(rand_time_noisy(.8))
	log = browser.find_element_by_xpath('//input[@name="username"]')
	log.send_keys(iuname)
	time.sleep(rand_time_noisy(.8))
	passw = browser.find_element_by_xpath('//input[@name="password"]')
	passw.send_keys(ipass)
	time.sleep(rand_time_noisy(1))
	enter = browser.find_elements_by_xpath('//button')
	enter[1].click()
	time.sleep(rand_time_noisy(4))
	



	browser.get('https://www.instagram.com/{}/'.format(iuname))
	edit_button = browser.find_elements_by_class_name('sqdOP.L3NKy._8A5w5.ZIAjV')
	edit_button[0].click()
	time.sleep(rand_time_noisy(2))
	textarea = browser.find_elements_by_class_name('p7vTm')
	textarea[0].clear()
	time.sleep(rand_time_noisy(1))
	textarea[0].send_keys(randphrase)
	time.sleep(rand_time_noisy(1))
	send_button = browser.find_elements_by_class_name('sqdOP.L3NKy.y3zKF')
	send_button[-1].click()
	
	time.sleep(rand_time_noisy(1))

	browser.close()
	browser.switch_to.window(main_window)

	time.sleep(rand_time_noisy(1))
	check = browser.find_elements_by_id('btn_link2')
	check[0].click()

	pass

def get_user_balance(browser):
	'''
	@brief: function to get user's balance at bosslike.ru. 
			To get balance current window must be bosslike.ru.

		@browser: 	actual browser object
	'''
	return browser.find_element_by_id("user_points_balance").text

def auth_insta(browser, username, password):
	'''
	@brief: function to auth on instagram.com

		@browser: 	actual browser object
		@username:	username to set
		@password:	password to set (plain text, no md5)
	'''
	browser.get(constant.INSTAGRAM_URL_AUTH)
	time.sleep(.8)
	log = browser.find_element_by_xpath('//input[@name="username"]')
	log.send_keys(username)
	time.sleep(.8)
	passw = browser.find_element_by_xpath('//input[@name="password"]')
	passw.send_keys(password)
	time.sleep(1)
	enter = browser.find_elements_by_xpath('//button')
	enter[1].click()
	time.sleep(4)
	pass

if __name__ == '__main__':
	args = sys.argv
	is_backgr_proc = True if '-s' in args else False

	#driver start
	opts = Options()
	opts.headless = True if is_backgr_proc else False

	opts.add_argument("user-agent={}".format(constant.DRIVER_USER_AGENT))

	browser = webdriver.Chrome(constant.DRIVER_EXEC_PATH, options=opts)

	#auth bosslike + instagram
	iuname, ipass = read_user_data('instadata.txt')
	auth_freelike(browser, iuname, ipass)
	time.sleep(rand_time_noisy(2))
	browser.get('https://freelikes.online/earn/instagram/instalike')
	counter = 0

	print("\n")
	n = browser.find_elements_by_class_name('do.do-task.btn.btn-primary.btn-block')
	print("Tasks reg: {}".format(len(n)))
	while True or counter!=len(n):
		main_window = browser.current_window_handle
		browser.switch_to.window(main_window)
		time.sleep(rand_time_noisy(1))
		afterbut = browser.find_elements_by_class_name('do.do-task.btn.btn-primary.btn-block')
		time.sleep(rand_time_noisy(1))
		try:
			afterbut[counter].click()
		except IndexError:
			print("Rebooting program")
			os.system('python freelike_bot_like.py -s &')
			os.system('kill -9 {}'.format(os.getpid()))
		time.sleep(rand_time_noisy(1))
		chwd = browser.window_handles
		for x in chwd:
			if x!=main_window:
				browser.switch_to.window(x)
		time.sleep(rand_time_noisy(0.2))

		like_button = browser.find_elements_by_class_name('wpO6b ')
		if len(like_button):
			like_button[1].click()
			time.sleep(rand_time_noisy(2))
			browser.close()
		time.sleep(rand_time_noisy(1))
		browser.switch_to.window(main_window)
		afterbut = browser.find_elements_by_class_name('do.do-task.btn.btn-primary.btn-block')
		afterbut[counter].click()
		time.sleep(rand_time_noisy(2))
		counter += 1
		balance = browser.find_elements_by_id('points2')[0].text
		print("{}\t{}".format(str(datetime.datetime.now().time()).split('.')[0], balance))
		if counter == 18 or counter==len(n):
			browser.get('https://freelikes.online/earn/instagram/instalike')
			time.sleep(rand_time_noisy(2))
			n = browser.find_elements_by_class_name('do.do-task.btn.btn-primary.btn-block')

