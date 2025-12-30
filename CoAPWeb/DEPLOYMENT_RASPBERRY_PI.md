# CoAPWeb Deployment Guide for Raspberry Pi

## Prerequisites
- Raspberry Pi running Linux (Raspberry Pi OS recommended)
- Python 3.7 or newer
- pip (Python package manager)
- coap-client-notls installed and accessible in PATH

## Steps

### 1. Copy Project Files
Copy the entire `CoAPWeb` folder from your development machine to your Raspberry Pi. You can use `scp`, a USB drive, or any file transfer method.

Example using scp:
```
scp -r CoAPWeb pi@<raspberry-pi-ip>:/home/pi/
```

### 2. Install Python and pip (if not already installed)
```
sudo apt update
sudo apt install python3 python3-pip
```

### 3. Install Flask
Navigate to the CoAPWeb directory:
```
cd ~/CoAPWeb
pip3 install flask
```

### 4. Install coap-client-notls
Install libcoap or your preferred CoAP client. For libcoap:
```
sudo apt install libcoap-1-0-bin
```
Make sure `coap-client-notls` is available, or create a symlink if needed:
```
sudo ln -s /usr/bin/coap-client /usr/local/bin/coap-client-notls
```

### 5. Run the Web App
```
cd ~/CoAPWeb
python3 app.py
```

The app will start on port 5000. Access it from your browser:
```
http://<raspberry-pi-ip>:5000
```

### 6. (Optional) Run as a Background Service
For production, consider using a process manager like `systemd` or `pm2` to keep the app running.

### 7. Troubleshooting
- Ensure `coap-client-notls` is executable and in your PATH.
- Check firewall settings if you cannot access the web app from another device.
- Use `python3 -m unittest test_app.py` to run automated tests.

---
This guide helps you deploy and run the CoAPWeb dashboard on your Raspberry Pi for Wi-SUN node management and control.
