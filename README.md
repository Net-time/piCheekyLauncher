# piCheekyLauncher
Command line launcher for USB missile launcher, python 2, tested on rpi 3

Note that the script is made only for the Dream Cheeky Launcher with vendor and id 0x1941-0x8021.
Use lsusb to check your model.
The script should be easy to modify.


Found myself having a Automower G2 so to add wifi support I’m installing a Rasberry Pi in it, and as I also had a Dream Cheeky lying around so why not hook that up as well.
First I downloaded 3 versions of windows software before I found the one that work with my Launcher and even that one had a graphic bug. Tested that it was not broken, left limit switch was bent so had to be fixed.
Next I downloaded and tried to install about 4 versions of linux software. None worked for different reasons.

Software tried on Pi 3b Jessie  	Fail reason	                            Cons
Kostmo/Pyrocket	                  Setup not working	
Stadler/pyrocket	                Fails connecting to limit switches ?	
Grimlockrock/pi-missile-launcher	Requires getch.
                                  Getch failed to install.	
codedance/retaliation.py	        My device not included	                No check for limit switches.


The closest to work was codedance/retaliation.py version for Python 2, just changed the “original” vendor and id to mine and it worked 
Besides up/down being reversed and fire never stopped.
Noted that the limit switches are soft coded so added that to the code, just a check before command yet, not during.
Used freeusbanalyzer to check which switch does what.
Changed code to use valve switch instead of just a timed fire sequence.
Todo:
Change directional commands to use limit switches in real time.
Center command.
Initial release.
