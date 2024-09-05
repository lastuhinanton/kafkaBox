import yaml
import subprocess

def detailed_check_creds_yml():
    creds  = parse_yaml('./creds.yml')
    if 'environments' in creds:
        for env in creds['environments'].keys():
            if 'machines' in creds['environments'][env]:
                for vm in creds['environments'][env]['machines'].keys():
                    s = vm.split('_')
                    if len(s) != 2: raise Exception(f"Sorry, something wrong with vm name of {vm}. The pattern is '<vm_name>_<vm_id>'")
                    if not s[1].isdigit(): raise Exception(f"Sorry, something wrong with vm id. The id has to be only numeric.")

                    vm_keys = creds['environments'][env]['machines'][vm]

                    if not 'ip' in vm_keys.keys(): raise Exception(f"Sorry, something wrong with 'ip' field of {vm}")
                    if len(vm_keys['ip'].split('.')) != 4: raise Exception(f"Sorry, something wrong with 'ip={vm_keys['ip']}' of {vm}")
                    if vm_keys['ip'].count('.') != 3: raise Exception(f"Sorry, something wrong with 'ip={vm_keys['ip']}' of {vm}")
                    for ki in vm_keys['ip'].split('.'):
                        if not ki.isdigit():  raise Exception(f"Sorry, something wrong with 'ip={vm_keys['ip']}' of {vm}")
                        if int(ki) < 0 or int(ki) > 255: raise Exception(f"Sorry, something wrong with 'ip={vm_keys['ip']}' of {vm}")

                    if not 'username' in vm_keys.keys(): raise Exception(f"Sorry, something wrong with 'username' field of {vm}")
                    if vm_keys['username'] == None or vm_keys['username'].strip() == '':  raise Exception(f"Sorry, something wrong with 'username={vm_keys['username']}' of {vm}")

                    if not 'password' in vm_keys.keys(): raise Exception(f"Sorry, something wrong with 'password' of {vm}")
                    if vm_keys['password'] == None or vm_keys['password'].strip() == '':  raise Exception(f"Sorry, something wrong with 'password={vm_keys['pass']}' of {vm}")
            else:
                raise Exception("Sorry, creds.yml doesn't contain 'machines' or it's spelled")
    else:
        raise Exception("Sorry, creds.yml doesn't contain 'environments' or it's spelled")

def parse_yaml(path):
    with open(path) as f:
        yml = yaml.safe_load(f)
    return yml

#TODO: optimize geting the parse_yaml
def get_information(type_info, stand=None):
    result = list()
    creds = parse_yaml('./creds.yml')
    project_options = parse_yaml('./ansible/environments/all/project_options.yml')
    if type_info == 'kafka_versions':
        result = get_kafka_versions(project_options)
    elif type_info == 'zookeeper_versions':
        result = get_zookeeper_versions(project_options)
    elif type_info == 'stands':
        result = get_stands(creds)
    elif type_info == 'machines':
        result = get_machines(creds, stand)
    elif type_info == 'jdk_versions':
        result = get_jdk_versions(project_options)
    elif type_info == 'project_tasks':
        result = get_project_tasks(project_options)
    elif type_info == 'kafka_tasks':
        result = get_kafka_tasks(project_options)
    elif type_info == 'time':
        result = get_current_time()
    return result

#TODO: make validation
def get_kafka_versions(file):
    return file['kafka_versions']

def get_zookeeper_versions(file):
    return file['zookeeper_versions']

def get_stands(file):
    return file['environments'].keys()

def get_machines(file, stand):
    result = dict()
    machines = file['environments'][stand]['machines']
    for machine in machines.keys():
        result[machine] = dict()
        result[machine]['id'] = machine.split('_')[1]
        result[machine]['ip'] = machines[machine]['ip']
        result[machine]['username'] = machines[machine]['username']
        result[machine]['password'] = machines[machine]['password']
    return result

def get_jdk_versions(file):
    return file['jdk_versions']

def get_project_tasks(file):
    return file['project_tasks']

def get_kafka_tasks(file):
    return file['kafka_tasks']

def get_current_time():
    return subprocess.run(['date', '+%d_%m_%Y_%H_%M_%S'], stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1]
