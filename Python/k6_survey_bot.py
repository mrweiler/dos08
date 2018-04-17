''' Bot to test experiment factory's k6-survey
2018 by Matthias Weiler '''
import datetime
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def answer_checkbox(question_block, number_of_options, none_option):
    """ answer checkboxes """
    number_of_answers = np.random.choice(number_of_options, 1)
    check_list = np.random.choice(number_of_options, number_of_answers, replace=False)

    if number_of_answers == 0:
        answer = DRIVER.find_element_by_xpath(
            '//label[@for="checkbox-k6-survey_%i_%i"]' % (question_block, none_option))
        answer.click()
    elif none_option in check_list:
        answer = DRIVER.find_element_by_xpath(
            '//label[@for="checkbox-k6-survey_%i_%i"]' % (question_block, none_option))
        answer.click()
    else:
        for checked_item in check_list:
            answer = DRIVER.find_element_by_xpath(
                '//label[@for="checkbox-k6-survey_%i_%i"]' % (question_block, checked_item))
            answer.click()

def answer_likert_items(question_block, number_of_questions, number_of_options):
    """ answer likert items """
    for i in range(number_of_questions):
        answer = DRIVER.find_element_by_xpath(
            '//label[@for="option-k6-survey_%i_%i"]' % (i + question_block, np.random.choice(
                number_of_options, 1)))
        answer.click()

def answer_textfield(question_block, number_of_questions, textfield):
    """ answer textfield """
    for i in range(number_of_questions):
        answer = DRIVER.find_element_by_xpath(
            '//input[@name="k6-survey_%i"]' % (i + question_block))
        answer.send_keys("%s" % textfield)

def click_button(button_text):
    """ simulate button click """
    button = DRIVER.find_element_by_xpath('//button[text()="%s"]' % (button_text))
    button.click()

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
DRIVER.get('https://expfactory-experiments.github.io/k6-survey/')

# ---- Instructions
click_button("Next")

# Go to next screen
click_button("Next")

# ---- Survey part 1
# Q1
answer_likert_items(question_block=3, number_of_questions=6, number_of_options=5)

# Q2
answer_likert_items(question_block=9, number_of_questions=1, number_of_options=7)

# Go to next screen
click_button("Next")

# ---- Survey part 2
# Q3
answer_textfield(question_block=11, number_of_questions=1, textfield=np.random.choice(30, 1))

# Q4
answer_textfield(question_block=12, number_of_questions=1, textfield=np.random.choice(30, 1))

# Q5
answer_textfield(question_block=13, number_of_questions=1, textfield=np.random.choice(30, 1))

# Q6
answer_likert_items(question_block=14, number_of_questions=1, number_of_options=5)

# Go to next screen
click_button("Next")

# ---- Survey part 2
# Psychological disorders
answer_checkbox(question_block=15, number_of_options=14, none_option=13)

# "other" option is checked
OTHER_OPTION = DRIVER.find_element_by_xpath('//label[@for="checkbox-k6-survey_%i_%i"]' % (15, 12))
if "is-checked" in OTHER_OPTION.get_attribute("class"):
    answer_textfield(
        question_block=16, number_of_questions=1, textfield="Other psychological disorder")

# Neurological disorders
answer_likert_items(question_block=17, number_of_questions=1, number_of_options=2)

# "yes" option is checked
YES_OPTION = DRIVER.find_element_by_xpath('//label[@for="option-k6-survey_%i_%i"]' % (17, 0))
if "is-checked" in YES_OPTION.get_attribute("class"):
    answer_textfield(
        question_block=18, number_of_questions=1, textfield="Other neurological disorder")

# Medical conditions
answer_checkbox(question_block=19, number_of_options=9, none_option=8)

# "other" option is checked
OTHER_OPTION = DRIVER.find_element_by_xpath('//label[@for="checkbox-k6-survey_%i_%i"]' % (19, 7))
if "is-checked" in OTHER_OPTION.get_attribute("class"):
    answer_textfield(
        question_block=20, number_of_questions=1, textfield="Other psychological disorder")

# Go to next screen
click_button("Next")

# ---- Survey part 3
click_button("Finish")

# Wait for download screen
wait_for_download_screen()

# ---- Survey part 4
click_button("Download")

# Wait for download
wait_for_download_completion()

# Close browser
DRIVER.close()

# Stop timer
END_TIME = datetime.datetime.now()
print('End experiment: %s' % END_TIME)

# Print timing
DURATION = END_TIME - START_TIME
print('Timing: %s' % DURATION)
