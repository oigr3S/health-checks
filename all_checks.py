#!/usr/bin/env python3

import os
import psutil
import shutil
import sys
import socket


def check_reboot():
    """Returns True if the computer has a pending reboot"""
    return os.path.exists("/run/reboot-required")

def check_disk_full(disk, min_gb, min_percentage):
    """Returns True if there isn't enough disk space, False otherwise."""
    du = shutil.disk_usage(disk)
    #calculate the percentage of free space
    percent_free = 100 * du.free / du.total
    #calculate how many free gigabytes
    gigabytes_free = du.free / 2**30
    if percent_free < min_percentage or gigabytes_free < min_gb:
        return True
    return False

def check_root_full():
    """Returns True if the root partition is full, False otherwise."""
    return check_disk_full(disk="/", min_gb=2, min_percentage=10)

def check_no_network():
    """Returns True if it fails to resolve Google's URL, False otherwise"""
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True

def check_cpu_constrained():
    """Returns Trrue if the cpu is having too much usage, False otherwise"""
    return psutil.cpu_percent(1) > 75

def main():
    checks =[
    (check_reboot, "Pending Reboot"),
    (check_root_full, "Root partion full"),
    (check_no_network, "No working network"),
    (check_cpu_constrained, "CPU load too high")
    ]
    everything_ok= True
    for check, msg in checks:
        if check():
            print(msg)
            everything_ok=False

    if not everything_ok:
        sys.exit(1)

    print("Everything is ok.")
    sys.exit(0)
main()
