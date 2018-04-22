import sys
import os
import datetime
import requests
import whois
from urllib.parse import urlparse


def load_urls4check(filepath):
    with open(filepath, 'r') as file:
        urls_lst = file.read().split('\n')
    return urls_lst


def is_server_respond_ok(url):
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


def get_days_before_expiration(exp_date):
    return (exp_date - datetime.datetime.today()).days


def is_expiration_date_ok(days_before_expiration, days_limit=30):
    return days_before_expiration > days_limit


if __name__ == '__main__':
    if len(sys.argv) == 1:
        exit('need path to file as parameter')
    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        exit('incorrect path to file')
    urls_for_check_list = load_urls4check(filepath)
    for url in urls_for_check_list:
        domain = get_domain_name(url)
        exp_date = get_domain_expiration_date(domain)
        status_code = requests.get(url).status_code
        days_before_expiration = get_days_before_expiration(exp_date)
        condition_status = is_server_respond_ok(url)
        condition_expiration = is_expiration_date_ok(days_before_expiration)
        if condition_status and condition_expiration:
            print(
                'for domain *{}*  :  check status: OK! \n'
                'response status code : {} \n'
                'days before expiration : {} \n'.format(
                    domain, status_code, days_before_expiration
                ))
        else:
            print(
                'for domain *{}*  :  check status: FAILED! \n'
                'response status code : {} \n'
                'days before expiration : {} \n'.format(
                    domain, status_code, days_before_expiration
                ))
