# v0.3
from itertools import cycle
from concurrent.futures import ThreadPoolExecutor
import requests
from stem import Signal
from stem.control import Controller


class requestsTor(object):
    '''
    If newid_auto = 5, Tor identity will be changed automatically
    as soon as 5 urls will be downloaded through the one tor
    socks port. So, if you have 5 socks ports, Tor identity
    will be changed after downloading of 25 urls at all.
    '''
    
    def __init__(self, tor_ports=[9150], tor_cport=9151, password=None, newid_auto=None, debug=0):
        self.tor_ports = cycle(tor_ports)
        self.tor_cport = tor_cport
        self.password = password
        self.headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.5",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"}
        self.ip_api_list = cycle(['https://api.my-ip.io/ip', 'https://api.ipify.org', 'https://ifconfig.me/ip',
                                  'https://icanhazip.com/', 'https://ipinfo.io/ip', 'https://whoer.net/ip',
                                  'https://wtfismyip.com/text', 'https://checkip.amazonaws.com/',
                                  'https://bot.whatismyipaddress.com',])
        self.newid_auto = newid_auto
        self.newid_gen = cycle(range(newid_auto)) if newid_auto else None
        self.debug = debug
    
    def new_id(self):
        with Controller.from_port(port=self.tor_cport) as controller:
            controller.authenticate(password=self.password)
            controller.signal(Signal.NEWNYM)
            if self.debug == 1:
                print(f"\nTOR control port authenticated: {controller.is_authenticated()}")
                print(f"TOR NEW IDENTITY\n")

    def check_ip(self):
        ip_api_url = next(self.ip_api_list)
        return self.get(ip_api_url).text

    def get(self, url, _newid=1):
        if _newid == 1 and self.newid_gen:
            counter = next(self.newid_gen)
            if counter == self.newid_auto:
                self.new_id()
        tor_port = next(self.tor_ports)
        proxies = {'http': f'socks5h://localhost:{tor_port}', 'https': f'socks5h://localhost:{tor_port}',}
        resp = requests.get(url, headers = self.headers, proxies = proxies)
        if self.debug == 1:
            print(f"proxy=localhost:{tor_port} status={resp.status_code} url={resp.url}")
        return resp

    def get_urls(self, urls, threads=8):
        results, counter = [], 1
        with ThreadPoolExecutor(max_workers=threads) as executor:
             for resp in executor.map(self.get, urls, 0):
                 results.append(resp)
                 if counter * threads
        return results
