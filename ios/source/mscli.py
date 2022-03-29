import utils
import os

# Kept for historical purposes

if __name__ == '__main__':
    print("Looking for installs...")
    installs = utils.find_proseka() # Slow af
    if len(installs) == 0:
        print("Project Sekai not found.")
        exit(1)
    print(f"Found {len(installs)} install(s). \nData:{installs}")
    selected = 0
    if len(installs) > 1:
        x = 0
        print("Select installation: ")
        for install in installs:
            print(f"{x}: {install['type']}, {install['GUID']}, {install['installed']}")
            x += 1
        selected = int(input("> ")) # TODO: Check things
    if not installs[selected]['installed']:
        if input("Install multisekai on selected install? (y/N)> ").lower() == 'y':
            utils.install_multisekai(installs[selected])
        else:
            exit(1)
    else:
        install = installs[selected]
        plist = f'/var/mobile/Containers/Data/Application/{install["GUID"]}/Library/Preferences/com.sega.ColorfulStage.en.plist'
        path = f'/var/mobile/Containers/Data/Application/{install["GUID"]}/.multisekai'
        json_files = [pos_json for pos_json in os.listdir(f"{path}/accounts") if pos_json.endswith('.json')]
        x = 0
        print("Dumped accounts: \n")
        for file in json_files:
            print(f"{x}: {file}")
            x += 1
        print("\nCommands: \n load {name}\n write {name}\n load_empty")
        i = input(">").split()
        if len(i) > 0:
            if i[0] == 'load_empty':
                print("Deleting plist.")
                utils.load_empty(install)
            elif i[0] == 'load':
                print("Loading into plist.")
                utils.write_sekai_plist(plist, utils._load_json(f'{path}/accounts/{i[1]}'))
            elif i[0] == 'write':
                print("Saving plist.")
                utils._write_json(f"{path}/accounts/{i[1]}", utils.read_sekai_plist(plist))
