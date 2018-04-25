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
    try:
        return requests.get(url).ok
    except requests.exceptions.RequestException:
        print('error for get a response from server')


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
    if exp_date:
        return (exp_date - datetime.datetime.today()).days
    else:
        return 0


def is_expiration_date_ok(days_before_expiration, days_limit=30):
    return days_before_expiration > days_limit


def print_check_message(condition_stat, condition_exp, domain, days_before_exp):
    if condition_stat and condition_exp:
        check_value = 'OK!'
    else:
        check_value = 'FAILED!'
    print('for domain "{}"  :  check status: {}'.format(domain, check_value))
    print('server response : {}'.format(check_value))
    print('days before expiration : {}'.format(days_before_exp))


if __name__ == '__main__':
    separator = '*' * 30
    if len(sys.argv) == 1:
        exit('need path to file as parameter')
    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        exit('incorrect path to file')
    urls_for_check_list = load_urls4check(filepath)
    for url in urls_for_check_list:
        condition_status = is_server_respond_ok(url)
        domain = get_domain_name(url)
        exp_date = get_domain_expiration_date(domain)
        days_before_exp = get_days_before_expiration(exp_date)
        condition_expiration = is_expiration_date_ok(days_before_exp)
        print_check_message(
            condition_status,
            condition_expiration,
            domain,
            days_before_exp
        )
        print(separator)
