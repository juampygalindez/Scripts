from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
from dotenv import load_dotenv
import shutil

load_dotenv()

folderPath = os.getenv("FILES_FOLDER")
folderBackupPath = os.getenv("BACKUP_FOLDER")
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")


# List of file names on the folder
files = os.listdir(folderPath)

# Start Chrome browser with Selenium
driver = webdriver.Chrome()

# Maximize browser window
driver.maximize_window()

# Login to Pinterest 
driver.get("https://www.pinterest.com/login/")
time.sleep(2)

# Complete the login form
emailField = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
emailField.send_keys(email)
time.sleep(2) 

passField = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
passField.send_keys(password)
passField.send_keys(Keys.RETURN)
time.sleep(5) 

# Navigate to the page to upload files
driver.get("https://www.pinterest.com/pin-creation-tool/")
time.sleep(2) 


# Upload each file 
for file in files:

    completeFolderPath = os.path.join(folderPath, file)

    fileName = file.split(".")[0]
    
    # Find the upload button
    uploadButton = driver.find_element(By.CSS_SELECTOR, "input[data-test-id='storyboard-upload-input']")
    
    # Upload file
    uploadButton.send_keys(completeFolderPath)
    
    # Wait a moment to load file
    time.sleep(5)  

    # Complete title field with the file name
    titleField = driver.find_element(By.ID, "storyboard-selector-title")
    titleField.send_keys(fileName)
    time.sleep(2)

    # Select board selector
    boardSelector = driver.find_element(By.CSS_SELECTOR, "button[data-test-id='board-dropdown-select-button']")
    boardSelector.click()
    time.sleep(2)

    # Search board. In this case, search "Recetas"
    board = driver.find_element(By.CSS_SELECTOR, "div[data-test-id='board-row-Recetas']")
    board.click()
    time.sleep(2)

    # Find the publish button
    publishButton = driver.find_element(By.CSS_SELECTOR, "button[class*='RCK'][class*='USg'][class*='adn'][class*='CCY'][class*='NTm'][class*='KhY']")
    publishButton.click()

    # Move the file to backup folder
    shutil.move(completeFolderPath, os.path.join(folderBackupPath, file))

    # Continue if found upload button
    uploadButtonFound = None
    while not uploadButtonFound:
        try:
            uploadButtonFound = driver.find_element(By.CSS_SELECTOR, "input[data-test-id='storyboard-upload-input']")
        except:
            time.sleep(1)  # Wait 1 second before try again

# Close the browser when finished
driver.quit()

