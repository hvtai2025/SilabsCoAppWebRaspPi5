# CoAPWeb Deployment and Node Control Guidelines on Rasp Pi5 Linux Gateway

## 1. Deploying CoAPWeb

### Prerequisites
- Python 3.x installed
- Required Python packages (see below)

### Installation Steps
1. **Navigate to the CoAPWeb directory:**
   ```sh
   cd CoAPWeb
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   If `requirements.txt` does not exist, manually install Flask and any other required packages:
   ```sh
   pip install flask
   ```
3. **Run the web server:**
   ```sh
   python app.py
   ```
4. **Access the web interface:**
   Open your browser and go to [http://localhost:5000](http://localhost:5000)

---

## 2. Changing the `node_type` in wisun_node_monitoring

The `node_type` determines the role or behavior of the node in the Wi-SUN network. To change it:

### Steps
1. **Locate the configuration:**
   - Open `app_parameters.c` or `app_parameters.h` in the `wisun_node_monitoring` directory.
   - Look for a variable or macro named `node_type` (e.g., `NODE_TYPE`, `g_node_type`, etc.).
2. **Modify the value:**
   - Change the value to the desired node type (e.g., `ROUTER`, `LEAF`, `BORDER_ROUTER`).
   - Example:
     ```c
     #define NODE_TYPE ROUTER
     ```
3. **Rebuild and flash the firmware:**
   - Use your build system (e.g., Simplicity Studio) to rebuild the project and flash the updated firmware to your device.

---

## 3. CoAPWeb Node Control Commands

The following commands are available to control the node from the CoAPWeb interface:

| Command           | Description                                 |
|-------------------|---------------------------------------------|
| `led/on`          | Turn the node's LED on                      |
| `led/off`         | Turn the node's LED off                     |
| `get/status`      | Get the current status of the node          |
| `get/neighbors`   | List neighboring nodes                      |
| `get/node_type`   | Get the current node type                   |
| `set/node_type`   | Set the node type (requires value)          |
| `reboot`          | Reboot the node                             |
| `trace/start`     | Start trace logging                         |
| `trace/stop`      | Stop trace logging                          |

> **Note:** The exact command endpoints may vary depending on your implementation. Refer to `app_coap.c` and `coap_sensor.py` for the latest list of supported commands.

---

## 4. Additional Notes
- Ensure the node and CoAPWeb are on the same network or can communicate over the required interface.
- For troubleshooting, check the logs in the terminal running `app.py` and on the node's serial output.
