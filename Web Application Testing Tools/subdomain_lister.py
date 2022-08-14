#!/usr/bin/env python

import requests
from requests.adapters import HTTPAdapter
from requests.adapters import Retry
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-w", "--wordlist", dest="wordlist", help="[+] path of wordlist")
    options = parser.parse_args()[0]
    if not options.wordlist:
        parser.error("[-] Please select the wordlist path")
    return options

def request(url):
    try:
        retry_strategy = Retry(
            total=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)

        return http.get("https://" + url, timeout=2)
    except requests.exceptions.ConnectionError:
        pass

target_url = "google.com"
option = get_arguments()
wordlist_path = option.wordlist

with open(wordlist_path, "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = word + "." + target_url
        response = request(test_url)
        if response:
            print(test_url)


