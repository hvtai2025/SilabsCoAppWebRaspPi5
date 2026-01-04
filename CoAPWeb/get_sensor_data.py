import sys
import subprocess

def get_sensor_data(ipv6):
    # Query /sensor/data from the node using coap-client-notls
    cmd = [
        "coap-client-notls", "-m", "get", "-N", "-B", "5",
        f"coap://[{ipv6}]:5683/sensor/data"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        output = result.stdout.strip()
        if output:
            return output
        else:
            return "{}"
    except Exception as e:
        return f"{{\"error\": \"{str(e)}\"}}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("{}")
        sys.exit(1)
    ipv6 = sys.argv[1]
    print(get_sensor_data(ipv6))
