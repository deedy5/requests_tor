[![Python >= 3.6](https://img.shields.io/badge/python->=3.6-red.svg)](https://www.python.org/downloads/) [![](https://badgen.net/github/release/deedy5/requests_tor)](https://github.com/deedy5/requests_tor/releases) [![](https://badge.fury.io/py/requests-tor.svg)](https://pypi.org/project/requests-tor) 
# requests_tor 

`Release history:` [https://pypi.org/project/requests-tor/#history](https://pypi.org/project/requests-tor/#history)

---

Multithreading requests via [TOR](https://www.torproject.org) with automatic TOR new identity.

Wrapper of the [requests](https://docs.python-requests.org) and [stem](https://stem.torproject.org) libraries.
Returns [requests.Response](https://docs.python-requests.org/en/latest/api/#requests.Response) object.

Masking as Tor Browser by using its default headers:
``` 
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"
```

### Install

```
pip install -U requests_tor
```

### Dependencies
Download and start [Tor Browser](https://www.torproject.org/download/) or install [Tor](https://www.torproject.org/docs/installguide.html.en)

---
### Simple usage
```python
from requests_tor import RequestsTor

# If you use the Tor browser
rt = RequestsTor()
OR
# If you use the Tor
rt = RequestsTor(tor_ports=(9050,), tor_cport=9051)

url = 'https://httpbin.org/anything'
r = rt.get(url)
print(r.text)

urls = ['https://foxnews.com', 'https://nbcnews.com', 'https://wsj.com/news/world',
        'https://abcnews.go.com', 'https://cbsnews.com',  'https://nytimes.com',
        'https://usatoday.com','https://reuters.com/world', 'http://bbc.com/news',
        'https://theguardian.com/world', 'https://cnn.com', 'https://apnews.com']
r = rt.get_urls(urls)
print(r[-1].text)
```

---
### Advanced usage
[Edit torrc file](https://support.torproject.org/tbb/tbb-editing-torrc/):

1. add [socks ports](https://www.torproject.org/docs/tor-manual.html.en#SocksPort),
```
SocksPort 9000 IsolateDestAddr
SocksPort 9001 IsolateDestAddr
SocksPort 9002 IsolateDestAddr
SocksPort 9003 IsolateDestAddr
SocksPort 9004 IsolateDestAddr
```
2. add password for control port [not necessary]:

generate and add in torrc file [HashedControlPassword](https://www.torproject.org/docs/tor-manual.html.en#HashedControlPassword).
```
HashedControlPassword hashed_password
```
---
```python
from requests_tor import RequestsTor

rt = RequestsTor(tor_ports=(9000, 9001, 9002, 9003, 9004), tor_cport=9151, password=None,
                 autochange_id=5, threads=8,)
"""
    tor_ports = specify Tor socks ports tuple (default is (9150,), as the default in Tor Browser),
    if more than one port is set, the requests will be sent sequentially through the each port;
    tor_cport = specify Tor control port (default is 9151 for Tor Browser, for Tor use 9051);
    password = specify Tor control port password (default is None);
    autochange_id = number of requests via a one Tor socks port (default=5) to change TOR identity,
    specify autochange_id = 0 to turn off autochange Tor identity;
    threads = specify threads to download urls list (default=8).
    """
    
# check your ip
rt.check_ip()

# new Tor identity. Сalling this function includes time.sleep(3)
rt.new_id()

# test automatic TOR new identity
rt.test()

# Requests. TOR new identity is executed after (autochange_id * len(tor_ports)) requests.
# GET request. 
rt.get(url, params=None, **kwargs)

# POST request. 
rt.post(url, data=None, json=None, **kwargs)

# PUT request. 
rt.put(url, data=None, **kwargs)

# PATCH request.
rt.patch(url, data=None, **kwargs)

# DELETE request.
rt.delete(url, **kwargs)

# HEAD request.
rt.head(url, **kwargs)

"""
    url – URL for the new Request object.
    params – dictionary, list of tuples or bytes to send in the query string.
    **kwargs – optional arguments that request takes:
        data – (optional) Dictionary, list of tuples, bytes, or file-like object 
                to send in the body of the request.
        json – (optional) A JSON serializable Python object 
                to send in the body of the Request.
        headers – (optional) Dictionary of HTTP Headers to send with the Request.
        cookies – (optional) Dict or CookieJar object to send with the Request.
        files – (optional) Dictionary of 'name': file-like-objects (or {'name': file-tuple}) 
            for multipart encoding upload. file-tuple can be a 2-tuple ('filename', fileobj), 
            3-tuple ('filename', fileobj, 'content_type') or a 4-tuple ('filename', fileobj, '
            content_type', custom_headers), where 'content-type' is a string defining the 
            content type of the given file and custom_headers a dict-like object containing 
            additional headers to add for the file.
        auth – (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
        timeout – (optional) How many seconds to wait for the server to send data before 
                giving up, as a float, or a (connect timeout, read timeout) tuple.
        allow_redirects (bool) – (optional) Boolean. 
            Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to True.
        proxies – (optional) Dictionary mapping protocol to the URL of the proxy.
        verify – (optional) Either a boolean, in which case it controls whether we verify 
            the server’s TLS certificate, or a string, in which case it must be a path to 
            a CA bundle to use. Defaults to True.
        stream – (optional) if False, the response content will be immediately downloaded.
        cert – (optional) if String, path to ssl client cert file (.pem). 
                If Tuple, (‘cert’, ‘key’) pair.
        """
```
## Examples
### 1. Get url with unique params and headers in request.
```python
from requests_tor import RequestsTor

rt = RequestsTor(tor_ports=(9000, 9001, 9002, 9003, 9004), autochange_id=5)

url = 'https://httpbin.org/anything'
params = {
    "id": 12345,
    "status": 'passed'
    }
headers = {
    "Origin": "https://www.foxnews.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
r = rt.get(url, params=params, headers=headers)
print(r.text)  
```

### 2. Get list of urls concurrently.
```python
from requests_tor import RequestsTor

rt = RequestsTor(tor_ports=(9000, 9001, 9002, 9003, 9004), autochange_id=5)

# get urls list concurrently. TOR new identity is executed depending on the number of socksports and 
# autochange_id parameter. In case of 5 socksports and autochange_id=5, after downloading 5*5=25 urls
# TOR identity will be changed. It does matter, because calling TOR new identity includes time.sleep(3).
# get_urls(urls) can accept params, headers and other arguments from requests library.
urls = (f'https://checkip.amazonaws.com' for _ in range(10))
results = rt.get_urls(urls)
for r in results:
    print(r.text) 
```

 
### 3. Get list of urls concurrently with unique ip for each url
```python
from requests_tor import RequestsTor

rt = RequestsTor(tor_ports=(9000, 9001, 9002, 9003, 9004), autochange_id=1)

urls = (f'https://habr.com/ru/post/{x}' for x in range(1, 51))
r = rt.get_urls(urls)
print(r[-1].text)
```
---
