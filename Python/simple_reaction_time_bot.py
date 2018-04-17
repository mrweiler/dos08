''' Bot to test experiment factory's simple-reaction-time
2018 by Matthias Weiler '''

import datetime
import time
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
            # wait for stimuli
            wait_for_stimuli()

            # response delay
            time.sleep(.700)

            # press space
            press_key(Keys.SPACE)

        except TimeoutException:
            break

def wait_for_download(timeout=10):
    """ wait for download """
    element_present = EC.presence_of_element_located((By.ID, 'jspsych-download-as-text-link'))
    WebDriverWait(DRIVER, timeout).until(element_present)

def wait_for_experiment(timeout=3):
    """ wait for instruction text to show up """
    element_present = EC.presence_of_element_located(
        (By.XPATH, '//div[@class="centerbox"]//p[@class="block-text"]'))
    WebDriverWait(DRIVER, timeout).until(element_present)

def wait_for_next_screen(timeout=3):
    """ wait for instruction text to show up """
    element_present = EC.presence_of_element_located(
        (By.XPATH, '//div[@class="centerbox"]//p[@class="center-block-text"]'))
    WebDriverWait(DRIVER, timeout).until(element_present)

def wait_for_stimuli(timeout=10):
    """ wait for stimuli to show up """
    element_present = EC.presence_of_element_located((By.ID, 'cross'))
    WebDriverWait(DRIVER, timeout).until(element_present)

def wait_for_summary(timeout=10):
    """ wait for summary to show up """
    element_present = EC.presence_of_element_located((By.ID, 'jspsych-survey-text-preamble'))
    WebDriverWait(DRIVER, timeout).until(element_present)

def wait_for_task_completion(timeout=10):
    """ wait for task completion """
    element_present = EC.presence_of_element_located(
        (By.XPATH, '//div[@class="centerbox"]//p[@class="center-block-text"]'))
    WebDriverWait(DRIVER, timeout).until(element_present)


# Start timer
START_TIME = datetime.datetime.now()
print('Start experiment: %s' % START_TIME)

# Set webdriver
DRIVER = webdriver.Chrome()

# Open website
DRIVER.get('https://expfactory-experiments.github.io/simple-reaction-time/')

# ---- Launch experiment
click_button("Launch Experiment")

# ---- Begin
press_key(key=Keys.ENTER)

# ---- Instructions
click_button("End Instructions")

# ---- Practice trials
# Start practice trials
wait_for_next_screen()
press_key(key=Keys.ENTER)

# Run practice trials
run_experiment()

# ---- Experiment
# Start experiments
wait_for_experiment()
press_key(key=Keys.ENTER)

# Run experiment
for i in range(3):
    # Run experiment
    run_experiment()

    # Break
    wait_for_next_screen()
    press_key(key=Keys.ENTER)

# ---- Summary and comments
# Wait for summary
wait_for_summary()

# Enter summary
edit_textarea(0, "Task summary")

# Enter comment
edit_textarea(1, "Comment")

# Submit answers
click_button("Submit Answers")

# ---- Task completed
# Wait for task completion
wait_for_task_completion()

# Go to next screen
press_key(key=Keys.ENTER)

# Download results
wait_for_download()

# Close browser
DRIVER.close()

# Stop timer
END_TIME = datetime.datetime.now()
print('End experiment: %s' % END_TIME)

# Print timing
DURATION = END_TIME - START_TIME
print('Timing: %s' % DURATION)
