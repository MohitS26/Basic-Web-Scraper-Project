# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 14:38:56 2022

@author: mohit & vartika
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd


def PL_DATA(id):
    my_url = f'https://www.premierleague.com/match/{id}'
    option = Options()
    option.headless = False
    driver = webdriver.Chrome(r"chromedriver.exe")
    driver.get(my_url)
    driver.maximize_window()
    sleep(5)
    #Tried to implement a work around the accept cookies page but it does not work sometimes due to lag
    #driver.implicitly_wait(10)
    #driver.find_elements_by_class_name('_2hTJ5th4dIYlveipSEMYHH BfdVlAo_cgSVjDUegen0F js-accept-all-close').click()

    elem = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='tablist']//li[@data-tab-index='2']")))
    elem.click()
    sleep(5)
    home_team = driver.find_element_by_xpath('//*[@id="mainContent"]/div/section/div[2]/section/div[3]/div/div/div[1]/div[1]/a[2]/span[1]').text
    away_team = driver.find_element_by_xpath('//*[@id="mainContent"]/div/section/div[2]/section/div[3]/div/div/div[1]/div[3]/a[2]/span[1]').text

    scores = driver.find_element_by_xpath('//*[@id="mainContent"]/div/section/div[2]/section/div[3]/div/div/div[1]/div[2]/div/div').text
    home_score = scores.split('-')[0]
    away_score = scores.split('-')[1]
    list = {home_team:home_score,away_team:away_score}
    
    

    dfs = pd.read_html(driver.page_source)
    stats = dfs[-1]
    return stats,list;
    
    
    
def match_id():
    #Reading File
    df = pd.read_csv("PL_Match_Ids.csv")

    #Entering the teams
    print("Enter Home Team")
    HT = str(input())
    print("Enter Away Team")
    AT = str(input())

    #Getting the MATCH ID
    ID_loc = df.loc[(df["Home_Team"]==HT) & (df["Away_Team"]==AT)]
    ids = ID_loc.iloc[0]['Match_id']
    return ids
    



if __name__ == "__main__":
    
    id = match_id()
    show_stats, score = PL_DATA(id)
    x = show_stats.keys()
    a= score.get(x[0])+" : "+score.get(x[2])
    final = show_stats.rename(columns = {"Unnamed: 1" : a})
    final.to_csv("Premier_League19-20.csv")
    print(final)
    

       
 