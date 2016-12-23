import requests
import random
import urllib


def get_proxies_list():
    proxy_list = "http://www.freeproxy-list.ru/api/proxy"
    html = requests.get(proxy_list, params={'anonymity': 'false', 'token': 'demo'}).text
    proxies = html.split('\n')
    return proxies


def load_urls4check(path):
    with open(path) as urls_file:
        return [line.rstrip('\n') for line in urls_file]


def is_server_respond_with_200(url):
    try:
        return requests.get(url).status_code
    except requests.RequestException:
        return


def get_domain_expiration_date(url):
    url = urllib.parse.urlparse(url).netloc
    whois_api = "https://madchecker.com/domain/api/{}".format(url)
    proxy = {"http": random.choice(get_proxies_list())}

    while 1:
        try:
            document = requests.get(whois_api, params={'properties': 'expiration'}, proxies=proxy).json()
            expiration_date = document['data']['expiration']
        except (requests.exceptions.ProxyError, KeyError):
            return 0
        else:
            return expiration_date


def pretty_print(domains_data):
    print(''.center(60, '='), end='\n')
    print('URL STATUS CHECKER'.center(60, ' '), end='\n')
    print(''.center(60, '='), end='\n\n')
    for domain in domains_data:
        print('{}\nStatus: {}\nResponse: {}, Expires On: {}'.format
              (domain[0], domain[3], domain[1], domain[2]), end='\n\n')


def main():
    domains_data = []

    urls = load_urls4check(input('Enter the path to a textfile with urls: '))

    for index, url in enumerate(urls, 1):
        print('fetching url', index, '...')
        response = is_server_respond_with_200(url)

        if response:
            expiration_date = get_domain_expiration_date(url)
            if expiration_date:
                url_status = 'Ok'
            else:
                url_status = 'Not ok'
        else:
            expiration_date, response, url_status = 'n/a', 'n/a', 'Not Ok'

        domains_data.extend([(url, response, expiration_date, url_status)])

    pretty_print(domains_data)

if __name__ == '__main__':
    main()
