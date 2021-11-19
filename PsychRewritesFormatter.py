from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Input email and password
email = input("Enter your full student email (With domain): ")
password = input("Enter Password: ")
link = input("Enter the URL to your psych test: ")

# Navigate to the page
driver = webdriver.Chrome('chromedriver.exe')
driver.get("https://novi.schoology.com/home#/?_k=io2lml")
driver.find_element(By.ID, 'identifierId').send_keys(email + Keys.ENTER)
time.sleep(2)
driver.find_element(By.NAME, 'password').send_keys(password + Keys.ENTER)
time.sleep(3)
driver.get(link)
time.sleep(3)
driver.find_element(By.PARTIAL_LINK_TEXT, 'View').click()
time.sleep(3)

# Get the questions
questions = []
for i in driver.find_elements(By.CLASS_NAME, "lrn_stimulus_content"):
    questions.append(i.text)

# Get all possible answers and their correction st
answers = []
for i in driver.find_elements(By.CLASS_NAME, "lrn-accessibility-label"):
    val = i.get_attribute('innerHTML').split(" - ")
    answers = answers + [val]

# Compile output
out = []
store = ""
CaughtWrong = False
for i in range(len(answers)):
    if i % 5 == 0:
        out = out + ["\n"]
        out = out + ["\n"]

        CaughtWrong = False
        store = ""

        out = out + [str(i//5 + 1) + ") " + questions[i // 5] + "\n"]
        out = out + ["\n"]
    
    if answers[i][1] == "correct":
        out = out + [answers[i][0] + " is correct\n"]
        out = out + ["Define: \n"]
        out = out + ["Apply: \n"]


    elif answers[i][1] == "incorrect":
        out = out + [answers[i][0] + " is incorrect\n"]
        out = out + ["Define: \n"]
        out = out + ["Apply: \n"]
        CaughtWrong = True

        if len(store) > 0:
            out = out + [store + " is correct\n"]
            out = out + ["Define: \n"]
            out = out + ["Apply: \n"]

    elif answers[i][1] == " not selected, this is the correct answer" and CaughtWrong == False:
        store = answers[i][0]

    elif answers[i][1] == " not selected, this is the correct answer":
        out = out + [answers[i][0] + " is correct\n"]
        out = out + ["Define: \n"]
        out = out + ["Apply: \n"]

# Send data to output file
f = open('output.txt', 'w')
f.writelines(out[2:])
f.close()
exit()