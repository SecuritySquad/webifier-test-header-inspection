import json
import os

from selenium.webdriver.remote.webdriver import WebDriver as Remote


def get_mandatory_env(env: str) -> str:
    try:
        return os.environ[env]
    except KeyError:
        print("Please specify the environment variable: '" + env + "'")
        exit(2)


SAUCE_USERNAME = get_mandatory_env('SAUCE_USERNAME')
SAUCE_ACCESS_KEY = get_mandatory_env('SAUCE_ACCESS_KEY')
COMMAND_EXECUTOR = "http://" + SAUCE_USERNAME + ":" + SAUCE_ACCESS_KEY + "@ondemand.saucelabs.com:80/wd/hub"

with open('../res/browsers.json', 'r') as browsersFile:
    browsers = json.load(browsersFile)

for browser in browsers:
    driver = Remote(command_executor=COMMAND_EXECUTOR, desired_capabilities=browser)
    driver.get("http://www.reliply.org/tools/requestheaders.php")

    headerRows = driver.find_elements_by_css_selector('tr')
    headerRows = iter(headerRows)
    next(headerRows)
    next(headerRows)

    headers = {}

    for headerRow in headerRows:
        cells = headerRow.find_elements_by_tag_name('td')
        headerName = cells[0].text
        headerValue = cells[1].text
        headers[headerName] = headerValue

    browsers.append(headers)

    driver.quit()

with open('../res/headers.json', 'w') as headersFile:
    json.dump(browsers, headersFile, indent=4)
