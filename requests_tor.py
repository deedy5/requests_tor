from time import sleep
from random import choice
from itertools import cycle
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import requests
from stem import Signal
from stem.control import Controller


class requestsTor(object):
    """
    Wrapper of the requests and stem libraries to make requests via TOR.
    tor_ports = specify Tor socks ports list (default is [9150]), if more than one port
    is set, the requests will be sent sequentially through each port
    tor_cport = specify Tor control port (default is 9151),
    tor_cport = specify Tor control port password (default is None),
    autochange_id = specify urls via a one Tor socks port (default is 5) to change TOR identity,
    threads = specify threads to download urls list (default = min(32, os.cpu_count() + 4)),
    debug = 1, if you want to print additional information (default is 0).
    """

    def __init__(
        self,
        tor_ports=[9150],
        tor_cport=9151,
        password=None,
        autochange_id=5,
        threads=None,
        debug=0,
    ):
        self.tor_ports = cycle(tor_ports)
        self.tor_ports_count = len(tor_ports)
        self.tor_cport = tor_cport
        self.password = password
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
        }
        self.ip_api_list = [
            "https://api.my-ip.io/ip",
            "https://api.ipify.org",
            "https://ifconfig.me/ip",
            "https://icanhazip.com/",
            "https://ipinfo.io/ip",
            "https://whoer.net/ip",
            "https://wtfismyip.com/text",
            "https://checkip.amazonaws.com/",
            "https://bot.whatismyipaddress.com",
        ]
        self.autochange_id = autochange_id
        self.newid_counter = (
            cycle(range(1, autochange_id + 1)) if autochange_id else None
        )
        self.threads = threads
        self.debug = debug

    def new_id(self):
        with Controller.from_port(port=self.tor_cport) as controller:
            controller.authenticate(password=self.password)
            controller.signal(Signal.NEWNYM)
            if self.debug == 1:
                print(
                    f"\nTOR control port authenticated: {controller.is_authenticated()}"
                )
                print(f"TOR NEW IDENTITY\n")
            sleep(3)

    def check_ip(self):
        ip_api_url = choice(self.ip_api_list)
        return self.get(ip_api_url).text

    def _fetch(self, url):
        tor_port = next(self.tor_ports)
        proxies = {
            "http": f"socks5h://localhost:{tor_port}",
            "https": f"socks5h://localhost:{tor_port}",
        }
        resp = requests.get(url, headers=self.headers, proxies=proxies)
        if self.debug == 1:
            print(
                f"proxy=localhost:{tor_port} status={resp.status_code} url={resp.url}"
            )
        return resp

    def get(self, url):
        resp = self._fetch(url)
        if self.autochange_id and next(self.newid_counter) == self.autochange_id:
            self.new_id()
        return resp

    def get_urls(self, urls):
        results, temp_urls = [], []
        step = self.tor_ports_count * self.autochange_id
        for i, url in enumerate(urls, start=1):
            temp_urls.append(url)
            if i % step == 0:
                temp_results = self._fetch_urls(temp_urls)
                results.extend(temp_results)
                temp_urls.clear()
                self.new_id()
                print(f"Progress: {i} urls")
        temp_results = self._fetch_urls(temp_urls)
        results.extend(temp_results)
        return results

    def _fetch_urls(self, urls):
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            return [resp for resp in executor.map(self._fetch, urls)]

    def test(self):
        print(
            f"\nTEST\nSocks ports count = {self.tor_ports_count}. Autochange_id = {self.autochange_id}\n"
        )
        self.new_id()
        ip_url = choice(self.ip_api_list)
        print(f"Checking your ip from: {ip_url}")
        my_ip_list = [ip_url for _ in range(30)]
        results = self.get_urls(my_ip_list)
        resultsCounter = Counter(res.text for res in results)
        print("\nResults:")
        for k, v in resultsCounter.items():
            print(f"Your IP: {k} was {v} times")
