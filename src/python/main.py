from .roles import env_setup, zookeeper, kafka
from .helpers.main import *


def start():
	check_flags()
	check_creds_yml()
	introduce()
	while True:
		info = dict()
		info['jdk_version'] = info['zookeeper_version'] = info['kafka_task'] = None

		info['stand'] = choose_points('stands', 'Stands')

		info['project_task'] = choose_points('project_tasks', 'Project tasks')
		if info['project_task'] == 'env_setup':
			info['jdk_version'] = choose_points('jdk_versions', 'JDK versions')

		elif info['project_task'] == 'zookeeper':
			info['zookeeper_version'] = choose_points('zookeeper_versions', 'Zookeeper versions')

		elif info['project_task'] == 'kafka':
			info['kafka_task'] = choose_points('kafka_tasks', 'Kafka tasks')
			if info['kafka_task'] == 'install_kafka':
				info['kafka_version'] = choose_points('kafka_versions', 'Kafka versions')

		machine_option = choose_machines(info['stand'], 'Machines')
		machines = get_information('machines', stand=info['stand'])
		info['machines'] = machines
		if machine_option == 'all':
			for machine in machines.keys():
				info['machine'] = machine
				info['time'] = get_information('time')
				check_json_external_vars(json.dumps(info, indent=4))
				run_ansible(info)
		else:
			info['machine'] = machine_option
			check_json_external_vars(json.dumps(info, indent=4))
			run_ansible(info)

		break
