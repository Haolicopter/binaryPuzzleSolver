#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import os


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


def drawCell(browser, cell, val):
    if val == 1:
        drawOne(browser, cell)
    elif val == 0:
        drawZero(browser, cell)
    else:
        drawNone(browser, cell)


def drawOne(browser, cell):
    if cell.text == 0:
        ActionChains(browser).click(cell).perform()
    elif cell.text == '':
        ActionChains(browser).click(cell).click(cell).perform()


def drawZero(browser, cell):
    if cell.text == '':
        ActionChains(browser).click(cell).perform()
    elif cell.text == '1':
        ActionChains(browser).click(cell).click(cell).perform()


def drawNone(browser, cell):
    if cell.text == '1':
        ActionChains(browser).click(cell).perform()
    elif cell.text == '0':
        ActionChains(browser).click(cell).click(cell).perform()
