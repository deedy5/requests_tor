from time import sleep
from random import choice
from itertools import cycle
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from functools import partial

import requests
from stem import Signal
from stem.control import Controller


__version__ = '1.3'

IP_API = ("https://api.my-ip.io/ip", "https://api.ipify.org",
          "https://icanhazip.com", "https://ipinfo.io/ip",
          "https://wtfismyip.com/text", "https://ifconfig.me/ip",
          "https://checkip.amazonaws.com", "https://api.myip.la",
          "https://ipapi.co/ip", "https://trackip.net/ip",
          "https://ip.rootnet.in", "https://myexternalip.com/raw",
          "https://ip8.com/ip",)

TOR_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
    }


class RequestsTor():
    """
    tor_ports = specify Tor socks ports tuple (default is (9150,), as the default in Tor Browser),
    if more than one port is set, the requests will be sent sequentially through the each port;
    tor_cport = specify Tor control port (default is 9151 for Tor Browser, for Tor use 9051);
    password = specify Tor control port password (default is None);
    autochange_id = number of requests via a one Tor socks port (default=5) to change TOR identity,
    specify autochange_id = 0 to turn off autochange Tor identity;
    threads = specify threads to download urls list (default=8);
    verbose = print debug information (default=False).
    """

    def __init__(self, tor_ports=(9150,), tor_cport=9151, password=None,
                 autochange_id=5, threads=8, verbose=False):
        self.tor_ports = tor_ports
        self.tor_cport = tor_cport
        self.password = password
        self.autochange_id = autochange_id
        self.threads = threads
        self.ports = cycle(tor_ports)
        self.newid_counter = autochange_id * len(tor_ports)
        self.newid_cycle = cycle(range(1, self.newid_counter + 1))
        self.verbose = verbose

    def new_id(self):
        with Controller.from_port(port=self.tor_cport) as controller:
            controller.authenticate(password=self.password)            
            controller.signal(Signal.NEWNYM)
            if self.verbose:
                print(f"\nTOR cport auth: {controller.is_authenticated()}. TOR NEW IDENTITY. Sleep 3 sec.\n")
            sleep(3)

    def check_ip(self):
        my_ip = self.get(choice(IP_API)).text
        if self.verbose:
            print(f"my_ip = {my_ip}")
        return my_ip

    def request(self, method, url, **kwargs):
        port = next(self.ports)

        # if using requests_tor as drop in replacement for requests remove any user set proxies
        if kwargs.__contains__("proxies"):
            del kwargs["proxies"]
                    
        proxies = {"http": f"socks5h://localhost:{port}",
                   "https": f"socks5h://localhost:{port}"}
        
        kwargs["headers"] = kwargs.get("headers", TOR_HEADERS)
        resp = requests.request(method, url, **kwargs, proxies=proxies)
        if self.verbose:
            print(f"SocksPort={port} status={resp.status_code} url={resp.url}")
        if self.autochange_id and next(self.newid_cycle) == self.newid_counter:
            self.new_id()
        return resp

    def get(self, url, **kwargs):
        method = 'GET'
        return self.request(method, url, **kwargs)

    def post(self, url, **kwargs):
        method = 'POST'
        return self.request(method, url, **kwargs)

    def put(self, url, **kwargs):
        method = 'PUT'
        return self.request(method, url, **kwargs)
    
    def patch(self, url, **kwargs):
        method = 'PATCH'
        return self.request(method, url, **kwargs)

    def delete(self, url, **kwargs):
        method = 'DELETE'
        return self.request(method, url, **kwargs)

    def head(self, url, **kwargs):
        method = 'HEAD'
        return self.request(method, url, **kwargs)

    def get_urls(self, urls, **kwargs):
        results, temp_urls = [], []
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            for i, url in enumerate(urls, start=1):
                temp_urls.append(url)
                if self.newid_counter and i % self.newid_counter == 0:
                    temp_results = [resp for resp in
                                    executor.map(partial(self.get, **kwargs), temp_urls)]
                    results.extend(temp_results)
                    temp_urls.clear()
                    if self.verbose:
                        print(f"Progress: {i} urls")
            temp_results = [resp for resp in
                            executor.map(partial(self.get, **kwargs), temp_urls)]
            results.extend(temp_results)
            if self.verbose:
                print("Progress: finished")
        return results

    def test(self):
        print("\n******************TOR NEW ID test******************\n")
        self.new_id()
        
        print("\n******************HEADERS test******************\n")
        check_anything = self.get("https://httpbin.org/anything")
        print(check_anything.text)
        
        print("\n******************One thread test******************\n")
        print(f"Socks ports = {self.tor_ports}. Autochange_id = {self.autochange_id}")
        ip_url = choice(IP_API)
        print(f"Checking your ip from: {ip_url}")
        for _ in range(20):
            resp = self.get(ip_url)
            print(f"my ip = {resp.text}")
            
        print("\n******************Multithreading test******************\n")
        ip_url = choice(IP_API)
        print(f"Checking your ip from: {ip_url}")
        my_ip_list = [ip_url for _ in range(40)]
        results = self.get_urls(my_ip_list)
        results_counter = Counter(res.text for res in results)
        print("\nResults:")
        for k, item in results_counter.items():
            print(f"Your IP: {k} was {item} times")
