from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pwinput

# Credentials
email = input('Username: ')
password = pwinput.pwinput(mask='💐')
profile_name = "dimitra._.vrou"
my_profile_name = "just._.peeping__"


# Setup
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver=webdriver.Chrome(options = options)
driver.maximize_window()
driver.get('https://www.instagram.com/accounts/login/?next=%2F'+ profile_name +'%2F&source=omni_redirect')


# Accepts cookies
while True:
    try: 
        # Finds any element with the text: Allow all cookies
        driver.find_element(By.XPATH, '//*[text()="Allow all cookies"]').click()
        break

    except NoSuchElementException:
        pass


# Insert credentials
while True:
    try:
        # Finds any element with the attribute value name = "email" or "pass"
        driver.find_element(By.XPATH, '//*[@value and @name="email"]').send_keys(email)
        driver.find_element(By.XPATH, '//*[@value and @name="pass"]').send_keys(password)
        break

    except NoSuchElementException:
        pass


# Clicks enter
actions=ActionChains(driver)
actions.send_keys(Keys.ENTER).perform()


# Clicks Not Now
while True:
    try:
        # Finds any element with the text: Not now
        driver.find_element(By.XPATH, '//*[text()="Not now"]').click()
        break

    except NoSuchElementException:
        pass


# Gets follower count button
while True:
    try:
        # Finds any element with the attribute href = "/profile_name/followers/" or "/profile_name/following/"
        followers_count_button = driver.find_element(By.XPATH, '//*[@href="/' + profile_name + '/followers/"]')
        following_count_button = driver.find_element(By.XPATH, '//*[@href="/' + profile_name + '/following/"]')
        break

    except NoSuchElementException:
        pass


# EG: temp_follower_count="1256 Followers", this gets only 1256
followers_count=''
for character in followers_count_button.text:
    if character in ['0','1','2','3','4','5','6','7','8','9']:
        followers_count += str(character)

following_count=''
for character in following_count_button.text:
    if character in ['0','1','2','3','4','5','6','7','8','9']:
        following_count += str(character)


# Gathers followers and following
followers_following = [[my_profile_name], []]
for i in range(2): 
    if i == 0:
        page = followers_count_button
        count = followers_count

    else:
        page = following_count_button
        count = following_count


    # Restarting till instagram shows all the hidden followers/following
    while True:
        # Opens followers/following
        page.click()

        # Gets the element with the followers/following list and scrollbar (without the search bar up top)
        while True:
            try:
                # Finds any element where the class name equals that long string
                scroll_list = driver.find_element(By.XPATH, "//*[@class='x6nl9eh x1a5l9x9 x7vuprf x1mg3h75 x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']")
                break
            
            except (NoSuchElementException, StaleElementReferenceException):
                pass

        # The scrollbar reveals 12 followers/following per full scroll, so it moves the scrollbar 
        # ceil(follower_count or following_count / 12) times
        for j in range(int(int(count) / 12) + 1):
            time.sleep(1)
            driver.execute_script('arguments[0].scrollTop=arguments[0].scrollTop+arguments[0].offsetHeight*100;',scroll_list)

        # Gets all the followers/following after it's done scrolling
        while True:
            try:
                # Finds any element where the class name equals that long string
                temp_followers_following = driver.find_element(By.XPATH, "//*[@class='x6nl9eh x1a5l9x9 x7vuprf x1mg3h75 x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']").text
                break

            except NoSuchElementException:
                pass

        # Because the temp_followers_following has a format like ['username1\nname1\nfollow\nusername2\nname2\nfollow'], make an array with 
        # every username having it's own cell
        temp_followers_following = temp_followers_following.split('\n') # Gives the previous word a cell every time a \n comes up
        for j in range(len(temp_followers_following)):
            if temp_followers_following[j] == "Follow":
                if temp_followers_following[j - 2] != "Follow": # It has to go back 1 cell to get the username, if someone doesn't have a name (only a username)
                    if temp_followers_following[j - 2] not in followers_following[i]: # If it's a new username
                        followers_following[i].append(temp_followers_following[j - 2])
                
                else:
                    if temp_followers_following[j - 1] not in followers_following[i]:
                        followers_following[i].append(temp_followers_following[j - 1])

        
        print(str(len(followers_following[i])) + "/" + count + "\n")

        # Clicks the X button in order to reopen the followers/following page
        while True:
            try:
                # Finds any element with the attribute aria-label = "Close"
                driver.find_element(By.XPATH, '//*[@aria-label="Close"]').click()
                break

            except NoSuchElementException:
                pass

        # Stops when it finds them all
        if len(followers_following[i]) == int(count):
            break

driver.quit()


# Finds those who are in the following list but not in the follower's one and prints them
unfollowed = []
for i in range(len(followers_following[1])):
    if followers_following[1][i] not in followers_following[0]:
        unfollowed.append(followers_following[1][i])

print('Snake List:', *unfollowed, sep=' | ', end='')
print(' |')
