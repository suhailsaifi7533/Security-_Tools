#!/user/bin/env python

import scapy.all as scapy
import optparse

def argument_parser():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="target machine ip address")
    options = parser.parse_args()[0]
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    client_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        client_list.append(client_dict)
    return client_list

def print_f(results_list):
    print("IP ADDRESS\t\tMAC ADDRESS\n.........................................")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])

options = argument_parser()
scan_result = scan(options.target)
print_f(scan_result)