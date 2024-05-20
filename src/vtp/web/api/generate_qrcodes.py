#!/usr/bin/env python
"""Something to generate the QR codes for the uvicorn server"""

import argparse
import socket

import requests
import segno


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


def get_wan_ip():
    """a persnickity get the external IP"""
    try:
        response = requests.get("http://ip.jsontest.com/", timeout=5)
        if response.status_code == 200:
            that_ip = response.json()["ip"]
        else:
            print("Note - did not receive 200 status code")
            that_ip = "0.0.0.0"
    except requests.exceptions.Timeout:
        print("Note - http://ip.jsontest.com/ timed out")
        that_ip = "0.0.0.0"
    except:  # pylint: disable=bare-except
        print("Note - could not effectively get to the internet")
        that_ip = "0.0.0.0"
    return that_ip


def main():
    """main"""
    parser = argparse.ArgumentParser(
        description="""Will generate the local LAN and internet WAN
QR codes that if scanned will direct the user to the uvicorn
web-api server.
""",
    )
    parser.add_argument(
        "-n",
        "--printonly",
        action="store_true",
        help="will printonly and not write to disk (def=True)",
    )

    # Parse args
    parsed_args = parser.parse_args()

    lan_ip = get_local_ip()
    print(f"LAN_IP={lan_ip}")
    if not parsed_args.printonly:
        lan_qrcode = segno.make_qr("http://" + lan_ip + ":8000")
        lan_qrcode.save(lan_ip + ".svg", scale=5, light="#EFF1C5", dark="darkgreen")

    wan_ip = get_wan_ip()
    if wan_ip != "0.0.0.0":
        print(f"WAN_IP={wan_ip}")
        if not parsed_args.printonly:
            wan_qrcode = segno.make_qr("http://" + wan_ip + ":8000")
            wan_qrcode.save(wan_ip + ".svg", scale=5, light="#EFF1C5", dark="darkgreen")


if __name__ == "__main__":
    main()
