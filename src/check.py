import requests, difflib

url = 'http://browserspy.dk/headers.php'
win10firefox = requests.get(url, headers={
}).text

win10chrome = requests.get(url, headers={
}).text
html_diff = difflib.HtmlDiff()
diff = html_diff.make_file(win10firefox.split('\n'), win10chrome.split('\n'))

headers = {
    'win10 firefox 49': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'browserspy.dk',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    },
    'win10 chrome 54': {
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
    }
}

s = difflib.SequenceMatcher(None, win10firefox, win10chrome)
print(s.ratio())


def save_to_file(str, file_name):
    file = open(file_name, "w")
    file.write(diff)
    file.close()
