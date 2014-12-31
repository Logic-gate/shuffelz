#!/usr/bin/env python


'''# shufflez.py '''

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the <organization> nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__author__ = ["A'mmer Almadani:Mad_Dev", "sysbase.org"]
__email__  = ["mad_dev@linuxmail.org", "mail@sysbase.org"]

import random
import urllib2
from search import GoogleSearch, SearchError
import time
from multiprocessing import Process
from threading import Timer

class shufflez:

	def __init__(self):
		self.word_list = 'lists/wordlist.txt'
		self.websites = 'lists/websites.txt'
		self.user_agent = 'lists/user_agent.txt'

	def together(self, *functions):
		process = []
		for function in functions:
			s = Process(target=function)
			s.start()
			process.append(s)
		for s in process:
			s.join() 

	def randomize(self, r, typ):
		'''Return Random List
		   r (range):	int 
		   typ : word | site | user-agent	
		'''
		lst = []
	  	if typ == 'word':
	  		list_to_parse  = self.word_list
	  	elif typ == 'site':
	  		list_to_parse = self.websites
	  	elif typ == 'user-agent':
	  		list_to_parse = self.user_agent

	  	a = open(list_to_parse, 'r')
	  	for i in a.readlines():
	  		lst.append(i)
	  	random.shuffle(lst)
	  	if typ == 'site':
	  		return map(lambda x:x if 'http://' in x else 'http://' +x, lst)[0:int(r)]
	  	else:
	  		return lst[0:int(r)]

	def append_to_list(self, typ, lst):
		if typ == 'word':
			l = self.word_list
		elif typ == 'link':
			l = self.websites

		li = open(l, 'a')
		for i in lst:
			li.write(i+'\n')
		li.close()


	def open_url(self, url, user_agent):
		try:
	  		header = { 'User-Agent' : str(user_agent) }
	  		req = urllib2.Request(url, headers=header)
	  		response = urllib2.urlopen(req)
	  		print 'STATUS', response.getcode()
	  	except:
	  		pass

	def google(self, term):
		links_from_google = []
		words_from_google = []
		try:
			gs = GoogleSearch(term)
			gs.results_per_page = 10
			results = gs.get_results()
			for res in results:
				words_from_google.append(res.title.encode('utf8'))
				print '\033[92mGot new words from Google...appending to list\n\033[0m'
				self.append_to_list('word', words_from_google)
				links_from_google.append(res.url.encode('utf8'))
				print '\033[92mGot new link from Google...appending to list\n\033[0m'
				self.append_to_list('link', links_from_google)
		except SearchError, e:
			print "Search failed: %s" % e



mask = shufflez()

def random_websites():
	count = random.randint(1,15)
	for i, e, in zip(mask.randomize(10, 'site'), mask.randomize(10, 'user-agent')):
		if count == random.randint(1,15):
			break
		else:
			sleep_time = str(random.randint(1,5)) +'.'+ str(random.randint(1,9))
			print 'VISITING', '\033[92m', i , '\033[0m', 'USING', '\033[94m', e, '\033[0m', 'SLEEPING FOR', '\033[95m', sleep_time, 'SECONDS', '\033[0m'
			time.sleep(float(sleep_time))
			mask.open_url(i, e)
			print '\n'

def random_google():
	
	count = random.randint(1,15)
	for i in mask.randomize(10, 'word'):
		if count == random.randint(1,15):
			break
		else:
			sleep_time = str(random.randint(1,5)) +'.'+ str(random.randint(1,9))
			print 'SEARCHING FOR', '\033[92m', i ,'\033[0m', 'SLEEPING FOR', '\033[95m', sleep_time, 'SECONDS', '\033[0m', '\n'
			time.sleep(float(sleep_time))
			mask.google(i)
			

#while True:
#	try:
#		mask.together(random_google(), random_websites())

#	except KeyboardInterrupt:
#		print 'Exit'
#		break