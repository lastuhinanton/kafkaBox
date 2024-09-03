import os
import sys
from python.helpers.parsers import detailed_check_creds_yml

def help():
  print(f"""
  Hello, {os.environ.get('USERNAME')}!

  For runing script securily make sure you have file creds.yml
  This file will be hidden by the .gitignore so just in case you can't push to the remote git server

  For example, let's look at the directory graph with creds.yml
  src/
  .
  ├── ansible
  ├── creds.yml    <<-- That's our file with credentials that will be HIDDEN
  ├── example_creds.yml
  ├── python
  └── run.py


  For easy setting up this file you have an example file example_creds.yml

  For example, let's look at the directory graph with creds.yml
  src/
  .
  ├── ansible
  ├── creds.yml
  ├── example_creds.yml    <<-- That's our file with EXAMPLE credentials
  ├── python
  └── run.py

  """)

def introduce():
  print(f"""

  Hello, {os.environ.get('USERNAME')}!

  """)

def check_flags():
	if '--help' in sys.argv:
		help()
		exit()

def check_creds_yml():
	is_exist = os.path.exists('./creds.yml')
	if not is_exist:
		raise Exception("Sorry, there is no creds.yml. Run --help to know how to make it.")
	detailed_check_creds_yml()
