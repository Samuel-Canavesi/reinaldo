from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lidar')
def lidar_view():
    return render_template('lidar.html')

@app.route('/connect', methods=['POST'])
def connect_wifi():
    ssid = request.form['ssid']
    password = request.form['password']
    configure_wifi(ssid, password)
    return "Conectando ao Wi-Fi..."

def configure_wifi(ssid, password):
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'a') as file:
        file.write(f'\nnetwork={{\n ssid="{ssid}"\n psk="{password}"\n}}\n')
    os.system('sudo systemctl restart dhcpcd')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

