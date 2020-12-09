from collections import Counter
from requestsTor_test import requestsTor


url = 'https://ya.ru'
urls = (f'https://habr.com/ru/post/{x}' for x in range(5))
urls2 = (f'https://api.my-ip.io/ip' for _ in range(50))

def main():
    rt = requestsTor(tor_ports=[9000, 9001, 9002, 9003, 9004], debug=1)
    print(rt.check_ip())
    rt.new_id()

    print(rt.get('https://ya.ru').text)
    print(rt.get('https://ya.ru').text)
    print(rt.get('https://ya.ru').text)
    print(rt.get('https://ya.ru').text)
    print(rt.get('https://ya.ru').text)
    print(rt.get('https://ya.ru').text)
    print(rt.get('https://ya.ru').text)



    res = rt.get_urls(urls)
    for r in res:
        print(r.url, r.text)
    print(Counter(r.text for r in res))

    res2 = rt.get_urls(urls2)
    for r in res2:
        print(r.url, r.text)
    print(Counter(r.text for r in res2))
    

if __name__ == '__main__':
    main()
