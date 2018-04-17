''' Bot to test experiment factory's directed-forgetting
2018 by Matthias Weiler '''

import datetime
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def end_instructions():
    """ end instructions """
    end_instructions_button = DRIVER.find_element_by_xpath(
        '//button[@id="jspsych-instructions-next"]')
    end_instructions_button.click()

def enter_fullscreen_mode():
    """ enter fullscreen mode """
    fullscreen_button = DRIVER.find_element_by_xpath('//button[@id="jspsych-fullscreen-btn"]')
    fullscreen_button.click()

def get_top_stimuli():
    """ get list of letters on top """
    top_stimuli = []
    top_left = DRIVER.find_element_by_xpath('//div[@class="topLeft"]/img')
    top_stimuli.append(top_left.get_attribute("src")[-5:-4])
    top_middle = DRIVER.find_element_by_xpath('//div[@class="topMiddle"]/img')
    top_stimuli.append(top_middle.get_attribute("src")[-5:-4])
    top_right = DRIVER.find_element_by_xpath('//div[@class="topRight"]/img')
    top_stimuli.append(top_right.get_attribute("src")[-5:-4])
    return top_stimuli

def get_bottom_stimuli():
    """ get list of letters on bottom """
    bottom_stimuli = []
    bottom_left = DRIVER.find_element_by_xpath('//div[@class="bottomLeft"]/img')
    bottom_stimuli.append(bottom_left.get_attribute("src")[-5:-4])
    bottom_middle = DRIVER.find_element_by_xpath('//div[@class="bottomMiddle"]/img')
    bottom_stimuli.append(bottom_middle.get_attribute("src")[-5:-4])
    bottom_right = DRIVER.find_element_by_xpath('//div[@class="bottomRight"]/img')
    bottom_stimuli.append(bottom_right.get_attribute("src")[-5:-4])
    return bottom_stimuli

def get_cue():
    """ get current cue """
    cue_img = DRIVER.find_element_by_xpath('//img[@class="forgetStim"]')
    cue = cue_img.get_attribute("src")[-7:-4]
    return cue

def get_probe():
    """ get probe """
    probe_img = DRIVER.find_element_by_xpath('//img[@class="forgetStim"]')
    probe = probe_img.get_attribute("src")[-5:-4]
    return probe

def press_enter_key():
    """ press enter key """
    element_body = DRIVER.find_element_by_tag_name('body')
    element_body.send_keys(Keys.ENTER)

def wait_for_cue(timeout=3):
    """ wait for cue to show up """
    element_present = EC.presence_of_element_located(
        (By.XPATH, '//div[@class="centerbox"]/img[@class="forgetStim"]'))
    WebDriverWait(DRIVER, timeout).until(element_present)

def wait_for_download(timeout=10):
    """ wait for download """
    element_present = EC.presence_of_element_located((By.ID, 'jspsych-download-as-text-link'))
    WebDriverWait(DRIVER, timeout).until(element_present)

def wait_for_fixation(timeout=3):
    """ wait for fixation """
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'fixation'))
    WebDriverWait(DRIVER, timeout).until(element_present)

def wait_for_instructions(timeout=3):
    """ wait for instruction text to show up """
    element_present = EC.presence_of_element_located(
        (By.ID, 'jspsych-poldrack-single-stim-stimulus'))
    WebDriverWait(DRIVER, timeout).until(element_present)

def wait_for_probe(timeout=10):
    """ wait for probe """
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'forgetStim'))
    WebDriverWait(DRIVER, timeout).until(element_present)

def wait_for_stimuli(timeout=10):
    """ wait for stimuli to show up """
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'topLeft'))
    WebDriverWait(DRIVER, timeout).until(element_present)

def wait_for_task_completion(timeout=10):
    """ wait for task completion """
    element_present = EC.presence_of_element_located(
        (By.XPATH, '//div[@class="centerbox"]//p[@class="center-block-text"]'))
    WebDriverWait(DRIVER, timeout).until(element_present)

def run_experiment():
    """ run experiment """
    while True:
        try:
            # wait for stimuli
            wait_for_stimuli()
            # get list of letters on top
            top_stimuli = get_top_stimuli()
            # get list of letters on bottom
            bottom_stimuli = get_bottom_stimuli()
            # wait for cue
            wait_for_cue()
            # get cue ("BOT" of "TOP")
            cue = get_cue()
            # set memory list
            if cue == "TOP":
                memory_list = bottom_stimuli
            else:
                memory_list = top_stimuli
            # wait for fixation
            wait_for_fixation()
            # wait for probe
            wait_for_probe()
            # get probe
            probe = get_probe()
            # answer to probe
            percentage_of_right_answers = 0.8
            percentage_of_wrong_answers = 1 - percentage_of_right_answers
            element_body = DRIVER.find_element_by_tag_name('body')
            if probe in memory_list:
                # Left key is right answer
                key_to_press = np.random.choice(
                    [Keys.LEFT, Keys.RIGHT], 1,
                    p=[percentage_of_right_answers, percentage_of_wrong_answers])
                element_body.send_keys(key_to_press)
            else:
                # Right key is right answer
                key_to_press = np.random.choice(
                    [Keys.RIGHT, Keys.LEFT], 1,
                    p=[percentage_of_right_answers, percentage_of_wrong_answers])
                element_body.send_keys(key_to_press)

        except TimeoutException:
            break

def edit_textarea(area_number, text):
    """ edit textareas for summary and comments """
    answer = DRIVER.find_element_by_xpath(
        '//textarea[@name="#jspsych-survey-text-response-%i"]' % (area_number))
    answer.send_keys("%s" % (text))

def submit_answers():
    """ submit answers """
    submit_answers_button = DRIVER.find_element_by_xpath('//button[@id="jspsych-survey-text-next"]')
    submit_answers_button.click()


# Start timer
START_TIME = datetime.datetime.now()
print('Start experiment: %s' % START_TIME)

# Set webdriver
DRIVER = webdriver.Chrome()

# Open website
DRIVER.get('https://expfactory-experiments.github.io/directed-forgetting/')

# ---- Launch Experiment
enter_fullscreen_mode()

# ---- Welcome to the experiment
press_enter_key()

# ---- Instructions 1
end_instructions()

# ---- Instructions 2 and 3
for i in range(2):
    wait_for_instructions()
    press_enter_key()

# ---- Example
print("Entering example")

# Run example
run_experiment()

# ---- End instructions
end_instructions()

# ---- Practice trials
print("Entering practice trials")

# Run practice trials
run_experiment()

# ---- Experiment and test runs
for i in range(3):
    print("Entering experiment %i" % (i + 1))

    # Start experiment
    press_enter_key()

    # Run experiment
    run_experiment()

    # Exit experiment
    press_enter_key()

# ---- Summary and comments
# Enter summary
edit_textarea(0, "Task summary")

# Enter comment
edit_textarea(1, "Comment")

# Submit answers
submit_answers()

# ---- Task completed
# Wait for task completion
wait_for_task_completion()

# Go to next screen
press_enter_key()

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
