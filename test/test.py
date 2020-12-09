from requestsTor import requestsTor

urls = (f'https://habr.com/ru/post/{x}' for x in range(531522, 531550))
url = 'https://habr.com/ru/post/531622'

def main():
    rt = requestsTor(tor_ports=[9000, 9001, 9002, 9003, 9004], debug=1)
##    print(rt.check_ip())
##    print(rt.get('https://ya.ru').text)
##    rt.new_ip()
##    print(rt.check_ip())
##    print(rt.get('https://r0.ru').text)
    res = rt.get_urls(urls)
    for r in res:
        print(r.url, r.text)
    

    

if __name__ == '__main__':
    main()
