import json
from selenium import webdriver
from lxml import etree
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

def get_full_xpath(element):
    components = []
    while element is not None and element.name != '[document]':
        siblings = element.find_previous_siblings(element.name)
        index = len(siblings) + 1
        components.append(f'{element.name}[{index}]')
        element = element.find_parent()
    components.reverse()
    return '/' + '/'.join(components)
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
            end_time = start_time + 5
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
            for index, post in enumerate(posts):
                    post_content = post.find("div", class_="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a")
                    if post_content:
                        # Find the "Leave a comment" button within the post if that post have one or more comments then click on the comment button
                        comment_count_element = post.find("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa")
                        if comment_count_element:
                            comment_button = post.find("div", attrs={"aria-label": "Leave a comment"})
                            comment_button_xpath = get_full_xpath(comment_button)
                            self.driver.find_element(By.XPATH, comment_button_xpath).click()
                            #wait the comment section popup
                            time.sleep(3)
                            #refetch
                            soup = BeautifulSoup(self.driver.page_source, "html.parser")
                            #find all the comment
                            comments = soup.find_all("div", class_="x1y1aw1k xn6708d xwib8y2 x1ye3gou")
                            #locate the post after pop up
                            posts_popup = soup.find_all("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h")
                            post_popup = posts_popup[len(posts_popup)-1]
                            #find see more button
                            seemore_button = post_popup.find("div", class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1sur9pj xkrqix3 xzsf02u x1s688f", role="button")
                            #if that post have see more button then click 
                            if seemore_button:
                                seemore_button_xpath = get_full_xpath(seemore_button)
                                selenium_seemore_button = self.driver.find_element(By.XPATH, seemore_button_xpath)
                                selenium_seemore_button.click()
                                #wait the caption loaded
                                time.sleep(1)
                                #refetch the pop up post
                                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                                posts_popup = soup.find_all("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h")
                                post_popup = posts_popup[len(posts_popup)-1]
                            else:
                                print("không có button")
                            # extract all the content of the post
                            first_paragraph =  post_popup.find("div", class_="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a") #this is the first
                            content_post = first_paragraph.text.strip()
                            sub_list = post_popup.find_all("div", class_="html-a xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs")
                            if sub_list:
                                for list in sub_list:
                                    content_post += ' \n' + list.text.strip()
                            else:
                                print("this post dont have sub list")
                            sub_paragraph = post_popup.find_all("div", class_="x11i5rnm xat24cr x1mh8g0r x1vvkbs xtlvy1s x126k92a")
                            if sub_paragraph:
                                for paragraph in sub_paragraph:
                                    content_post += ' \n' + paragraph.text.strip() 
                            else:
                                print("this post dont have sub paragrpahs")
                            if content_post not in results:
                                results[content_post] = []
                            for comment in comments:
                                results[content_post].append(comment.text.strip())
                            close_comment_buton = self.driver.find_element(By.XPATH, f"//div[@aria-label='Close' and @role='button']")
                            close_comment_buton.click()
                            # Wait for the comment section to close
                            time.sleep(3)
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
