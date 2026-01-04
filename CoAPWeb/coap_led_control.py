#!/usr/bin/env python3
# coap_led_control.py
# Helper script to control LED on a node using aiocoap
# Usage: python coap_led_control.py <ipv6> <on|off>
import sys
import asyncio
from aiocoap import *

async def control_led(ipv6, action):
    uri = f'coap://[{ipv6}]:5683/leds/control'
    protocol = await Context.create_client_context()
    
    # Determine payload based on action
    if action.lower() == 'on':
        payload = b'LED ON'
    elif action.lower() == 'off':
        payload = b'LED OFF'
    else:
        print(f'ERROR: Invalid action "{action}". Use "on" or "off".', file=sys.stderr)
        sys.exit(1)
    
    request = Message(code=PUT, uri=uri, payload=payload)
    
    try:
        response = await protocol.request(request).response
        print(response.payload.decode('utf-8'))
    except Exception as e:
        print(f'ERROR: {e}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python coap_led_control.py <ipv6> <on|off>')
        sys.exit(1)
    ipv6 = sys.argv[1]
    action = sys.argv[2]
    asyncio.run(control_led(ipv6, action))
