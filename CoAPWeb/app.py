from flask import Flask, render_template, jsonify, request
import subprocess
import threading
import re
import json

app = Flask(__name__)

from flask import Flask, render_template, jsonify, request
import subprocess
import threading
import re
import json

app = Flask(__name__)

nodes = []  # List of discovered nodes (dict: {ipv6, type})
user_nodes = []  # List of nodes added to user UI


# Helper to determine node type using CoAP query
def get_node_type(ipv6):
    import os
    import sys
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './get_node_type.py'))
    try:
        result = subprocess.run([sys.executable, script_path, ipv6], capture_output=True, text=True, timeout=5)
        output = result.stdout.strip()
        if output and output != "UNKNOWN":
            return output
        else:
            return "UNKNOWN"
    except Exception as e:
        pass
        print(f"[ERROR] Failed to get node type for {ipv6}: {e}")
        return "UNKNOWN"

# Helper to get join time from /statistics/app/join_states_sec
def get_join_time(ipv6):
    import os
    import sys
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './coap_join_stats.py'))
    try:
        result = subprocess.run([sys.executable, script_path, ipv6], capture_output=True, text=True, timeout=8)
        if result.returncode != 0:
            return None
        data = result.stdout.strip()
        try:
            parsed = json.loads(data)
        except Exception:
            return None
        # join_states_sec is expected to be a list of numbers
        if isinstance(parsed, dict) and 'join_states_sec' in parsed:
            arr = parsed['join_states_sec']
            if isinstance(arr, list):
                try:
                    return sum(float(x) for x in arr)
                except Exception:
                    return None
        elif isinstance(parsed, list):
            try:
                return sum(float(x) for x in parsed)
            except Exception:
                return None
        return None
    except Exception as e:
        print(f"[ERROR] Failed to get join time for {ipv6}: {e}")
        return None

@app.route("/api/sensor_data/<path:ipv6>", methods=["GET"])
def api_sensor_data(ipv6):
    import os
    import sys
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './coap_sensor.py'))
    try:
        result = subprocess.run([sys.executable, script_path, ipv6], capture_output=True, text=True, timeout=8)
        if result.returncode != 0:
            return jsonify({'error': 'CoAP request failed', 'stderr': result.stderr}), 502
        data = result.stdout.strip()
        # Try to parse as JSON, else return as string
        try:
            parsed = json.loads(data)
        except Exception:
            parsed = data

        # If parsed is a dict and has 'payload', try to parse payload
        if isinstance(parsed, dict) and 'payload' in parsed:
            payload = parsed['payload']
            # payload may be a JSON string or already a dict
            if isinstance(payload, str):
                try:
                    payload_dict = json.loads(payload)
                except Exception:
                    payload_dict = None
            elif isinstance(payload, dict):
                payload_dict = payload
            else:
                payload_dict = None
            # If temperature is present, return it as value
            if payload_dict and 'temperature' in payload_dict:
                return jsonify({'value': payload_dict['temperature']})
            # If payload_dict is a dict, return it
            if payload_dict:
                return jsonify(payload_dict)
            # Otherwise, return the payload as string
            return jsonify({'value': payload})
        # If parsed is a dict and has temperature directly
        if isinstance(parsed, dict) and 'temperature' in parsed:
            return jsonify({'value': parsed['temperature']})
        # If parsed is a dict, return it
        if isinstance(parsed, dict):
            return jsonify(parsed)
        # Otherwise, return as string
        return jsonify({'value': parsed})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Discover nodes using pydbus and the WSBRD D-Bus API
def discover_nodes():
    global nodes
    import sys
    import os
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './get_nodes_ipv6_address.py'))
    discovered = []
    try:
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=5)
        output = result.stdout.strip()
        if output:
            for line in output.splitlines():
                ipv6 = line.strip()
                if ipv6:
                    node_type = get_node_type(ipv6)
                    if not node_type or node_type == "UNKNOWN":
                        continue  # Skip nodes that do not reply to type request
                    join_time = get_join_time(ipv6)
                    node_info = {"ipv6": ipv6, "type": node_type}
                    if join_time is not None:
                        node_info["join_time_sec"] = join_time
                    discovered.append(node_info)
        nodes = discovered
        print("[DEBUG] Discovered node IPv6 addresses (from script):")
        for n in nodes:
            jt = n.get('join_time_sec')
            jt_str = f", join_time={jt:.2f}s" if jt is not None else ""
            print(f"  {n['ipv6']} ({n['type']}){jt_str}")
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
        print(f"[DEBUG] Executing command: {' '.join(cmd)}")
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
    return jsonify({"nodes": nodes})

@app.route("/api/user_nodes", methods=["GET", "POST", "DELETE"])
def api_user_nodes():
    global user_nodes
    if request.method == "POST":
        node = request.json
        if node not in user_nodes:
            user_nodes.append(node)
        return jsonify(user_nodes)
    elif request.method == "DELETE":
        user_nodes.clear()
        return jsonify({"status": "cleared"})
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
