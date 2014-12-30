#Shuffelz - an automated browsing simulator.
I wrote it for specificity for TOR.  Please read the ISSUES to understand why it should not be used outside the TOR network.
###What does it do?

* Visit random links using random user-agent at random intervals  
* Submit random queries to Google at random intervals
    * Get new links from google and append them to the website list
    * Get new words(title string) and append them to the wordlist

* POST fake data to websites regardless of the status code


###Issues:

* The consistency of your user-agent along side the random user-agents will give you away.

* The status code from the post request will give you away

* The large amount of traffic from a single IP address will alert HIM/HER/THEM...THE ENITITY to you. It is not clandestine; the sudden increase in traffic will place you in the line of fire.  

###Uses outside TOR:

* When using a network other than your own.

* To mess around with the MAN IN THE MIDDLE.

###Screenshot of shuffelz
<img src="https://dl.dropboxusercontent.com/u/79143906/Screenshot%20-%2012302014%20-%2001%3A19%3A40%20PM.png">

