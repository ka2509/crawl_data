# Description: This script automates the process of extracting Facebook posts and comments from the EGO Power+ Facebook page.
# Author: harmindesinghnijjar
# Date: 2023-12-08
# Version: 1.0.0
# Usage: python Facebook_automation.py

# Import modules.
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import getpass
import os
import time
import logging
import bs4
from bs4 import BeautifulSoup
import requests
import re

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("fb_post_scraper", mode="a")
log_format = logging.Formatter(
    "%(asctime)s - %(name)s - [%(levelname)s] [%(pathname)s:%(lineno)d] - %(message)s - [%(process)d:%(thread)d]"
)
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

print = logger.info

# Set username.
user = getpass.getuser()


def add_colon_between_names(text):
    """
    Inserts a colon and a space between the last lowercase letter and the first uppercase letter.
    Args:
    text (str): The input string.

    Returns:
    str: The modified string with a colon and a space inserted.
    """
    return re.sub(r"([a-z])([A-Z])", r"\1: \2", text)


# Initialize an empty list to store the post data
all_posts = []


# Define a Selenium class to automate the browser.
class Selenium:
    # Constructor method.
    def __init__(self, driver):
        self.driver = driver

    def extract_posts(self):
        results = {"posts": [], "comments": []}
        try:
            last_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )

            # Scroll for 10 seconds
            start_time = time.time()
            end_time = start_time + 10
            while time.time() < end_time:
                # Scroll down to bottom
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )

                # Wait to load page
                time.sleep(3)

                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script(
                    "return document.body.scrollHeight"
                )
                if new_height == last_height:
                    break
                last_height = new_height

                # Extract posts and comments after the page has loaded
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                posts = soup.find_all("div", class_="x78zum5 x1n2onr6 xh8yej3")

                for post in posts:
                    post_content = post.find(
                        "div", class_="x1iorvi4 x1pi30zi x1l90r2v x1swvt13"
                    )
                    comments = post.find_all(
                        "div", class_="x1y1aw1k xn6708d xwib8y2 x1ye3gou"
                    )
                    if post_content and post_content.text not in results["posts"]:
                        results["posts"].append(post_content.text)
                        results["comments"].extend(
                            [comment.text for comment in comments if comment]
                        )

        except Exception as e:
            logger.error(f"Error scraping posts: {e}")
        return results
    
    #Method to login
    def login(self):
        self.driver.get("https://www.facebook.com/login")
        
        # Allow page to load
        time.sleep(5)
        
        # Find and fill the email field
        email_field = self.driver.find_element(By.ID, 'email')
        email_field.send_keys('doquanganhzzz2k3@gmail.com')
        
        # Find and fill the password field
        password_field = self.driver.find_element(By.ID, 'pass')
        password_field.send_keys('Eocopas12345677')
        
        # Find and click the login button
        login_button = self.driver.find_element(By.NAME, 'login')
        login_button.click()
        
        # Allow time for the login process to complete
        time.sleep(10)

    # Method to search
    def search_topic(self):
        # Click the element using JavaScript
        element = self.driver.find_element(By.XPATH, '//div[@class="x1n2onr6 x1ja2u2z x78zum5 x2lah0s xl56j7k x6s0dn4 xozqiw3 x1q0g3np xi112ho x17zwfj4 x585lrc x1403ito x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1qhmfi1 x1r1pt67 x1jdnuiz x1x99re3"]')
        self.driver.execute_script("arguments[1].click();", element)

        # Locate the element using CSS Selector with placeholder attribute
        search_field = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Search this group"]')
        # Enter a search query
        search_field.send_keys('Lê Khánh Trình')
        search_field.send_keys(Keys.RETURN)

        time.sleep(5)
    # Method to open Facebook in Chrome.
    def open_Facebook_posts(self):

        self.driver.get("https://www.facebook.com/groups/188355961296813")
        time.sleep(5)

    def insert_data_into_csv(self, post, comments):
        try:
            with open("facebook_posts.csv", "a", encoding="utf-8") as f:
                f.write(f"{post},{comments}\n")
        except Exception as e:
            logger.error(f"Error writing to csv: {e}")

    # Method to close the Chrome instance.
    def close_browser(self, driver):
        """
        Closes the web browser.

        Args:
        driver (selenium.webdriver.Chrome): The Chrome web driver object.

        Returns:
        None
        """
        self.driver.quit()


if __name__ == "__main__":
    # Kill any existing Chrome instances to avoid conflicts
    os.system("taskkill /im chrome.exe /f")

    # Fetch current user's name
    user = getpass.getuser()

    # Set up ChromeDriver service
    service = Service(executable_path="C:\\Users\\doqua\\Downloads\\chromedriver-win64\\chromedriver.exe")


    # Define Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument(
        f"--user-data-dir=C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data"
    )
    options.add_argument("--profile-directory=Default")

    # Create a WebDriver instance
    chrome_driver = webdriver.Chrome(service=service, options=options)

    # Create an instance of Selenium
    selenium = Selenium(driver=chrome_driver)
    
    # Login to Facebook
    # selenium.login()

    # Open Facebook in Chrome
    selenium.open_Facebook_posts()

    # Search Topic
    selenium.search_topic()

    # Extract posts and comments
    results = selenium.extract_posts()

    # Assuming results is a dictionary with 'posts' and 'comments' keys
    for post, comments in zip(results["posts"], results["comments"]):
       post_data = {"post": post, "comments": add_colon_between_names(comments)}
       all_posts.append(post_data)
    
    # Write the list of posts to a JSON file
    with open("facebook_posts.json", "w", encoding="utf-8") as file:
       json.dump(all_posts, file, ensure_ascii=False, indent=4)

    # Write the list of posts to a JSON file
    with open("facebook_posts.json", "w", encoding="utf-8") as file:
        json.dump(all_posts, file, ensure_ascii=False, indent=4)
        # Close the browser
        selenium.close_browser(chrome_driver)
