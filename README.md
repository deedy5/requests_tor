# requestsTor

Wrapper of the [requests](https://docs.python-requests.org) and [stem](https://stem.torproject.org) libraries to make requests through [TOR](https://www.torproject.org)

## Install

```
pip install requestsTor
```

## Dependencies
1. download and start [Tor](https://www.torproject.org/download/tor/) or [Torbrowser](https://www.torproject.org/download/)
2. install [requests](https://docs.python-requests.org) and [stem](https://stem.torproject.org) libraries
```
pip install requests[socks]
pip install stem
```
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
