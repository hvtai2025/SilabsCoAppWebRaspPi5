# coap_sensor.py
# Helper script to fetch /sensor/data from a node using aiocoap
# Usage: python coap_sensor.py <ipv6>
import sys
import asyncio
from aiocoap import *

async def main(ipv6):
    uri = f'coap://[{ipv6}]:5683/sensor/data'
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri=uri)
    try:
        response = await protocol.request(request).response
        print(response.payload.decode('utf-8'))
    except Exception as e:
        print('ERROR:', e, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python coap_sensor.py <ipv6>')
        sys.exit(1)
    ipv6 = sys.argv[1]
    asyncio.run(main(ipv6))
