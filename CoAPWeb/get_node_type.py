import subprocess
import sys

def get_node_type(ipv6, coap_port=5683):
    """
    Query the node at the given IPv6 address for its type using the /settings/parameter/node_type CoAP resource.
    Returns the node type string (e.g., 'LED', 'SENSOR', 'GPN') or None if not found.
    """
    coap_uri = f"coap://[{ipv6}]:{coap_port}/settings/parameter/node_type"
    cmd = [
        "coap-client-notls", "-m", "get", "-N", "-B", "5", coap_uri
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        output = result.stdout.strip()
        if output:
            return output
        else:
            return None
    except Exception as e:
        print(f"[ERROR] Failed to get node type for {ipv6}: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_node_type.py <ipv6_address>")
        sys.exit(1)
    ipv6 = sys.argv[1]
    node_type = get_node_type(ipv6)
    if node_type:
        print(node_type)
    else:
        print("UNKNOWN")
