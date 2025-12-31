# sensor_proxy.py
# Flask endpoint to proxy CoAP /sensor/data requests to a node
# Requires: pip install flask aiocoap

from flask import Flask, jsonify
from flask import request
import asyncio
from aiocoap import *
import ipaddress

app = Flask(__name__)

async def coap_get_sensor_data(ipv6):
    protocol = await Context.create_client_context()
    # CoAP URI for /sensor/data
    uri = f'coap://[{ipv6}]:5683/sensor/data'
    request = Message(code=GET, uri=uri)
    try:
        response = await protocol.request(request).response
        return response.payload.decode('utf-8')
    except Exception as e:
        return None

@app.route('/api/sensor_data/<path:ipv6>')
def api_sensor_data(ipv6):
    # Validate IPv6
    try:
        ipaddress.IPv6Address(ipv6)
    except Exception:
        return jsonify({'error': 'Invalid IPv6'}), 400
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    data = loop.run_until_complete(coap_get_sensor_data(ipv6))
    if data is None:
        return jsonify({'error': 'CoAP request failed'}), 502
    # Try to parse as JSON, else return as string
    try:
        import json
        return jsonify(json.loads(data))
    except Exception:
        return jsonify({'value': data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
