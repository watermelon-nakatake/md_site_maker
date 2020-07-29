import requests


def check_web_data(local_url):
    domain_str = 'https://www.demr.jp/'
    web_url = domain_str + local_url.replace('reibun/', '')