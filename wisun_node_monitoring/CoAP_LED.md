# CoAP LED Control Feature

## Feature Overview
This project implements remote LED control on the Wi-SUN node using CoAP PUT requests. The feature allows a Border Router or any CoAP client to turn the onboard LED ON or OFF over the network.

## Implementation Details

- **Resource URI:** `/leds/control`
- **CoAP Method:** PUT
- **Payload:**
  - `LED ON`  — turns the LED on
  - `LED OFF` — turns the LED off
- **Handler:** The firmware parses the payload and calls `sl_led_turn_on(&sl_led_led0)` or `sl_led_turn_off(&sl_led_led0)` accordingly.
- **Component Dependency:** Requires SIMPLE_LED component with instance `sl_led_led0` present.

## Example Usage

From the Border Router (replace `[DEVICE_IPV6]` with your node's IPv6 address):

```
coap-client-notls -m put -N -B 10 -t text coap://[DEVICE_IPV6]:5683/leds/control -e "LED ON"
coap-client-notls -m put -N -B 10 -t text coap://[DEVICE_IPV6]:5683/leds/control -e "LED OFF"
```

## Application Flow

1. Device boots and registers CoAP resources.
2. Waits for CoAP requests.
3. On receiving a PUT to `/leds/control`, parses the payload.
4. If payload is `LED ON`, turns on the LED. If `LED OFF`, turns off the LED.
5. Responds to the client with the result.

## Code Location
- Resource handler: `app_coap.c` (`coap_callback_leds_control`)
- Resource registration: `app_coap_resources_init()`
- Documentation: `README.md`, `coap_get_examples.md`, `application_flow.md`

---

For further details, see the main documentation or source code.
