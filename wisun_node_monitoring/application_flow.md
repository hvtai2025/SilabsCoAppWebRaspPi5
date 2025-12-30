# Wi-SUN Node Monitoring Application Flow

## Overview
This document describes the high-level application flow and code structure for the Wi-SUN Node Monitoring project, including the new CoAP LED control feature.

---

## Application Flow Diagram

```
+-------------------+
| Device Boot/Init  |
+-------------------+
         |
         v
+-----------------------------+
| Register CoAP Resources     |
| (app_coap_resources_init)   |
+-----------------------------+
         |
         v
+-----------------------------+
| Wait for CoAP Requests      |
+-----------------------------+
         |
         v
+-----------------------------+
| Receive CoAP PUT to         |
| /leds/control               |
+-----------------------------+
         |
         v
+-----------------------------+
| Parse Payload:              |
|  - "LED ON"  -> ON          |
|  - "LED OFF" -> OFF         |
+-----------------------------+
         |
         v
+-----------------------------+
| Call sl_led_turn_on/off     |
| for sl_led_led0             |
+-----------------------------+
         |
         v
+-----------------------------+
| Respond to CoAP Client      |
+-----------------------------+
```

---

## Key Code Points

- **CoAP Server**: Exposes resources for monitoring and control.
- **LED Control**: `/leds/control` resource, PUT with "LED ON"/"LED OFF" toggles the LED.
- **Component Use**: SIMPLE_LED/SIMPLE_BUTTON for hardware abstraction.
- **Resource Registration**: All resources registered in `app_coap_resources_init()`.
- **Documentation**: Usage and examples in README.md and coap_get_examples.md.

---

For more details or a graphical diagram, see the main documentation or request an update.
