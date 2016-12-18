import requests
import random
import urllib


def get_proxies_list():
    proxy_list = "http://www.freeproxy-list.ru/api/proxy?anonymity=false&token=demo"
    html = requests.get(proxy_list).text
    proxies = html.split('\n')
    return proxies


def load_urls4check(path):
    return [line.rstrip('\n') for line in open(path)]


def is_server_respond_with_200(url):
    try:
        return requests.get(url).status_code
    except requests.RequestException:
        print('It seems that', url, 'is down')


def get_domain_expiration_date(url):
    url = urllib.parse.urlparse(url).netloc
    whois_api = "https://madchecker.com/domain/api/{}?properties=expiration"
    proxy = {"http": random.choice(get_proxies_list())}

    while 1:
        try:
            document = requests.get(whois_api.format(url), proxies=proxy).json()
            expiration_date = document['data']['expiration']
        except (requests.exceptions.ProxyError, KeyError):
            return 'Unknown'
        else:
            return expiration_date


def pretty_print(domains_data):
    print(''.center(60, '='), end='\n')
    print('URL STATUS CHECKER'.center(60, ' '), end='\n')
    print(''.center(60, '='), end='\n\n')
    for domain in domains_data:
        print('Url: {}\nStatus: {}\nExpires on: {}'.format(domain[0], domain[1], domain[2]), end='\n\n')


def main():
    domains_data = []
    urls = load_urls4check(input('Enter the path to a textfile with urls: '))

    for index, url in enumerate(urls, 1):
        print('fetching url', index, '...')
        status = is_server_respond_with_200(url)
        if status:
            expiration_date = get_domain_expiration_date(url)
            domains_data.extend([(url, status, expiration_date)])

    pretty_print(domains_data)

if __name__ == '__main__':
    main()
