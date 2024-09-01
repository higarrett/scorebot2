# Scorebot Base
Scorebot is a scoring engine for CTF competitions. It is built upon a Blue Team / Red Team model, where Blue Teams defend flags against Red teams. (Blue Teams may also attack other Blue Teams to steal flags). Scoring is based upon flags stolen, scored service up time, and injects submitted.

This project is based off of the Scorebot used in the Pros vs Joes CTF by BSidesLV. Since I could not figure out how it is run or a clean way to get everything together, I am making my own.

# Current Status

## To do
 - [ ] Scoreboard
 - [ ] Flag submission portal
 - [ ] Monitor scripts
	 - [x] DNS
	 - [x] Email (SMTP & IMAP)
	 - [x] FTP
	 - [x] LDAP
	 - [ ] Website Check

# Setup

Setup information is still being written as the project is developed and written. The majority of the Scorebot will be written in Python as to make it easy to run on many systems. 
The current development is being conducted on Ubuntu 22.04.4 LTS and will be tested on other Linux variants once complete.

## Dependencies

### Python
dnspython
ldap3
ping3
