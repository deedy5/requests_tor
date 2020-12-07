from random import choice
import requests
from stem import Signal
from stem.control import Controller


class requestsTor(object):
    
    def new_ip(self, cport=9151, password=None):
        with Controller.from_port(port=cport) as controller:
            controller.authenticate(password=password)
            controller.signal(Signal.NEWNYM)

    def check_ip(self):
        ip_api_list = ['https://api.my-ip.io/ip', 'https://api.ipify.org', 'https://ifconfig.me/ip', 
                       'https://httpbin.org/ip', 'https://icanhazip.com/', 'https://ipinfo.io/ip',
                       'https://wtfismyip.com/text', 'https://checkip.amazonaws.com/', 
                       'https://bot.whatismyipaddress.com', 'https://whoer.net/ip',]
        return self.get(choice(ip_api_list)).text

    def get(self, url, port=9150):
        headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                   "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.5",
                   "Upgrade-Insecure-Requests": "1",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"}
        proxies = {'http': f'socks5h://localhost:{port}', 'https': f'socks5h://localhost:{port}',}
        return requests.get(url, headers = headers, proxies = proxies)
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        return self
