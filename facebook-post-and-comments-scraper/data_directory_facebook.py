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
                        "div", class_="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a"
                    )
                    print(post_content.text.encode('utf-8').decode('unicode_escape'))
                    comments = post.find_all(
                        "div", class_="x1y1aw1k xn6708d xwib8y2 x1ye3gou"
                    )
                    if post_content and post_content.text not in results["posts"]:
                        results["posts"].append(post_content.text.encode('utf-8').decode('unicode_escape'))
                        results["comments"].extend(
                            [comment.text for comment in comments if comment]
                        )

        except Exception as e:
            logger.error(f"Error scraping posts: {e}")
        return results
    def extract_posts(self):
        #results = {"posts" : [], "comments" : []}
        results = {}
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
            # Scroll back to the top of the page
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(3)  # Wait for the page to scroll to the top
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            posts = soup.find_all("div", class_="x78zum5 x1n2onr6 xh8yej3")
            leave_comment_buttons = self.driver.find_elements(By.XPATH, f"//div[@aria-label='Leave a comment' and @role='button']")
            for index, post in enumerate(posts):
                    post_content = post.find("div", class_="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a")
                    if post_content:
                        selenium_post = self.driver.find_element(By.XPATH, f"//div[contains(text(), '{post_content.text[:10]}')]")
                        #Find the "See more" button
                        try:
                            see_more_button = selenium_post.find_element(By.XPATH, ".//div[contains(text(), 'See more')]")
                            see_more_button.click()
                        except Exception as e:
                            print("this post dont have extra content", e)
                        #Find all the content of that post
                        first_paragraph =  post.find("div", class_="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a")
                        content_post = first_paragraph.text.strip()
                        try:
                            sub_paragraph = post.find_all("div", class_="x11i5rnm xat24cr x1mh8g0r x1vvkbs xtlvy1s x126k92a")
                            for paragraph in sub_paragraph:
                                content_post += '\n' + paragraph.text.strip() 
                        except Exception as e:
                            print("this post dont have sub paragrpahs", e)
                    # Find the "Leave a comment" button within the post
                        comment_count_element = post.find("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa")
                        if comment_count_element:
                            leave_comment_buttons[index].click()
                            time.sleep(3)
                            soup = BeautifulSoup(self.driver.page_source, "html.parser")
                            comments = soup.find_all("div", class_="x1y1aw1k xn6708d xwib8y2 x1ye3gou")
                            if content_post not in results:
                                results[content_post] = []
                        
                            for comment in comments:
                                results[content_post].append(comment.text.strip())
                            # if post_content and post_content.text not in results["posts"]:
                            #     results["posts"].append(post_content.text)
                            #     for comment in comments:
                            #         results["comments"].append(comment.text)
                            #     # results["comments"].extend(
                            #     #     [comment.text for comment in comments if comment]
                            #     # )
                            close_comment_buton = self.driver.find_element(By.XPATH, f"//div[@aria-label='Close' and @role='button']")
                            close_comment_buton.click()
                            # Wait for the comment section to close
                            time.sleep(3)
                            # Re-fetch the page source to ensure we're not extracting comments from an old view
                            # soup = BeautifulSoup(self.driver.page_source, "html.parser")
                    else:
                        continue
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
        password_field.send_keys('sdsfdsfd')
        
        # Find and click the login button
        login_button = self.driver.find_element(By.NAME, 'login')
        login_button.click()
        
        # Allow time for the login process to complete
        time.sleep(10)

    # Method to search
    def search_topic(self):
        # Click the element using JavaScript
        elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.x1n2onr6.x1ja2u2z.x78zum5.x2lah0s.xl56j7k.x6s0dn4.xozqiw3.x1q0g3np.xi112ho.x17zwfj4.x585lrc.x1403ito.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1qhmfi1.x1r1pt67.x1jdnuiz.x1x99re3')

# Check if the 4th element exists and click on it
        if len(elements) >= 4:
            elements[3].click()  # Index is 3 because it's zero-based (0 is the first element)
        else:
            print("The 4th element was not found.")
        # Locate the element using CSS Selector with placeholder attribute
        search_field = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Search this group"]')
        # Enter a search query
        search_field.send_keys('"thầy" "cô" "review" "môn"')
        search_field.send_keys(Keys.RETURN)
        time.sleep(3)
        # bỏ bước này vì mặc định sẽ hiển thị những bài viết có tương tác cao lên trước => lấy được nhiều reivew hơn
        # checkbox = self.driver.find_element(By.XPATH, '//input[@aria-label="Most recent"]')
        # if not checkbox.is_selected():
        #     checkbox.click()  # Click the checkbox to check it
        # time.sleep(5)
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
    for post, comments in results.items():
       post_data = {"post": post, "comments": comments}
       all_posts.append(post_data)
    
    # Write the list of posts to a JSON file
    with open("facebook_posts.json", "w", encoding="utf-8") as file:
       json.dump(all_posts, file, ensure_ascii=False, indent=4)

    # Write the list of posts to a JSON file
    with open("facebook_posts.json", "w", encoding="utf-8") as file:
        json.dump(all_posts, file, ensure_ascii=False, indent=4)
        # Close the browser
        selenium.close_browser(chrome_driver)
