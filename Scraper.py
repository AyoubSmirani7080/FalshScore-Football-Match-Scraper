# importing various libraries that are needed for the script to run:
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


# This code is trying to create a new instance of the Chrome webdriver using the `webdriver.Chrome()`
# function. It assumes that you have Chrome installed and have also installed the appropriate
# chromedriver for your version of Chrome.
try:
    page = webdriver.Chrome()  
except ConnectionRefusedError :
     print(ConnectionRefusedError)       



# The code is trying to access the website "https://www.flashscore.com/" using the `get()` method of
# the `page` object. If there is a `ConnectionError` exception raised during this process, it will print the error message `ConnectionRefusedError`.
try:
     page.get('https://www.flashscore.com/')
except ConnectionError:
     print(ConnectionRefusedError) 
 

# The function `getDateNow` returns the current date from a web page element with the ID 'calendarMenu'.
# return: the first 5 characters of the text found in the element with the ID 'calendarMenu'.
def getDateNow():

    return page.find_element(By.ID,'calendarMenu').text[:5]


# The line `date = input('donne une date sous forme jj/mm :')` is prompting the user to enter a date
# in the format "jj/mm". The entered date will be stored in the variable `date`.
date = input('donne une date sous forme jj/mm :')


# Conversion des chaînes en objets datetime
date_format = "%d/%m"
date1 = datetime.strptime(date, date_format)
date2 = datetime.strptime(getDateNow(), date_format)






# The function "change_Date" waits for a specific element to be clickable, clicks on it, and then
# waits for a certain amount of time before updating the date.
# param ClassName: The ClassName parameter is the name of the class of the element that you want to
# click on. This is used to locate the element on the page
# param date1: The starting date that you want to change
# param date2: The `date2` parameter is the target date that you want to change to. It is a string
# representation of a date in a specific format
def change_Date(ClassName,date1,date2):

    while date1 != date2 :
          wait = WebDriverWait(page, 10)
          element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,ClassName )))
          element.click()
          time.sleep(5)
          date2 = datetime.strptime(getDateNow(), date_format) 


# This code block is comparing two dates, `date1` and `date2`, and performing different actions based
# on the comparison result.
if date1 < date2:
    print(f"{date} est antérieure à {getDateNow()}")       
    change_Date('calendar__navigation--yesterday',date1,date2)      
    print(getDateNow())
elif date1 > date2:
    print(f"{date} est postérieure à {getDateNow()}")
    change_Date('calendar__navigation--tomorrow',date1,date2)   
    print(getDateNow())
else:
    print(f"{date} est égale à {getDateNow()}")



# The function `Save_teams_logo` downloads and saves the logos of home and away teams in separate directories.
# param home_team_logo: A list of URLs representing the logos of the home teams
# param away_team_logo: A list of URLs that representing the logos of the away teams
def Save_teams_logo(home_team_logo, away_team_logo):

    home_path = f'home_team_logo {getDateNow()}'
    away_path = f'away_team_logo {getDateNow()}'
    os.makedirs(home_path)
    os.makedirs(away_path)
      
    for i in home_team_logo:
        try:
            img_response = requests.get(i.get_attribute('src'))
            if img_response.status_code == 200:
                with open(f"{home_path}/{i.get_attribute('src').split('/')[-1]}", 'wb') as f:
                        f.write(img_response.content)
            print(f"Downloaded: {i}") 
        except :
            print('error downloading')    

    for i in away_team_logo:
        try:    
            img_response = requests.get(i.get_attribute('src'))
            if img_response.status_code == 200:
                with open(f"{away_path}/{i.get_attribute('src').split('/')[-1]}", 'wb') as f:
                        f.write(img_response.content)
            print(f"Downloaded: {i}") 
        except :
            print('error downloading')   
                     




# The function `get_football_matchs_data` retrieves data about football matches, including the home team, away team, time, home team logo, away team logo, home team score, and away team score.
# return: a dictionary with the following keys and values:
# - 'home team': a list of home team names
# - 'away team': a list of away team names
# - 'time': a list of match times
# - 'home team logo': a list of filenames for the home team logos
# - 'away team logo': a list of filenames for the away team logos
# - 'score_home'
# - 'score_away'
def get_football_matchs_data():

    home_team_selector = page.find_elements(By.CLASS_NAME , 'event__participant--home')
    away_team_selector = page.find_elements(By.CLASS_NAME , 'event__participant--away')
    time_selector = page.find_elements(By.CLASS_NAME , 'event__time') 
    score_home_selector = page.find_elements(By.CLASS_NAME , 'event__score--home')
    score_away_selector = page.find_elements(By.CLASS_NAME , 'event__score--away')
    event__logo_home = page.find_elements(By.CLASS_NAME , 'event__logo--home')
    event__logo_away = page.find_elements(By.CLASS_NAME , 'event__logo--away')

    time = []
    home_team = []
    away_team = [] 
    score_home = [] 
    score_away = [] 
    home_team_logo = []
    away_team_logo = []

    for i in range(len(home_team_selector)):
        home_team.append(home_team_selector[i].text)
        away_team.append(away_team_selector[i].text)
        time.append(time_selector[i].text if i < len(time_selector) else ' ')
     # The code is appending the text of the `score_home_selector` and `score_away_selector` elements
     # to the `score_home` and `score_away` lists, respectively.
        score_home.append(score_home_selector[i].text if i < len(score_home_selector) else ' ')
        score_away.append(score_away_selector[i].text if i < len(score_away_selector) else ' ')

    for home,away in zip(event__logo_home,event__logo_away):
        home_team_logo.append(home.get_attribute('src').split('/')[-1] if home is not None and home.get_attribute('src') else ' ') 
        away_team_logo.append(away.get_attribute('src').split('/')[-1] if away is not None and away.get_attribute('src') else ' ')     

   
    


    #Save_teams_logo(event__logo_home, event__logo_away)
    return {'home team':home_team,'away team':away_team ,'time': time,'home team logo' : home_team_logo,\
            'away team logo' : away_team_logo , 'home team score': score_home ,  'away team score': score_away }





# The code is calling the function `get_football_matchs_data()` to retrieve data about football
# matches. The returned data is then used to create a pandas DataFrame called `data`. The DataFrame is
# then saved as a CSV file with a filename that includes the current date. Finally, the `page.quit()`
# method is called to close the webdriver.
football_match = get_football_matchs_data()
data = pd.DataFrame(football_match, columns=football_match.keys())
data.to_csv(f'football match {getDateNow()[3:]}.csv',index=False)
page.quit()



