import os
import time
import json
import subprocess
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import logging

app = Flask(__name__)
socketio = SocketIO(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lidar')
def lidar_view():
    return render_template('lidar.html')

@app.route('/wifi-networks')
def wifi_networks():
    result = subprocess.run(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], stdout=subprocess.PIPE)
    networks = result.stdout.decode().strip().split('\n')
    return json.dumps(networks)

@app.route('/connect', methods=['POST'])
def connect_wifi():
    ssid = request.form.get('ssid')
    password = request.form.get('password')

    if not ssid or not password:
        logger.warning("SSID ou senha não fornecidos.")
        return jsonify({"status": "error", "message": "SSID e senha são obrigatórios."}), 400

    try:
        connect_with_nm(ssid, password)

        # Aguardar a conexão estabilizar
        time.sleep(5)

        ip_address = get_ip_address()
        return jsonify({"status": "success", "message": "Conectando ao Wi-Fi...", "ip": ip_address, "connected_ssid": ssid})
    except Exception as e:
        logger.error(f"Erro ao conectar ao Wi-Fi: {e}")
        return jsonify({"status": "error", "message": "Falha ao conectar ao Wi-Fi."}), 500

def get_ip_address():
    try:
        result = subprocess.run(['hostname', '-I'], stdout=subprocess.PIPE, text=True, check=True)
        ip_address = result.stdout.strip().split()[0] 
        logger.info(f"Novo endereço IP: {ip_address}")
        return ip_address
    except Exception as e:
        logger.error(f"Erro ao obter o endereço IP: {e}")
        return "Desconhecido"

def connect_with_nm(ssid, password):
    logger.info(f"Conectando-se à rede Wi-Fi: {ssid}")

    subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password], check=True)

    time.sleep(2)
    connection_status = get_connection_status()
    logger.info(f"Status da conexão após tentativa: {connection_status}")

def get_connection_status():
    try:
        result = subprocess.run(['nmcli', '-t', '-f', 'ACTIVE,SSID', 'dev', 'wifi'], stdout=subprocess.PIPE, text=True, check=True)
        logger.info(f"Status da conexão Wi-Fi: {result.stdout.strip()}")
        return result.stdout.strip()
    except Exception as e:
        logger.error(f"Erro ao obter status da conexão: {e}")
        return "Desconhecido"

if __name__ == '__main__':
    try:
        logger.info("Iniciando o servidor Flask com SocketIO.")
        socketio.run(app, host='0.0.0.0', port=8000, allow_unsafe_werkzeug=True)
    except Exception as e:
        logger.critical(f"Falha ao iniciar o servidor: {e}")
