# CoAPWeb Design Specification

## Overview
CoAPWeb is a web-based dashboard and user interface for managing and controlling Wi-SUN nodes (LEDs and sensors) via CoAP commands. It enables users to discover nodes from a border router, add them to a UI, and control their functions (e.g., toggle LEDs) using CoAP commands.

## Architecture
- **Backend:** Python (Flask)
  - Discovers nodes from the border router (via script or API)
  - Maintains a list of node IPv6 addresses
  - Executes CoAP commands (using coap-client-notls) to control devices
  - Provides REST API endpoints for frontend
- **Frontend:** HTML, JavaScript, CSS
  - Dashboard: Lists discovered nodes, allows adding nodes to the user UI
  - User UI: Shows all added LEDs and sensors with control buttons
  - Side-by-side layout for Dashboard and User UI

## Features
### Dashboard
- Discover all nodes from the border router and list their IPv6 addresses
- Button to add a node to the User UI
- For LED nodes: Show ON/OFF buttons to send CoAP commands
- For sensor nodes: Show a status button (API to be defined later)

### User UI
- Displays all added LEDs and sensors
- Provides control buttons for each device

### Layout
- Dashboard and User UI are displayed side by side

## Data Flow
1. Backend discovers nodes and exposes them via REST API
2. Frontend fetches node list and displays in Dashboard
3. User adds nodes to User UI
4. For LED nodes, ON/OFF buttons trigger backend API to send CoAP commands
5. For sensor nodes, status button (future API)

## Technology Stack
- Python 3.x (Flask)
- HTML5, CSS3, JavaScript (Fetch API)
- coap-client-notls (invoked by backend)

## File Structure
- CoAPWeb/
  - app.py (Flask backend)
  - static/
    - style.css
    - script.js
  - templates/
    - index.html
  - DESIGN_SPEC.md

## Future Extensions
- Sensor status API integration
- User authentication
- Node type auto-detection
- Responsive/mobile UI

---
This document will guide the implementation of the CoAPWeb app as described in your requirements.
