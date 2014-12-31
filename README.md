#Decompress the the wordlist file before you start
---
###Respect where it's due: 
```search.py``` and ```borwser.py``` are originally part of xgoogle by <a href="http://www.catonmat.net/blog/python-library-for-google-search/">Peteris Krumins</a>

####Changes to ```search.py```:
Original from line ```52```:

```
class GoogleSearch(object):
    SEARCH_URL_0 = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&btnG=Google+Search"
    NEXT_PAGE_0 = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&start=%(start)d"
    SEARCH_URL_1 = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&btnG=Google+Search"
    NEXT_PAGE_1 = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&start=%(start)d"
```
    
Modified:
```
    class GoogleSearch(object):
        SEARCH_URL_0 = "https://encrypted.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&btnG=Google+Search"
        NEXT_PAGE_0 = "https://encrypted.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&start=%(start)d"
        SEARCH_URL_1 = "https://encrypted.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&btnG=Google+Search"
        NEXT_PAGE_1 = "https://encrypted.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&start=%(start)d"```
---   
#shuffelz.py - an automated browsing simulator.
I wrote it for specificity for TOR.  Please read the ISSUES to understand why it should not be used outside the TOR network.
###What does it do?

* Visit random links using random user-agent at random intervals  
 
* Submit random queries to Google at random intervals
    * Get new links from google and append them to the website list
    * Get new words(title string) and append them to the wordlist

#####Randomize:
```
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
```

###Issues:

* The consistency of your user-agent along side the random user-agents will give you away.

* The status code from the post request will give you away

* The large amount of traffic from a single IP address will alert HIM/HER/THEM...THE ENITITY to you. It is not clandestine; the sudden increase in traffic will place you in the line of fire.  

###Uses outside TOR:

* When using a network other than your own.

* To mess around with the MAN IN THE MIDDLE.

###Screenshot of shuffelz
<img src="https://dl.dropboxusercontent.com/u/79143906/Screenshot%20-%2012302014%20-%2001%3A19%3A40%20PM.png">  
---
#tor_connect_example.py - an example of shuffelz through the TOR network
The example shows how to utilize shuffelz.

###What does it do?
* Connect to TOR using the following config
```
    config = {
        'SocksPort': '9050',
        'ControlPort': '9151',
        'CookieAuthentication': '1',
        'Log notice' : 'stdout',
        'AvoidDiskWrites' : '1',
        'ExitNodes': EXIT_NODE, #at first run, random selection from lists/conutry_codes.txt
        'EntryNodes': ENTRY_NODE, #at first run, random selection from lists/conutry_codes.txt
}
```
* Run shuffelz at the exit node(when TOR finshes its start-up)  
```
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
```
* Try to select random Entry/Exit nodes

    ```
        #Preview of lists/country_codes.tor
        #ASCENSION ISLAND                      {ac}
        #AFGHANISTAN                           {af}
        #ALAND                                 {ax}
        
        def multi():
          j = open('lists/country_codes.tor', 'r')
          nodes = j.read()
          regex = re.findall('{[a-z]*}', nodes)
          return random.choice(regex)
```

###Issues:

* Google search will occasionally return a ```503``` http error. Hence, the first attempt will select random Exit/Entry nodes.


