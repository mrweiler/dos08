''' Bot to test experiment factory's brief-self-control-survey
2018 by Matthias Weiler '''
import datetime
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def click_button(button_text):
    """ simulate button click """
    button = DRIVER.find_element_by_xpath('//button[text()="%s"]' % (button_text))
    button.click()

def answer_likert_items(question_block, number_of_questions, number_of_options):
    """ answer likert items """
    for i in range(number_of_questions):
        answer = DRIVER.find_element_by_xpath(
            '//label[@for="option-brief-self-control-survey_%i_%i"]' % (
                i + question_block, np.random.choice(number_of_options, 1)))
        answer.click()

def wait_for_download_screen(timeout=10):
    """ wait until download screen appears """
    element_present = EC.presence_of_element_located((By.XPATH, '//button[text()="Download"]'))
    WebDriverWait(DRIVER, timeout).until(element_present)

def wait_for_download_completion(timeout=10):
    """ wait until download is complete """
    element_present = EC.presence_of_element_located((By.ID, 'download'))
    WebDriverWait(DRIVER, timeout).until(element_present)


# Start timer
START_TIME = datetime.datetime.now()
print('Start experiment: %s' % START_TIME)

# Set webdriver
DRIVER = webdriver.Chrome()

# Open website
DRIVER.get('https://expfactory-experiments.github.io/brief-self-control-survey/')

# Welcome screen
click_button("Next")

# Instructions
click_button("Next")

# Survey
answer_likert_items(question_block=2, number_of_questions=13, number_of_options=5)
click_button("Next")

# Finish survey
click_button("Finish")

# Wait for download screen
wait_for_download_screen()

# Download results
click_button("Download")

# Wait until download is complete
wait_for_download_completion()

# Close browser
DRIVER.close()

# Stop timer
END_TIME = datetime.datetime.now()
print('End experiment: %s' % END_TIME)

# Print timing
DURATION = END_TIME - START_TIME
print('Timing: %s' % DURATION)
