import argparse
import pprint
from difflib import SequenceMatcher

import requests
from  requests.exceptions import *


def dump(var):
    pprint.pprint(dir(var))


def save_to_file(text, file_name):
    file = open(file_name, "w")
    file.write(text)
    file.close()


parser = argparse.ArgumentParser(description="Test website for Header Inspection.")
parser.add_argument('-u', type=str, required=True, help="specifies the URL to be checked", metavar="URL", dest='url')
parser.add_argument('-i', type=str, help="specifies the ID for this test", metavar="test_id", dest='id')
args = parser.parse_args()

configurations = [
    {
        'name': 'WINDOWS_10_FIREFOX_49',
        'headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'browserspy.dk',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        },
    },
    {
        'name': 'WINDOWS_10_CHROME_45',
        'headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8,de;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'browserspy.dk',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        },
    },
]

try:
    requests.head(args.url)
except RequestException as e:
    print(e)
    exit(2)


def get_responses(list: configurations):
    for configuration in configurations:
        configuration['response'] = requests.get(args.url, headers=configuration['headers']).text


get_responses(configurations)


def calculate_ratios():
    ratios = []
    for config_index, configuration in enumerate(configurations):
        print(config_index + 1)
        for other_config_index, other_headers in enumerate(configurations[config_index + 1:]):
            print('{} - {}'.format(config_index, other_config_index))
            ratio = SequenceMatcher(None, configuration['response'], other_headers['response']).ratio()
            ratios.append(ratio)


calculate_ratios()
# print(ratios[-1])
print(len(configurations))
