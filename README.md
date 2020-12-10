# requests_tor

Multithreading requests via [TOR](https://www.torproject.org) with automatic TOR new identity. 

Wrapper of the [requests](https://docs.python-requests.org) and [stem](https://stem.torproject.org) libraries. 


### Install

```
pip install requests_tor
```

### Dependencies
1. download and start [Tor](https://www.torproject.org/download/tor/) or [Torbrowser](https://www.torproject.org/download/)
2. [not necessary] edit torrc file, if you want to add socks ports, to change control port, or to add password for control port. [Tor manual](https://www.torproject.org/docs/tor-manual.html.en)

### Simple usage
```python
from requests_tor import RequestsTor

rt = RequestsTor()

url = 'https://foxnews.com'
r = rt.get(url)
print(r.text)

urls = (f'https://foxnews.com' for _ in range(10))
res = rt.get_urls(urls)
for result in res:
    print(result.text)
```
### Advanced usage
```python
from requests_tor import RequestsTor

rt = RequestsTor(tor_ports=[9150], tor_cport=9151, password=None, 
                 autochange_id=5, threads=None, debug=0)
'''
tor_ports = specify Tor socks ports list (default is [9150]),
tor_cport = specify Tor control port (default is 9151),
tor_cport = specify Tor control port password (default is None),
autochange_id = specify how many urls will be downloaded via a one 
                Tor socks port (default is 5) to change TOR identity,
threads = specify how many threads will be used to download urls list 
          (default = min(32, os.cpu_count() + 4)),
debug = 1, if you want to print additional information (default is 0).
'''
    
# check your ip
ip = rt.check_ip()
print(ip) 

# new Tor identity    
rt.new_id()

# test automatic TOR new identity
rt.test()

# get url
url = 'https://foxnews.com'
r = rt.get(url)
print(r.text) 

# get urls list concurrently
urls = (f'https://api.my-ip.io/ip' for _ in range(10))
results = rt.get_urls(urls)
for result in results:
    print(result.url, result.text) 


 ```
### Example: downloading list of urls concurrently with unique ip for each url
Urls:  https://habr.com/ru/post/1 - https://habr.com/ru/post/50
1. Edit torrc file (TorBrowser\Data\Tor\torrc): add an additional tor socks ports and restart Torbrowser. [Tor manual](https://www.torproject.org/docs/tor-manual.html.en)
```
SocksPort 9000 IsolateDestAddr
SocksPort 9001 IsolateDestAddr
SocksPort 9002 IsolateDestAddr
SocksPort 9003 IsolateDestAddr
SocksPort 9004 IsolateDestAddr
```
2. Program
```python
from requests_tor import RequestsTor

rt = RequestsTor(tor_ports=[9000, 9001, 9002, 9003, 9004], autochange_id=1)

urls = (f'https://habr.com/ru/post/{x}' for x in range(1, 50))
results = rt.get_urls(urls)
for result in results:
    print(result.status_code, result.url)
print(results[-1].text)
```
