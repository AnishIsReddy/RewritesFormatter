from typing import Text
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import graphics
import sys

# Create input window
win = graphics.GraphWin(title="Rewrites Input", width=500, height=200)
domain = graphics.Text(graphics.Point(355, 25), "@stu.novik12.org")
EmailLabel = graphics.Text(graphics.Point(80, 25), "Email:")
PasswordLabel = graphics.Text(graphics.Point(64, 75), "Password:")
LinkLabel = graphics.Text(graphics.Point(85, 125), "Link:")
SubmitButton = graphics.Rectangle(graphics.Point(200, 150), graphics.Point(250, 175))
SubmitButtonLabel = graphics.Text(graphics.Point(225, 162), "Enter")

inputs = [graphics.Entry(graphics.Point(200, 25), 20), graphics.Entry(graphics.Point(200, 75), 20), graphics.Entry(graphics.Point(200, 125), 20)]

for i in inputs:
    i.setFill('#D3D3D3')
    i.draw(win)

SubmitButton.setFill('#D3D3D3')
SubmitButton.draw(win)
SubmitButtonLabel.draw(win)
domain.draw(win)
EmailLabel.draw(win)
PasswordLabel.draw(win)
LinkLabel.draw(win)


# Get input from user
while True:
    click = win.getMouse()
    if abs(click.getX() - 225) <= 25 and abs(click.getY() - 163) <= 13:

        SubmitButton.setFill('gray')
        time.sleep(0.05)

        email = inputs[0].getText() + domain.getText()
        password = inputs[1].getText()
        link = inputs[2].getText()

        SubmitButton.setFill('#D3D3D3')
        time.sleep(0.1)

        win.close()
        break

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

# Get all possible answers and their correction stats
answers = []
for i in driver.find_elements(By.CLASS_NAME, "lrn-accessibility-label"):
    val = i.get_attribute('innerHTML').split(" - ")
    answers = answers + [val]

driver.quit()

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

sys.exit(0)