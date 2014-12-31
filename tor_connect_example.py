#!/usr/bin/env python


'''# tor_connect_example.py - an example of shuffelz'''

__author__ = ["A'mmer Almadani:Mad_Dev", "penbang.sysbase.org"]
__email__  = ["mad_dev@linuxmail.org", "mail@sysbase.org"]

import socket
import urllib2
import socks  # SocksiPy module
import stem.process
from stem.util import term
import re
from stem import CircStatus
from stem.control import Controller
import random
import shuffelz
import time



def check_tor():
  req = urllib2.Request('https://check.torproject.org/')
  response = urllib2.urlopen(req)
  the_page = response.read()
  if 'Sorry. You are not using Tor.' in the_page:
    print 'Sorry. You are not using Tor.'

  if 'Congratulations. This browser is configured to use Tor.' in the_page:
    print 'Congratulations. your are using Tor'

  return the_page
  


def print_bootstrap_lines(line):
  if "Bootstrapped " in line:
    print term.format(line, term.Color.RED)

def multi():
  j = open('lists/country_codes.tor', 'r')
  nodes = j.read()
  regex = re.findall('{[a-z]*}', nodes)
  return random.choice(regex)
    
def tor(random_node):

    SOCKS_PORT = 9050
    if random_node == None:
      EXIT_NODE = ' '
      ENTRY_NODE = ' '
    elif random_node == 'random':
      ENTRY_NODE = multi()
      #print ENTRY_NODE
      EXIT_NODE = multi()
     # print EXIT_NODE

    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
    socket.socket = socks.socksocket
    print term.format("Starting Tor:\n", term.Attr.BOLD)

    tor_process = stem.process.launch_tor_with_config(
      config = {
        'SocksPort': str(SOCKS_PORT),
        'ControlPort': '9151',
        'CookieAuthentication': '1',
        'Log notice' : 'stdout',
        'AvoidDiskWrites' : '1',
        'ExitNodes': EXIT_NODE,
        'EntryNodes': ENTRY_NODE,

      },
      init_msg_handler = print_bootstrap_lines,
    )
    check_tor()


    mask = shuffelz.shufflez()

    def random_websites():

      count = random.randint(1,5)
      for i, e, in zip(mask.randomize(10, 'site'), mask.randomize(10, 'user-agent')):
        if count == random.randint(1,5):
          break
        else:
          sleep_time = str(random.randint(1,5)) +'.'+ str(random.randint(1,9))
          print 'VISITING', '\033[92m', i , '\033[0m', 'USING', '\033[94m', e, '\033[0m', 'SLEEPING FOR', '\033[95m', sleep_time, 'SECONDS', '\033[0m'
          time.sleep(float(sleep_time))
          mask.open_url(i, e)
          print '\n'

    def random_google():
  
      count = random.randint(1,5)
      for i in mask.randomize(10, 'word'):
        if count == random.randint(1,5):
          break
        else:
          sleep_time = str(random.randint(1,5)) +'.'+ str(random.randint(1,9))
          print 'SEARCHING FOR', '\033[92m', i ,'\033[0m', 'SLEEPING FOR', '\033[95m', sleep_time, 'SECONDS', '\033[0m', '\n'
          time.sleep(float(sleep_time))
          mask.google(i)


    while True:
      try:
        mask.together(random_google(), random_websites())
      except KeyboardInterrupt:
        print 'Exit'
        break


    print '\n' + term.format("Tor Stoped\n", term.Attr.BOLD)
    tor_process.kill()


try:
  tor('random')

except OSError, e:
  print 'USING EXIT_NODE/ENTRY_NODE BASED ON TOR SUGGESTIONS'
  tor(None)

