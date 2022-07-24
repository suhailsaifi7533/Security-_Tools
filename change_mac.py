#!/user/bin/env python

import subprocess, optparse, re

def mac_changer(interface, new_mac):
    print("[+] Changin the mac for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def argument_parser():

    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its mac_address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New_Mac Address you want to set")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[+] Please type the interface")
    elif not options.new_mac:
        parser.error("[+], Please type the mac_address")
    return options

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_re = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_re:
        return mac_address_re.group(0)
    else:
        print("[+] Mac Address Not Found")
        exit()

options = argument_parser()

current_mac = get_current_mac(options.interface)
print("[+] Current Mac = " + str(current_mac))

mac_changer(options.interface, options.new_mac)
if current_mac == options.new_mac:
    print("[+] Your mac address got changed successfully to " + current_mac)
else:
    print("[-] Mac address did not get changed")
