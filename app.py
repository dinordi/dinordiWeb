from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import subprocess

app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app, resources={r"/*": {"origins": "*"}})

SERVICES = ["pikaraoke-ledfx", "spotify-ledfx"]

def run_command(command):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return e.stderr.strip()

@app.route("/")
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/start/<service>", methods=["POST"])
def start_service(service):
    if service not in SERVICES:
        return jsonify({"error": "Invalid service"}), 400
    output = run_command(f"sudo /bin/systemctl start {service}.service")
    response = jsonify({"message": f"{service} started", "output": output})
    return response

@app.route("/stop/<service>", methods=["POST"])
def stop_service(service):
    if service not in SERVICES:
        return jsonify({"error": "Invalid service"}), 400
    output = run_command(f"sudo /bin/systemctl stop {service}.service")
    response = jsonify({"message": f"{service} stopped", "output": output})
    return response

@app.route("/status/<service>", methods=["GET"])
def status_service(service):
    if service not in SERVICES:
        return jsonify({"error": "Invalid service"}), 400
    command = f"/bin/systemctl is-active {service}.service"
    output = run_command(command)
    if output == "active":
        output
    else:
        output = "inactive"
    response = jsonify({"service": service, "status": output})
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)