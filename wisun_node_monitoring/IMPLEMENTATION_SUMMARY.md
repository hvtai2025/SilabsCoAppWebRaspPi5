# Wi-SUN Node Monitoring Firmware: Implementation Summary

## Overview
The Wi-SUN Node Monitoring firmware is designed for Silicon Labs Wi-SUN evaluation kits to monitor, report, and control nodes in a Wi-SUN network. It supports automatic network joining, periodic status reporting, remote control via CoAP/UDP, and optional button/LED interaction.

## Key Features Implemented

### 1. Automatic Network Join
- Device auto-joins a Wi-SUN network using pre-configured parameters.
- No CLI: All configuration is set at build time or via remote commands.

### 2. Status Reporting
- Sends an initial UDP message to the Border Router upon joining.
- Periodically sends status messages (default every 60s) to a configurable IPv6/port.
- Status includes device info, network state, and application parameters.

### 3. CoAP and UDP Control
- Exposes CoAP resources for monitoring and control:
  - `/info/device`, `/info/chip`, `/statistics/app/all`, `/settings/parameter/<name>`, etc.
- Supports remote get/set of parameters (e.g., `auto_send_sec`, `neighbor_table_size`, `tx_power_ddbm`, etc.).
- Allows remote reboot, reset to defaults, and saving parameters to NVM.

### 4. Application Parameters
- Parameters are initialized, stored, and retrieved from NVM.
- Can be changed remotely via CoAP and saved persistently.
- Parameters include notification interval, device type, PAN ID, neighbor table size, and more.

### 5. Button and LED Support (Optional)
- If enabled, buttons can trigger messages to the server and select boot options.
- LEDs indicate join state, connection, and message activity.

### 6. OTA DFU Support
- Firmware supports Over-the-Air Device Firmware Upgrade (OTA DFU) using CoAP.
- Requires a bootloader with storage and compression enabled.

### 7. Network Monitoring and Control Scripts
- Compatible with Linux Border Router tools and scripts for mass monitoring and control.
- Example: `coap_all` script to send CoAP requests to all nodes.

## Main Source Files
- `main.c`: Application entry point and main loop.
- `app_init.c/h`: Initialization routines.
- `app_parameters.c/h`: Application parameter management (NVM, CoAP interface).
- `app_coap.c/h`: CoAP resource registration and handlers.
- `app_reporter.c/h`: Status reporting logic.
- `app_check_neighbors.c/h`: Neighbor table management.
- `app_tcp_server.c/h`, `app_udp_server.c/h`: TCP/UDP server implementations.
- `app_wisun_multicast_ota.c/h`: OTA DFU support.
- `app_rtt_traces.c/h`: RTT trace support.

## Usage Notes
- All configuration and control is done via CoAP/UDP or at build time.
- No interactive CLI is present on the node.
- Designed for real-world, headless deployment and remote management.

---
For detailed usage, configuration, and resource documentation, see the project README.md and code comments.
