# requestsTor

Wrapper of the [requests](https://docs.python-requests.org) and [stem](https://stem.torproject.org) libraries to make requests through [TOR](https://www.torproject.org)

## Install

```
pip install requestsTor
```

## Dependencies
1. download and start [Tor](https://www.torproject.org/download/tor/) or [Torbrowser](https://www.torproject.org/download/)
2. This is not necessary: сonfigure torrc file if you want to add socks ports, to change control port, or to add password for control port. [Tor manual](https://www.torproject.org/docs/tor-manual.html.en)

## Usage
```python
from requestsTor import requestsTor

with requestsTor() as rt:

    # check your ip
    ip = rt.check_ip()
    print(ip) 
    
    # get url
    # Specify url and Tor socks port (default is 9150)
    url = 'https://foxnews.com'
    r = rt.get(url, port=9150)
    print(r.text) 
    
    # new Tor identity
    # Specify Tor control port (default is 9151) and password (default is None)
    rt.new_ip(cport=9151, password=None)

```
## Example: downloading list of urls concurrently with unique ip for each url
Urls:  https://habr.com/ru/post/1 - https://habr.com/ru/post/100)

1. Add a tor socks ports in torrc file (TorBrowser\Data\Tor\torrc) and restart Torbrowser. [Tor manual](https://www.torproject.org/docs/tor-manual.html.en)
```
SocksPort 9000 IsolateDestAddr
SocksPort 9001 IsolateDestAddr
SocksPort 9002 IsolateDestAddr
SocksPort 9003 IsolateDestAddr
SocksPort 9004 IsolateDestAddr
SocksPort 9005 IsolateDestAddr
SocksPort 9006 IsolateDestAddr
SocksPort 9007 IsolateDestAddr
SocksPort 9008 IsolateDestAddr
SocksPort 9009 IsolateDestAddr
```

2. 
```python
from time import sleep
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from requestsTor import requestsTor

def fetch(url):    
    port = ports[-1]
    ports.rotate()
    with requestsTor() as rt:
        res = rt.get(url, port=port)
        print(F"Downloaded {res.url}")
        return res.text
         
def new_ip():
    with requestsTor() as rt:
        return rt.new_ip()

def main():    
    urls = (f'https://habr.com/ru/post/{x}' for x in range(1, 100))
    result, counter = [], 1
    with ThreadPoolExecutor() as executor:
        for r in executor.map(fetch, urls):
            result.append(r)
            if counter % 10 == 0:
                new_ip()
                print(f"Downloaded {counter} urls")
                sleep(2)
            counter += 1
    return result

if __name__ == '__main__':
    ports = deque([x for x in range(9000, 9010)])
    main()
```
