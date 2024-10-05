# README

## Bash Script: RPi Wi-Fi Hotspot and Web Service Setup

This script automates the setup of a Wi-Fi hotspot on a Raspberry Pi and configures two services: one to monitor the internet connection and another to host a web visualization application.

### Features
- Updates and upgrades the system's package manager.
- Installs necessary dependencies: `python3`, `python3-pip`, `hostapd`, and `dnsmasq`.
- Installs required Python libraries listed in `requirements.txt`.
- Copies project scripts to `/usr/local/bin/` and grants execution permissions.
- Creates and enables two services:
  - **Wi-Fi Monitor Service:** Monitors the internet connection and runs a Python script (`verify.py`).
  - **Web Page Service:** Hosts a web application (`app.py`).
- Configures `hostapd` and `dnsmasq` for Wi-Fi hotspot creation.
  
### Prerequisites
- Raspberry Pi running a compatible Linux OS (e.g., Raspberry Pi OS).
- Python 3 and pip installed.

### Usage

1. Clone or copy the project files to your Raspberry Pi.
2. Place the `requirements.txt` file in the project root with the necessary Python dependencies.
3. Execute the script to configure the Wi-Fi hotspot and services.

```bash
chmod 777 install.sh
./install.sh
```

### Breakdown of the Script

1. **System Update and Installation of Dependencies**
    - Updates the package lists and upgrades all installed packages.
    - Installs `python3`, `python3-pip`, `hostapd` (to create the hotspot), and `dnsmasq` (for DNS forwarding and DHCP services).

2. **Python Dependencies**
    - Installs all Python libraries listed in the `requirements.txt` file.

3. **Copying and Permissions**
    - Copies the current directory contents to `/usr/local/bin/` for system-wide accessibility.
    - Grants full permissions to all shell scripts in `/usr/local/bin/`.

4. **Wi-Fi Monitor Service**
    - Creates a systemd service file for the Wi-Fi monitor.
    - Runs the `verify.py` script to monitor the internet connection.

5. **Web Page Service**
    - Creates a systemd service file to launch the web page via `app.py`.

6. **Hotspot Configuration**
    - Configures `hostapd` to create a Wi-Fi hotspot with SSID `rasp_sam` and WPA2 encryption.
    - Configures `dnsmasq` to handle DHCP for the hotspot, assigning IPs in the range `192.168.0.1` to `192.168.0.20`.

7. **Enabling and Starting Services**
    - Reloads the systemd daemon to acknowledge new service files.
    - Enables and starts both the Wi-Fi monitor and web page services.

### Hostapd Configuration

The configuration file for `hostapd` defines the Wi-Fi hotspot settings:

- SSID: `rasp_sam`
- WPA2 encryption
- Passphrase: `sucodefruta`

### Dnsmasq Configuration

`dnsmasq.conf` handles DHCP settings for devices connecting to the Wi-Fi hotspot:

- DHCP range: `192.168.0.1` to `192.168.0.20`
  
### License

This script is provided "as-is" without any warranty. Use it at your own risk.

---

### Troubleshooting

If services fail to start, check their status using:

```bash
sudo systemctl status wifi_monitor.service
sudo systemctl status web_page.service
```

Ensure that the Raspberry Pi has a wireless interface (`wlan0`) available and that the system is up to date.