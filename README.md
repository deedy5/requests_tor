# requestsTor

Wrapper of the [requests](https://docs.python-requests.org) and [stem](https://stem.torproject.org) libraries to make requests through [TOR](https://www.torproject.org)

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
    r = rt.get('https://foxnews.com')
    print(r.text) 
    
    # new Tor identity
    rt.new_ip()

```
