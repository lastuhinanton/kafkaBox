import yaml

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

                    if not 'user' in vm_keys.keys(): raise Exception(f"Sorry, something wrong with 'user' field of {vm}")
                    if vm_keys['user'] == None or vm_keys['user'].strip() == '':  raise Exception(f"Sorry, something wrong with 'user={vm_keys['user']}' of {vm}")

                    if not 'pass' in vm_keys.keys(): raise Exception(f"Sorry, something wrong with 'pass' of {vm}")
                    if vm_keys['pass'] == None or vm_keys['pass'].strip() == '':  raise Exception(f"Sorry, something wrong with 'pass={vm_keys['pass']}' of {vm}")
            else:
                raise Exception("Sorry, creds.yml doesn't contain 'machines' or it's spelled")
    else:
        raise Exception("Sorry, creds.yml doesn't contain 'environments' or it's spelled")

def parse_yaml(path):
    with open(path) as f:
        yml = yaml.safe_load(f)
    return yml
