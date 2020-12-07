# requestsTor

Wrapper of the requests and stem libraries to make requests through TOR

## Dependencies
1. download and start Tor or Torbrowser
2. install stem and requests libraries
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
