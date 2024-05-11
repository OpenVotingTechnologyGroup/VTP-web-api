#!/usr/bin/env python
"""Something to generate the QR codes for the uvicorn server"""

import socket

import requests
import segno

# Get the external IP
try:
    response = requests.get("http://ip.jsontest.com/", timeout=5)
except requests.exceptions.Timeout:
    print("Note - http://ip.jsontest.com/ timed out")
    WAN_IP = "0.0.0.0"
if response.status_code == 200:
    WAN_IP = response.json()["ip"]
else:
    print("Note - did not receive 200 status code")
    WAN_IP = "0.0.0.0"


# Get the LAN (or localhost) IP
def get_local_ip():
    """a persnickity get local IP"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    # pylint: disable=broad-exception-caught
    try:
        # doesn't even have to be reachable
        s.connect(("10.254.254.254", 1))
        this_ip = s.getsockname()[0]
    except Exception:
        this_ip = "127.0.0.1"
    finally:
        s.close()
    return this_ip


LAN_IP = get_local_ip()

print(f"LAN_IP={LAN_IP}")
print(f"WAN_IP={WAN_IP}")

wan_qrcode = segno.make_qr("http://" + WAN_IP + ":8000")
lan_qrcode = segno.make_qr("http://" + LAN_IP + ":8000")

wan_qrcode.save(WAN_IP + ".svg", scale=5, light="#EFF1C5", dark="darkgreen")
lan_qrcode.save(LAN_IP + ".svg", scale=5, light="#EFF1C5", dark="darkgreen")