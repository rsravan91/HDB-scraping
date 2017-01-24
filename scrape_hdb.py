# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
import time # time delay
import re #regular expression subselection of address

driver=webdriver.Chrome("/Users/ephsr/Downloads/chromedriver")
driver.get("https://services2.hdb.gov.sg/web/fi10/emap.html#")

# wait for 10seconds, for webpage to load for the first time
time.sleep(30)


# once the page loads close the popup window
close_popup=driver.find_element_by_xpath("/html/body/div[2]/div/a[2]")
close_popup.click()

# enter pincode in the searchbox
search_box=driver.find_element_by_id("searchTxt")
search_box.send_keys("120420")
driver.find_element_by_id("searchButton").click()
# now click on housing button
driver.find_element_by_id("menuHouse").click()

# now wait for 30 seconds for map to load
time.sleep(30)

# once map loads find number of housings populated in the map
parent_node=driver.find_element_by_xpath('//*[@id="Flats_layer"]')
children_nodes = parent_node.find_elements_by_xpath(".//*")

# for each populated housing, find flat related data by clicking it
for i in children_nodes:
    extract_housing_data(i)

    
def extract_housing_data(child):
    child.click()
    address=driver.find_element_by_xpath('//*[@id="addr"]').text
    #extract pincode from the address
    pincode=re.search('S\(([0-9]+)\)',address).group(1)
    lease_start_date=driver.find_element_by_xpath('//*[@id="sRLI"]/div[1]').text
    lease_start_date=re.search(': (.*)',lease_start_date).group(1)
    lease_duration=driver.find_element_by_xpath('//*[@id="sRLI"]/div[2]').text
    lease_duration=re.search(': (.*)',lease_duration).group(1)
    remaining_lease=driver.find_element_by_xpath('//*[@id="sRLI"]/div[3]').text
    remaining_lease=re.search(': (.*) \(',remaining_lease).group(1)
    
    

    
    