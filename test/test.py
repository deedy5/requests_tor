from collections import Counter
from requestsTor_test import requestsTor

urls = (f'https://habr.com/ru/post/{x}' for x in range(531500, 531550))
url = 'https://habr.com/ru/post/531622'
##urls = (f'https://api.my-ip.io/ip' for x in range(531500, 531550))

def main():
    rt = requestsTor(tor_ports=[9000, 9001, 9002, 9003, 9004])
##    print(rt.check_ip())
##    rt.new_ip()
##    print(rt.check_ip())
##    print(rt.get('https://r0.ru').text)
##    print(rt.get('https://ya.ru').text)
##    print(rt.get('https://ya.ru').text)
##    print(rt.get('https://ya.ru').text)
##    print(rt.get('https://ya.ru').text)
##    print(rt.get('https://ya.ru').text)

##    print(rt.check_ip())
##    print(rt.check_ip())
##    print(rt.check_ip())
##    print(rt.check_ip())
##    print(rt.check_ip())
    rt.new_id()


##    res = rt.get_urls(urls)
##    for r in res:
##        print(r.url, r.text)
##    print(Counter(r.text for r in res))
    

    

if __name__ == '__main__':
    main()
