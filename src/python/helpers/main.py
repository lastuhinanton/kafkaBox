import os
import sys
import json
import ansible_runner
from python.helpers.parsers import detailed_check_creds_yml, get_information


def run_ansible(info):
	result = ansible_runner.run(
        playbook=f'{os.getcwd()}/ansible/run.yml',
        inventory=f'{os.getcwd()}/ansible/environments/{info["stand"]}/inventory.yml',
        extravars=info,
    )
	print(f"Status: {result.status}")
	print(result.stdout.read())


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

def check_json_external_vars(info):
    options_yes = ['y', 'yes']
    options_no = ['n', 'no']
    print("The below data will be used in ansible:")
    print(info)
    while True:
        answer = input('Continue running? (y=yes, n=no) >> ')
        if not answer in options_yes + options_no:
            print(f"Sory, try again with the following options {options_yes + options_no}")
            continue
        if answer in options_yes:
            print("Okey! Let's get started ...\n\n")
            break
        elif answer in options_no:
            print("Okey! Let's stop it ...\n\n")
            exit()


def check_creds_yml():
	is_exist = os.path.exists('./creds.yml')
	if not is_exist:
		raise Exception("Sorry, there is no creds.yml. Run --help to know how to make it.")
	detailed_check_creds_yml()


def choises_print(choises, description):
	list_points_str = [str(i) for i in list(range(1, len(choises)+1))]
	list_points_int = list(range(1, len(choises)+1))
	while True:
		print(f'{description}:')

		for i, choise in enumerate(choises):
			print(f"{i+1}. {choise}")

		point = input("\nWrite down the point >> ")
		if not point in list_points_str:
			print(f"There is no such point. Let's try again. Write down one of {list_points_int}")
		else:
			break
	return int(point) - 1


def choose_points(type_info, description):
	choises = list(get_information(type_info))
	point = choises_print(choises, description)
	return choises[point]


def choose_machines(stand, description):
	choises = ['all'] + list(get_information('machines', stand=stand).keys())
	point = choises_print(choises, description)
	return choises[point]


