#!/bin/bash

# Atualizando o sistema
echo "Atualizando pacotes..."
sudo apt-get update
sudo apt-get upgrade -y

echo "Instalando dependências..."
sudo apt-get install python3 python3-pip hostapd dnsmasq -y

# Lib python
sudo pip install -r requirements.txt

echo "Copiando scripts e concedendo permissao..."
sudo cp -r . /usr/local/bin/
sudo chmod 777 /usr/local/bin/*.sh

WIFI=/etc/systemd/system/wifi_monitor.service
echo "Criando arquivo de serviço de conexão internet"
sudo bash -c "cat > $WIFI <<EOF
[Unit]
Description=Internet connection
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/serv_config/verify.py
Restart=on-abort

[Install]
WantedBy=multi-user.target
EOF"

WEB=/etc/systemd/system/web_page.service
echo "Criando arquivo de serviço web"
sudo bash -c "cat > $WEB <<EOF
[Unit]
Description=web visualisation
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/serv_config/app.py
Restart=on-abort

[Install]
WantedBy=multi-user.target
EOF"


# Criar o arquivo de configuração do hostapd
cat <<EOL | sudo tee /etc/hostapd/hostapd.conf
interface=wlan0
driver=nl80211
ssid=rasp_sam
hw_mode=g
channel=6
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=sucodefruta
rsn_pairwise=CCMP
EOL

# Criar o arquivo de configuração do dnsmasq
cat <<EOL | sudo tee /etc/dnsmasq.conf
interface=wlan0      # Use a interface WLAN
dhcp-range=192.168.0.1,192.168.0.20,255.255.255.0,24h
EOL

echo "Habilitando o serviço..."
sudo systemctl daemon-reload
sudo systemctl enable wifi_monitor.service
sudo systemctl enable web_page.service
sudo systemctl start wifi_monitor.service
sudo systemctl start web_page.service

