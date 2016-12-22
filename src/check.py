import argparse
import json
from difflib import SequenceMatcher
from urllib.parse import urlparse

import numpy.core
import requests
from requests.exceptions import *

from collect import read_browsers


def main():
    parser = argparse.ArgumentParser(description="Test website for Header Inspection.")
    parser.add_argument('-u', type=str, required=True, help="specifies the URL to be checked", metavar="URL",
                        dest='url')
    parser.add_argument('-i', type=str, help="specifies the ID for this test", metavar="test_id", dest='id')
    args = parser.parse_args()

    try:
        requests.head(args.url)
    except RequestException as e:
        print(e)
        exit(2)

    browsers = read_browsers()

    fetch_responses(browsers, args.url)

    result = generate_result(browsers)

    output = '{}: {}'.format(args.id, json.dumps(result))
    print(output)


def fetch_responses(browsers, url):
    for browser in browsers:
        parse = urlparse(url)
        host = parse.netloc or None
        if host:
            browser['headers']['Host'] = host
        browser['response'] = requests.get(url, headers=browser['headers']).text


def generate_result(browsers):
    result = "clean"
    ratios = []
    worst_ratio = 1.0
    for browser_index, browser in enumerate(browsers[:-1]):
        for other_browser_index, other_browser in enumerate(browsers[browser_index + 1:]):
            ratio = SequenceMatcher(None, browser['response'], other_browser['response']).ratio()
            ratios.append(ratio)
            if ratio < worst_ratio:
                worst_ratio = ratio
                if ratio < 0.999:
                    result = "suspicious"

        mean_ratio = numpy.mean(ratios)
        browser['meanRatio'] = mean_ratio

    return {
        "result": result,
        "info": {
            "meanRatio": numpy.mean(ratios),
            "worstRatio": worst_ratio,
            "browsers": [browser['configuration']['name'] for browser in browsers]
        }
    }


if __name__ == '__main__':
    main()
