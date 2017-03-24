import argparse
import json
import statistics
from difflib import SequenceMatcher
from urllib.parse import urlparse

import requests
from requests.exceptions import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning

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
    ratios = []
    worst_ratio = 1.0
    diffs = []
    worst_diff = 0
    for browser_index_a, browser_a in enumerate(browsers[:-1]):
        response_a = browser_a['response']
        for browser_index_b, browser_b in enumerate(browsers[browser_index_a + 1:]):
            response_b = browser_b['response']
            matcher = SequenceMatcher(None, response_a, response_b)
            ratio = matcher.ratio()
            ratios.append(ratio)
            matching_blocks = matcher.get_matching_blocks()
            matching_length = sum(match.size for match in matching_blocks)
            max_response_size = max(len(response_a), len(response_b))
            diff = max_response_size - matching_length
            diffs.append(diff)
            if ratio < worst_ratio:
                worst_ratio = ratio
            if diff > worst_diff:
                worst_diff = diff
            print('checking browser {} against browser {} (total: {} browsers) diff: {}'
                  .format(browser_index_a + 1, browser_index_b + browser_index_a + 2,
                          len(browsers), diff))

    result = "MALICIOUS"
    if 0 == worst_diff:
        result = "CLEAN"
    elif worst_diff <= 50:
        result = "SUSPICIOUS"

    return {
        "result": result,
        "info": {
            "medianRatio": statistics.median(ratios),
            "worstRatio": worst_ratio,
            "medianDiff": statistics.median(diffs),
            "worstDiff": worst_diff,
            "browsers": [browser['configuration']['name'] for browser in browsers]
        }
    }


if __name__ == '__main__':
    main()
