import datetime
import requests
import whois
import argparse
from urllib.parse import urlparse


def load_urls4check(filepath):
    with open(filepath, 'r') as file:
        urls_lst = file.read().split('\n')
    return urls_lst


def is_server_respond_ok(url):
    try:
        return requests.get(url).ok
    except requests.exceptions.RequestException:
        return False


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


def get_parsed_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', type=str, help='path to text-file')
    return parser.parse_args()


def print_check_message(
        is_server_respond,
        is_exp_date_correct,
        domain, days_before_exp
):
    if is_server_respond and is_exp_date_correct:
        general_check_status = 'SUCCESS!'
    else:
        general_check_status = 'FAILED!'
    server_response_status = 'OK' if is_server_respond else 'NO RESPONSE'
    print('for domain "{}"  :  check status: {}'.format(
        domain,
        general_check_status
    ))
    print('server response : {}'.format(server_response_status))
    print('days before expiration : {}'.format(days_before_exp))


if __name__ == '__main__':
    separator = '*' * 30
    arg = get_parsed_argument()
    filepath = arg.filepath
    try:
        urls_for_check_list = load_urls4check(filepath)
    except(FileNotFoundError, UnicodeDecodeError):
        exit('incorrect path to file / not a text file')
    for url in urls_for_check_list:
        is_server_respond = is_server_respond_ok(url)
        domain = get_domain_name(url)
        exp_date = get_domain_expiration_date(domain)
        days_before_exp = get_days_before_expiration(exp_date)
        is_exp_date_correct = is_expiration_date_ok(days_before_exp)
        print_check_message(
            is_server_respond,
            is_exp_date_correct,
            domain,
            days_before_exp
        )
        print(separator)
