from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pwinput

email=input('Username: ')
password=pwinput.pwinput(mask='💐')
profile_name='dimitra._.vrou'

# Setup
options=webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver=webdriver.Chrome(options=options)
driver.maximize_window()
driver.get('https://www.instagram.com/accounts/login/?next=%2F'+profile_name+'%2F&source=omni_redirect')

# Accepts cookies
while True:
    try: 
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[text()="Allow all cookies"]').click() # Finding any element with the text: Allow all cookies
        break
    except NoSuchElementException:
        pass

while True:
    try:
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@value and @name="username"]').send_keys(email) # Finding any element with the attribute value name="username"
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@value and @name="password"]').send_keys(password) # Finding any element with the attribute value name="password"
        break
    except NoSuchElementException:
        pass

# Clicks enter
time.sleep(1)
actions=ActionChains(driver)
actions.send_keys(Keys.ENTER).perform()

# Clicks Not Now
while True:
    try:
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[text()="Not now"]').click() # Finds any element with the text not now
        break
    except NoSuchElementException:
        pass

# Gets follower count and goes on the follower page
while True:
    try:
        time.sleep(1)
        temp_followers_count=driver.find_element(By.XPATH,'//*[@href="/'+profile_name+'/followers/"]').text # Finds any element with the attribute href="/profile_name/followers/"
        temp_following_count=driver.find_element(By.XPATH,'//*[@href="/'+profile_name+'/following/"]').text
        break
    except NoSuchElementException:
        pass

# EG: temp_follower_count="1256 Followers", this gets only 1256
followers_count=''
for character in temp_followers_count:
    if character in ['0','1','2','3','4','5','6','7','8','9']:
        followers_count+=str(character)

following_count=''
for character in temp_following_count:
    if character in ['0','1','2','3','4','5','6','7','8','9']:
        following_count+=str(character)

# Gathers followers and following
followers_following=[['just._.peeping__'],[]]
for i in range(2): 
    if i==0:
        page='followers'
        count=followers_count
    else:
        page='following'
        count=following_count

    while True: # Restarting till instagram shows all the hidden followers/following
        time.sleep(1)
        driver.get('https://www.instagram.com/'+profile_name+'/'+page+'/') # Opens followers/following
        time.sleep(6)

        try:
            list=driver.find_element(By.CLASS_NAME,'_aano') # Gets the element with the followers/following list and scrollbar (without the search bar up top)
            # The scrollbar reveals 12 followers/following per full scroll, so it moves the scrollbar ceil(follower/following_count/12) times
            for j in range(int(int(count)/12)+1):
                driver.execute_script('arguments[0].scrollTop=arguments[0].scrollTop+arguments[0].offsetHeight*100;',list)
                time.sleep(3)
        except (NoSuchElementException, StaleElementReferenceException):
            pass

        # Gets all the followers/following since it's done scrolling
        while True:
            try:
                temp_followers_following=driver.find_element(By.CLASS_NAME,'_aano').text
                break
            except NoSuchElementException:
                pass

        # The temp_followers_following has a format like ['username1\nname1\nfollow\nusername2\nname2\nfollow'], all this makes an array with every username having it's own cell
        temp_followers_following=temp_followers_following.split('\n') # With the previous format in mind this gives the previous word a cell every time a \n comes up

        for j in range(len(temp_followers_following)):
            if temp_followers_following[j]=="Follow":
                if temp_followers_following[j-2]!="Follow": # Because some people dont have a name (only username) sometimes it has to go back 1 cell to get the username not 2
                    if temp_followers_following[j-2] not in followers_following[i]: # If it's a new username
                        followers_following[i].append(temp_followers_following[j-2])
                else:
                    if temp_followers_following[j-1] not in followers_following[i]:
                        followers_following[i].append(temp_followers_following[j-1])

        print(len(followers_following[i]))
        if len(followers_following[i])==int(count): # Stops when it finds them all
            break

driver.quit()


unfollowed=[]
# Finds those who are in the following list but not in the follower's one
for i in range(len(followers_following[1])):
    if followers_following[1][i] not in followers_following[0]:
        unfollowed.append(followers_following[1][i])

print('Snake List:',*unfollowed,sep=' | ',end='')
print(' |')
