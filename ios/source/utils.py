import subprocess
import json
import os

def _defaults_read(plist, key, value_type):
    try:
        return subprocess.run(['defaults', 'read', plist, key], check=True, stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
    except: # Something went wrong (No plist or key)
        if value_type == 'int':
            return 0
        elif value_type == 'string':
            return ''
        return None

def _defaults_write(plist, key, value):
    type_arg = "-int" if isinstance(value, int) else "-string"
    try:
        subprocess.run(['defaults', 'write', plist, key, type_arg, value], check=True, stdout=subprocess.PIPE)
    except:
        retu

def _load_json(file):
    with open(file) as f:
        return json.load(f)

def _write_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def read_sekai_plist(plist):
    data = dict()
    # Sekai account
    data['SEKAI_ACCOUNT_INSTALL_ID'] = _defaults_read(plist, 'SEKAI_ACCOUNT_INSTALL_ID', 'string')
    data['SEKAI_ACCOUNT_USER_ID'] = _defaults_read(plist, 'SEKAI_ACCOUNT_USER_ID', 'int')
    data['SEKAI_CREDENTIAL'] = _defaults_read(plist, 'SEKAI_CREDENTIAL', 'string')
    # Unity account, probably for statistics?
    data['unity.cloud_userid'] = _defaults_read(plist, 'unity.cloud_userid', 'string')
    data['unity.player_session_count'] = _defaults_read(plist, 'unity.player_session_count', 'int')
    data['unity.player_sessionid'] = _defaults_read(plist, 'unity.player_sessionid', 'int')
    return data

def write_sekai_plist(plist, data):
    _defaults_write(plist, 'SEKAI_ACCOUNT_INSTALL_ID', data['SEKAI_ACCOUNT_INSTALL_ID'])
    _defaults_write(plist, 'SEKAI_ACCOUNT_USER_ID', data['SEKAI_ACCOUNT_USER_ID'])
    _defaults_write(plist, 'SEKAI_CREDENTIAL', data['SEKAI_CREDENTIAL'])
    _defaults_write(plist, 'unity.cloud_userid', data['unity.cloud_userid'])
    _defaults_write(plist, 'unity.player_session_count', data['unity.player_session_count'])
    _defaults_write(plist, 'unity.player_sessionid', data['unity.player_sessionid'])

# Ugly
def find_files(filename, search_path):
   result = []
   for root, dir, files in os.walk(search_path):
      if filename in files:
         result.append(os.path.join(root, filename))
   return result

def find_proseka():
    installs = list()
    # Proseka EN
    files = find_files("com.sega.ColorfulStage.en.plist", "/var/mobile/Containers/Data/Application/")
    if len(files) > 0:
        for file in files:
            s = file.split("/")
            if len(s) < 6:
                continue
            GUID = file.split("/")[6]
            installed = os.path.exists(f"/var/mobile/Containers/Data/Application/{GUID}/.multisekai")
            installs.append({'type': 'en', 'GUID': GUID, 'installed': installed})  
    # Proseka JP
    files = find_files("com.sega.pjsekai.plist", "/var/mobile/Containers/Data/Application/")
    if len(files) > 0:
        for file in files:
            s = file.split("/")
            if len(s) < 6:
                continue
            GUID = files[0].split("/")[6]
            installed = os.path.exists(f"/var/mobile/Containers/Data/Application/{GUID}/.multisekai")
            # Proseka JP disabled for now
            # installs.append({'type': 'jp', 'GUID': GUID, 'installed': installed})  
    return installs

def install_multisekai(install):
    if install['installed']:
        return
    if install['type'] == 'en':
        path = f'/var/mobile/Containers/Data/Application/{install["GUID"]}/.multisekai'
        os.system(f"mkdir -p {path}/accounts/")
        # Backup current plist
        plist = f'/var/mobile/Containers/Data/Application/{install["GUID"]}/Library/Preferences/com.sega.ColorfulStage.en.plist'
        os.system(f'cp {plist} {path}/original.plist')
        _write_json(f"{path}/accounts/original.json", read_sekai_plist(plist))

def load_empty(install):
    plist = f'/var/mobile/Containers/Data/Application/{install["GUID"]}/Library/Preferences/com.sega.ColorfulStage.en.plist'
    os.remove(plist)
    os.system("launchctl kickstart -k system/com.apple.cfprefsd.xpc.daemon")
