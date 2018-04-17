''' Bot to test experiment factory's emotion-regulation
2018 by Matthias Weiler '''

import datetime
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def click_button(button_text):
    """ simulate button click """
    button = DRIVER.find_element_by_xpath('//button[text()="%s"]' % (button_text))
    button.click()

def edit_textarea(area_number, text):
    """ edit textareas for summary and comments """
    answer = DRIVER.find_element_by_xpath(
        '//textarea[@name="#jspsych-survey-text-response-%i"]' % (area_number))
    answer.send_keys("%s" % (text))

def press_key(key):
    """ press key """
    element_body = DRIVER.find_element_by_tag_name('body')
    element_body.send_keys(key)

def run_experiment():
    """ run experiment """
    while True:
        try:
            wait_for_decision_screen()
            press_key(np.random.choice([Keys.LEFT, Keys.RIGHT], 1))
        except TimeoutException:
            break

def run_practice_trial():
    """ run practice trial """
    while True:
        try:
            wait_for_experiment_screen()
            press_key(key=Keys.ENTER)
        except TimeoutException:
            break

def submit_answers():
    """ submit answers """
    submit_answers_button = DRIVER.find_element_by_xpath('//button[@id="jspsych-survey-text-next"]')
    submit_answers_button.click()

def wait_for_experiment_screen(timeout=20):
    """ wait for instruction text to show up """
    element_present = EC.presence_of_element_located(
        (By.XPATH, '//div[@class="centerbox"]//div[@class="center-block-text"]'))
    WebDriverWait(DRIVER, timeout).until(element_present)

def wait_for_instruction_screen(timeout=3):
    """ wait for instruction text to show up """
    element_present = EC.presence_of_element_located(
        (By.XPATH, '//div[@class="centerbox"]//p[@class="center-block-text"]'))
    WebDriverWait(DRIVER, timeout).until(element_present)

def wait_for_decision_screen(timeout=3):
    """ wait for instruction text to show up """
    element_present = EC.presence_of_element_located(
        (By.ID, 'jspsych-poldrack-single-stim-stimulus'))
    WebDriverWait(DRIVER, timeout).until(element_present)

def wait_for_download(timeout=10):
    """ wait for download """
    element_present = EC.presence_of_element_located((By.ID, 'jspsych-download-as-text-link'))
    WebDriverWait(DRIVER, timeout).until(element_present)


# Start timer
START_TIME = datetime.datetime.now()
print('Start experiment: %s' % START_TIME)

# Set webdriver
DRIVER = webdriver.Chrome()

# Open website
DRIVER.get('https://expfactory-experiments.github.io/emotion-regulation/')

# ---- Launch experiment
click_button("Launch Experiment")

# ---- Begin
press_key(key=Keys.ENTER)

# ---- Instructions
click_button("End Instructions")

# ---- Training and practice trials
# Run training and practice trials
for i in range(2):
    run_practice_trial()

    # Start next block
    wait_for_instruction_screen()
    press_key(key=Keys.ENTER)

# Run test trials
run_experiment()

# ---- Summary and comments
# Enter summary
edit_textarea(0, "Task summary")

# Enter comment
edit_textarea(1, "Comment")

# Submit answers
submit_answers()

# ---- Task completed
# Wait for task completion
wait_for_instruction_screen()

# Go to next screen
press_key(key=Keys.ENTER)

# Wait for download
wait_for_download()

# Close browser
DRIVER.close()

# Stop timer
END_TIME = datetime.datetime.now()
print('End experiment: %s' % END_TIME)

# Print timing
DURATION = END_TIME - START_TIME
print('Timing: %s' % DURATION)
