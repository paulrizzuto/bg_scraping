from bs4 import BeautifulSoup
from splinter import Browser
import datetime as dt
import numpy as np
import pandas as pd
import pymongo
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import os

executable_path = {'executable_path':'chromedriver'}

browser = Browser('chrome', **executable_path) 

counter = 15

months = ["January", "February", "March", "April", 
          "May", "June", "July", "August", "September", 
          "October", "November", "December"]
years = ["2012", "2013", "2014", "2015", "2016", "2017"]

locations = []

csvpath = os.path.join('msa3.csv')

with open(csvpath, newline= "", encoding='utf-8-sig') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\n')
    for row in csvreader:
        locations.append(row[0])

#start loop
for location in locations:
    url = "https://laborinsight.burning-glass.com/jobs/us#/reports/create"
    browser.visit(url)
    time.sleep(2)
    browser.fill('loginEmail', 'ahaque@trilogyed.com')
    time.sleep(2)
    browser.find_by_id('Password').fill('ahaque')
    time.sleep(2)
    browser.find_by_id('submit').click()
    time.sleep(3)
    browser.find_by_id('create').click()
    print("Checking... " + str(location))
    cols = pd.read_csv("frameColumns.csv")
    csv_loc = []
    csv_topic =[]
    jobs_data = []
    time.sleep(5)
    #entry level spec
        #time.sleep(3)
        #browser.find_by_text('any')[6].click()
        #time.sleep(3)
        #browser.find_by_text('0 to 2 years').click()
    #select skill clusters
    time.sleep(2)
    browser.find_by_id('accordionSkill').click()
    time.sleep(1)
    browser.find_by_id('JTAndSkillCluster').fill('Information Technology: Application Programming Interface (API)\n')
    time.sleep(1)
    browser.find_by_id('JTAndSkillCluster').fill('Information Technology: JavaScript and jQuery\n')
    time.sleep(1)
    browser.find_by_id('JTAndSkillCluster').fill('Information Technology: Web Development\n')
    time.sleep(1)
    browser.find_by_id('JTAndSkillCluster').fill('Information Technology: Web Servers\n')
    time.sleep(1)
    browser.find_by_id('JTAndSkillCluster').fill('Information Technology: Java\n')
    time.sleep(1)
    browser.find_by_id('JTAndSkillCluster').fill('Information Technology: Software Development Principles\n')
    time.sleep(1)
    browser.find_by_id('JTAndSkillCluster').fill('Information Technology: Software Development Tools\n')
    time.sleep(1)
    browser.find_by_id('JTAndSkillCluster').fill('Information Technology: Software Quality Assurance\n')
    #select report category
    time.sleep(2)
    browser.find_by_id('dk_container_selectReportCategories').click()
    time.sleep(1)
    dropdown = browser.find_by_id('dk_container_selectReportCategories')
    for option in dropdown.find_by_tag('li'):
        if option.text == "Job Counts by Year":
            option.click()
            break
    #select location
    time.sleep(2)
    browser.find_by_id('accordionLocation').click()
    time.sleep(1)
    browser.find_by_id('LocationMSA').fill(location)
    time.sleep(1)
    active_web_element = browser.driver.switch_to_active_element()  
    active_web_element.send_keys(Keys.DOWN)
    active_web_element.send_keys(Keys.ENTER)
    time.sleep(2)
    browser.find_by_id('timePeriodAccordionOrg').click()
    #select timeframe
    for year in years:
        for month in months:
            try:
                time.sleep(2)
                browser.find_by_id('dk_container_selectForMonth').click()
                time.sleep(1)
                dropdown = browser.find_by_id('dk_container_selectForMonth')
                for option in dropdown.find_by_tag('li'):
                    if option.text == month:
                        option.click()
                        break
                time.sleep(2)
                browser.find_by_id('dk_container_selectForYear').click()
                time.sleep(1)
                dropdown = browser.find_by_id('dk_container_selectForYear')
                for option in dropdown.find_by_tag('li'):
                    if option.text == year:
                        option.click()
                        break
                #get jobs data
                time.sleep(4)
                item = browser.find_by_tag('span')[2].text
                jobs_data.append(item.split(" ")[0].split("(")[1])
                csv_topic.append("Web Development")
                csv_loc.append(location)
            except:
                jobs_data.append('0')
                csv_topic.append("Web Development")
                csv_loc.append(location)
        #print(jobs_data)    
        print("Done checking " + year)   
    print("Done checking " + location)
    browser.find_by_id('reportClearBtn').click()
    time.sleep(2)
    jobs_data = jobs_data[:-2]
    csv_topic = csv_topic[:-2]
    csv_loc = csv_loc[:-2]
    cols["Jobs"] = jobs_data
    cols["Topic"] = csv_topic
    cols["MSA"] = csv_loc
    counter += 1
    cols.to_csv("JobsData" + str(counter) + ".csv")
    browser.reload()