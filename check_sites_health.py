import sys
import os
import datetime
import requests
import whois
from urllib.parse import urlparse


def load_urls4check(path):
    with open(path, 'r') as file:
        urls_lst = file.read().split('\n')
    return urls_lst


def is_server_respond_with_200(url):
    response = requests.get(url)
    if response.ok:
        return True


def get_domain_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain


def get_domain_expiration_date(domain_name):
    domain_info = whois.whois(domain_name)
    if type(domain_info.expiration_date) is list:
        return domain_info.expiration_date[0]
    else:
        return domain_info.expiration_date


if __name__ == '__main__':
    if len(sys.argv) == 1:
        exit('need path to file as parameter')
    path = sys.argv[1]
    if not os.path.isfile(path):
        exit('incorrect path to file')
    check_list = load_urls4check(path)
    for url in check_list:
        domain = get_domain_name(url)
        exp_date = get_domain_expiration_date(domain)
        days_limit = 30
        condition_status = is_server_respond_with_200(url)
        condition_expiration = exp_date - datetime.datetime.today() > \
            datetime.timedelta(days_limit)
        if condition_status and condition_expiration:
            print('***{}***    check status: OK!'.format(domain))
        else:
            print('***{}***    check status: FAILED!'.format(domain))
