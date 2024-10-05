import os
import time
import subprocess

def check_internet():
    try:
        response = subprocess.check_output(['ping', '-c', '1', '8.8.8.8'])
        return True
    except subprocess.CalledProcessError:
        return False

def start_hotspot():
    os.system('sudo systemctl start hostapd')
    os.system('sudo systemctl start dnsmasq')

def stop_hotspot():
    os.system('sudo systemctl stop hostapd')
    os.system('sudo systemctl stop dnsmasq')

def main():
    stop_hotspot()
    
    while True:
        if check_internet():
            print("Conectado à Internet.")
            stop_hotspot()
            time.sleep(10)
        else:
            print("Sem conexão com a Internet. Tentando reconectar...")
            time.sleep(60) 

            if not check_internet():
                print("Ativando hotspot para configuração...")
                start_hotspot()
                break 

if __name__ == "__main__":
    main()
