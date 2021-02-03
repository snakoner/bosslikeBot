# Bosslike Bot liker
# 		this program use selenium module for autoliking at bosslike.ru
#		@author: 	2021, Andrey Stroganov
#		@contact:	https://github.com/snakoner/ 
#		This program is free to use
#

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time
import copy
import selenium
import curses
import sys
import signal
import random
import datetime

driver_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
driver_exec_path = '/Users/andryusha/Desktop/chromedriver'
driver_max_windows_opened = 2

bosslike_url_auth = 'http://bosslike.ru/login/'
bosslike_url_likes = 'http://bosslike.ru/tasks/instagram/like/'
bosslike_refresh_treshhold = 4
bosslike_udata_path = 'udata/bosslike_data.txt'

insta_url_auth = 'https://www.instagram.com/accounts/login/'
insta_udata_path = 'udata/insta_data.txt'

def rand_time(min, max):
	noise = random.randint(0,100)/100.0
	return random.randint(min, max) + noise


def read_user_data(filename):
	data = []
	with open(filename, 'r') as f:
		data = f.read().splitlines()
	return data[0], data[1]

def auth_bosslike(browser, username, password):
	browser.get(bosslike_url_auth)
	log = browser.find_element_by_id('User_loginLogin')
	passw = browser.find_element_by_id('User_passwordLogin')
	log.send_keys(username)
	time.sleep(.2)
	passw.send_keys(password)
	time.sleep(.2)
	btn = browser.find_element_by_name('submitLogin')
	btn.click()
	pass

def get_user_balance(browser):
	return browser.find_element_by_id("user_points_balance").text

def auth_insta(browser, username, password):
	browser.get(insta_url_auth)
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
	#driver start
	opts = Options()
	opts.headless = True
	opts.add_argument("user-agent={}".format(driver_user_agent))
	browser = webdriver.Chrome(driver_exec_path, options=opts)

	#auth bosslike + instagram
	bosslike_username, bosslike_password = read_user_data(bosslike_udata_path)
	insta_username, insta_password = read_user_data(insta_udata_path)

	auth_bosslike(browser, bosslike_username, bosslike_password)
	time.sleep(1)
	auth_insta(browser, insta_username, insta_password)
	time.sleep(1)
	
	#go to bosslike
	browser.get(bosslike_url_likes)
	main_window = browser.current_window_handle

	#statistics
	done = 0
	failed = 0
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

		if len(chwd) != driver_max_windows_opened:
			failed += 1
			if failed > bosslike_refresh_treshhold:
				browser.get(bosslike_url_likes)
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
		if failed > bosslike_refresh_treshhold:
			browser.get(bosslike_url_likes)
			time.sleep(3)
			failed = 0
		#each cycle print data
		print("{} ---- {}".format(str(datetime.datetime.now().time()).split('.')[0], get_user_balance(browser)))

