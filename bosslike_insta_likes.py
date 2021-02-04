# Bosslike Bot liker
# 		this program use selenium module for autoliking at bosslike.ru
#		@author: 	2021, Andrey Stroganov
#		@contact:	https://github.com/snakoner/ 
#		This program is free to use
#

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType

import selenium
import time
import sys
import random
import datetime
import os
import constant


def use_proxy(ip, port):

	prox = Proxy()
	prox.proxy_type = ProxyType.MANUAL
	prox.http_proxy = "{}:{}".format(ip, port)
	prox.socks_proxy = "{}:{}".format(ip, port)
	prox.ssl_proxy = "{}:{}".format(ip, port)

	capabilities = webdriver.DesiredCapabilities.CHROME
	prox.add_to_capabilities(capabilities)

	return capabilities


def rand_time(min, max):
	'''
	@brief: function to get random float from {[min, max] + noise}, where noise < 1
	
		@min: 	minimal value
		@max: 	maximum value
	'''
	noise = random.randint(0,100)/100.0
	return random.randint(min, max) + noise


def read_user_data(filename):
	'''
	@brief: function to get user's auth data

		@filename: 	source file with user's auth data
	'''
	data = []
	with open(filename, 'r') as f:
		data = f.read().splitlines()
	return data[0], data[1]

def auth_bosslike(browser, username, password):
	'''
	@brief: function to auth on bosslike.ru

		@browser: 	actual browser object
		@username:	username to set
		@password:	password to set (plain text, no md5)
	'''
	browser.get(constant.BOSSLIKE_URL_AUTH)
	log = browser.find_element_by_id('User_loginLogin')
	passw = browser.find_element_by_id('User_passwordLogin')
	log.send_keys(username)
	time.sleep(.2)
	passw.send_keys(password)
	time.sleep(60)
	btn = browser.find_element_by_name('submitLogin')
	btn.click()
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
	time.sleep(3)
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
	time.sleep(60)
	#auth bosslike + instagram
	bosslike_username, bosslike_password = read_user_data(constant.BOSSLIKE_UDATA_PATH)
	insta_username, insta_password = read_user_data(constant.INSTAGRAM_UDATA_PATH)

	auth_bosslike(browser, bosslike_username, bosslike_password)
	time.sleep(1)
	auth_insta(browser, insta_username, insta_password)
	time.sleep(1)
	
	#go to bosslike
	browser.get(constant.BOSSLIKE_URL_LIKE)
	main_window = browser.current_window_handle

	#statistics
	done = 0
	failed = 0
	refresher = 0
	prev_balance = ''
	balance = ''
	
	print('\n')

	while True:
		btns = browser.find_elements_by_class_name("do.do-task.btn.btn-sm.btn-primary.btn-block")
		curr_btn = None
		try:
			curr_btn = btns.pop(0)
		except IndexError:
			continue
		try:
			curr_btn.click()
		except selenium.common.exceptions.ElementClickInterceptedException:
			continue

		time.sleep(2)
		chwd = browser.window_handles

		if len(chwd) != constant.DRIVER_MAX_WINDOW_OPENED:
			failed += 1
			if failed > constant.BOSSLIKE_REFRESH_TRESHOLD:
				browser.get(constant.BOSSLIKE_URL_LIKE)
				time.sleep(3)
				failed = 0
			continue
		else:
			time.sleep(rand_time(5,7))
			for w in chwd:
				if w!=main_window:
					browser.switch_to.window(w)
			like_button = browser.find_elements_by_class_name('wpO6b ')
			if len(like_button):
				like_button[1].click()
				time.sleep(rand_time(1,2))
				browser.close()
			time.sleep(1)
			browser.switch_to.window(main_window)
			btns = browser.find_elements_by_class_name("do.btn.btn-sm.btn-primary.btn-block.btn-success.check-task")
			curr_btn = None
			try:
				curr_btn = btns.pop(0)
			except IndexError:
				pass
			try:
				curr_btn.click()
			except selenium.common.exceptions.ElementClickInterceptedException:
				pass

			time.sleep(3)
			done += 1
		if failed > constant.BOSSLIKE_REFRESH_TRESHOLD:
			browser.get(constant.BOSSLIKE_URL_LIKE)
			time.sleep(3)
			failed = 0
		prev_balance = balance
		balance = get_user_balance(browser)
		if balance == prev_balance:
			refresher += 1
		else:
			refresher = 0
		if refresher == constant.BOSSLIKE_REFRESH_TRESHOLD:
			refresher = 0
			print("Starting new process")
			browser.close()
			time.sleep(2)
			os.system('python {} &'.format(constant.PY_EXEC_FILENAME_LIKES))
			os.system('kill -9 {}'.format(os.getpid()))

		#each cycle print data
		print("{} ---- {}".format(str(datetime.datetime.now().time()).split('.')[0], get_user_balance(browser)))

