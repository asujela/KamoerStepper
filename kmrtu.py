from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from kamoer_modbus_rtu import KamoerModbus
import json

app = Flask(__name__)
CORS(app)

with open('config.json', 'r') as f:
    config = json.load(f)

com_port = config['com_port']
addresses = config['addresses']

def get_kamoer_device(addr):
    return KamoerModbus(port=com_port, addr=addr)

@app.route('/')
def index():
    return render_template('index.html', addresses=addresses)


@app.route('/stop', methods=['POST'])
def stop():
    try:
        data = request.get_json()
        addr = int(data['addr'])
        kamoer = get_kamoer_device(addr)
        kamoer.stop()
        return jsonify({"status": "success", "message": "Pump stopped."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/forward', methods=['POST'])
def forward():
    try:
        data = request.get_json()
        addr = int(data['addr'])
        print(f"Received forward request for address {addr}")
        kamoer = get_kamoer_device(addr)
        kamoer.forward()
        print(f"Pump at address {addr} is moving forward.")
        return jsonify({"status": "success", "message": "Pump moving forward."}), 200
    except Exception as e:
        print(f"Error in forward route: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/setspeed', methods=['POST'])
def set_speed():
    try:
        data = request.get_json()
        addr = int(data['addr'])
        rpm_value = int(data['rpm'])
        print(f"Received set speed request for address {addr} with RPM {rpm_value}")
        if rpm_value is None:
            return jsonify({"status": "error", "message": "RPM value not provided."}), 400
        kamoer = get_kamoer_device(addr)
        kamoer.set_speed(val_rpm=rpm_value)
        print(f"Pump at address {addr} speed set to {rpm_value} RPM.")
        return jsonify({"status": "success", "message": f"Pump speed set to {rpm_value} RPM."}), 200
    except Exception as e:
        print(f"Error in forward route: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
