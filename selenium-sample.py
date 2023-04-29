#!/usr/bin/env python

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def waitfor(driver, path, delay=10):
    # This is a utility method to instruct Selenium to wait until
    # the browser is "ready" for input.
    return WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, path))
    )


def login(driver, username, password):
    # This is the "meat" of the function, which shows automating interaction
    # with the SCA member portal

    # Browse to the "Login" screen for the membership portal
    driver.get("https://members.sca.org/apps/#SignIn")

    # Since the page is dynamically built in Javascript, wait until the
    # "Login" form is rendered.
    waitfor(driver, '//button[text()="Login"]')
    # Find the first two input boxes, which correspond to username and password
    username_entry, password_entry = driver.find_elements_by_xpath("//input")[:2]

    # Type the username
    username_entry.send_keys(username)
    # Type the password
    password_entry.send_keys(password)

    # Since the "Login" button only becomes available after the browser thinks
    # a usernamd and password have been provided, wait for the login button to
    # become available, then click it.
    waitfor(driver, '//button[text()="Login" and @aria-disabled="false"]').click()

    # wait until the page loads, which will include the phrase "My Membership"
    waitfor(driver, '//h1[text()="My Membership"]')

    # If the program reaches here, the user has succesfully logged in. YAY.
    print("login successful")


def main():
    # This is the primary function

    # For ease of use during development, use the SCA username and password
    # stored in the Environment Variables rather than re-typing them.
    username = os.environ["SCA_USERNAME"]
    password = os.environ["SCA_PASSWORD"]

    # Setup the basic options for Chrome
    options = Options()

    # Specify the size of the browser (1920x1080 mirrors my laptop, so use that)
    options.add_argument("--window-size=1920x1080")

    # Specify running chrome without a GUI. Disable this to observe Chrome's
    # interactions as it occurs
    options.add_argument("--headless")

    # Specify the Google provided plugin for Selenium to interact with Chrome
    executable_path = "/usr/bin/chromedriver"

    # Launch selenium
    driver = webdriver.Chrome(options=options, executable_path=executable_path)

    # Attempt to login using Chrome
    login(driver, username, password)


if __name__ == "__main__":
    main()
