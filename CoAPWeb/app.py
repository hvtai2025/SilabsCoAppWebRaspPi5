from flask import Flask, render_template, jsonify, request
import subprocess
import threading
import re

app = Flask(__name__)

# In-memory node list and user UI list
nodes = []  # List of discovered nodes (dict: {ipv6, type})
user_nodes = []  # List of nodes added to user UI


# Discover nodes using pydbus and the WSBRD D-Bus API
def discover_nodes():
    global nodes
    import sys
    import os
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../wisun_applications/wisun_node_monitoring/linux_border_router_wsbrd/get_nodes_ipv6_address.py'))
    discovered = []
    try:
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=5)
        output = result.stdout.strip()
        if output:
            for line in output.splitlines():
                ipv6 = line.strip()
                if ipv6:
                    discovered.append({"ipv6": ipv6, "type": "LED"})
        nodes = discovered
        print("[DEBUG] Discovered node IPv6 addresses (from script):")
        for n in nodes:
            print(f"  {n['ipv6']}")
    except Exception as e:
        print(f"[ERROR] Failed to run get_nodes_ipv6_address.py: {e}")
        nodes = []

def send_coap_command(ipv6, command):
    # Build the coap-client-notls command
    if command == "LED ON":
        cmd = [
            "coap-client-notls", "-m", "put", "-N", "-B", "10", "-t", "text",
            f"coap://[{ipv6}]:5683/leds/control", "-e", "LED ON"
        ]
    elif command == "LED OFF":
        cmd = [
            "coap-client-notls", "-m", "put", "-N", "-B", "10", "-t", "text",
            f"coap://[{ipv6}]:5683/leds/control", "-e", "LED OFF"
        ]
    else:
        return {"status": "error", "message": "Unknown command"}
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return {"status": "ok", "stdout": result.stdout, "stderr": result.stderr}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/nodes", methods=["GET"])
def api_nodes():
    discover_nodes()
    return jsonify(nodes)

@app.route("/api/user_nodes", methods=["GET", "POST"])
def api_user_nodes():
    global user_nodes
    if request.method == "POST":
        node = request.json
        if node not in user_nodes:
            user_nodes.append(node)
    return jsonify(user_nodes)

@app.route("/api/led/<ipv6>/<action>", methods=["POST"])
def api_led_control(ipv6, action):
    if action == "on":
        result = send_coap_command(ipv6, "LED ON")
    elif action == "off":
        result = send_coap_command(ipv6, "LED OFF")
    else:
        result = {"status": "error", "message": "Invalid action"}
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
