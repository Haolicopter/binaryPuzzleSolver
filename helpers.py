#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import os


def elementExist(driver, cssSelector):
    try:
        driver.find_element_by_css_selector(cssSelector)
    except NoSuchElementException:
        return False
    return True


def getChromeDriver():
    chromedriver = "/usr/local/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    chrome_options = Options()
    # This make Chromium reachable
    chrome_options.add_argument("--no-sandbox")
    # Overrides default choices
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--disable-user-media-security=true")
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    return webdriver.Chrome(chromedriver, chrome_options=chrome_options)


def setCellToOne(browser, cell):
    if cell.text == 0:
        ActionChains(browser).click(cell).perform()
    elif cell.text == '':
        ActionChains(browser).click(cell).click(cell).perform()


def setCellToZero(browser, cell):
    if cell.text == '':
        ActionChains(browser).click(cell).perform()
    elif cell.text == '1':
        ActionChains(browser).click(cell).click(cell).perform()


def setCellToNone(browser, cell):
    if cell.text == '1':
        ActionChains(browser).click(cell).perform()
    elif cell.text == '0':
        ActionChains(browser).click(cell).click(cell).perform()
