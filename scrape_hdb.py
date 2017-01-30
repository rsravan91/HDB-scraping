# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
import time # time delay
import re #regular expression subselection of address
#import exceptions
from selenium.common.exceptions import NoSuchElementException
import numpy as np # to calculate distances between points
import pandas as pd
import math

# gloabal array to keep track of visited nodes
visited_nodes=[]


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
children_nodes = parent_node.find_elements_by_tag_name("image")



df=pd.DataFrame()

def extract_housing_data(child):
    address=driver.find_element_by_xpath('//*[@id="addr"]').text
    
    # extract pincode from the address
    pincode=re.search('S\(([0-9]+)\)',address).group(1)
    
    try:
        lease_start_date=driver.find_element_by_xpath('//*[@id="sRLI"]/div[1]').text
        lease_start_date=re.search(': (.*)',lease_start_date).group(1)
    except NoSuchElementException:
        lease_start_date='NA'
        
    try:
        lease_duration=driver.find_element_by_xpath('//*[@id="sRLI"]/div[2]').text
        lease_duration=re.search(': (.*)',lease_duration).group(1)
    
    except NoSuchElementException:
        lease_duration='NA'
    
    try:
        remaining_lease=driver.find_element_by_xpath('//*[@id="sRLI"]/div[3]').text
        remaining_lease=re.search(': (.*) \(',remaining_lease).group(1)
    except NoSuchElementException:
        remaining_lease='NA'
    
        
    # extract flat types
    
    table = driver.find_element_by_xpath('//*[@id="sBFT"]/div/div/table')
    rows= table.find_elements_by_xpath('.//tbody')
    # create a temp variable to store flat and units for each row
    flats_units=[]
    for row in rows:
        flat=row.find_element_by_xpath('.//tr/td[1]').text
        units=row.find_element_by_xpath('.//tr/td[2]').text
        flats_units.append([flat,units])

    
    # append above vaiables as columns into dataframe
    df=df.append({"address":address,"lease_start_date":lease_start_date,"lease_duration":lease_duration,"remaining_lease":remaining_lease,"flats_units":flats_units},ignore_index=True)
    


def get_coordinates_from_node(node):
    coord=[int(node.get_attribute('x')),int(node.get_attribute('y'))]
    return coord
          
def get_node_from_coordinate(coordinate):
    
              
          
def mark_node_as_visited(node):
    coord=get_coordinates_of_node(node)
    visited_nodes.append(coord)
    

def get_coordinates_of_all_nodes():
    nodes=driver.find_element_by_xpath('//*[@id="Flats_layer"]').find_elements_by_tag_name("image") 
    all_nodes=[]
    for node in nodes:
        coord=get_coordinates_from_node(node)
        all_nodes.append(coord)
    return all_nodes

    
def find_non_visited_node():
    all_nodes=get_coordinates_of_all_nodes()
    # get list of non visited nodes
    non_visited_nodes=list(set(all_nodes)-set(visited_nodes))
    # now find a non visited node which is nearest to just visited node--> to be tested later(dfs)
    # get first element of non visited nodes and visit that (random walk)
    return non_visited_nodes[1]




flag=True
#def visit_unvisited_node():
while(flag)
    get_coordinated_of_all_nodes()
    non_visited_node=find_non_visited_node()
    # check for emptyness of non_visited_nodes before returning
    if not non_visited_node: 
        flag=False
    else:
        
    

    
    
# randomly click on one building to start the program 
# randomly start scraping from one point and and as map gets updated
# keep scraping till you have seen all pincodes

# create a list of visited nodes, each node is represented by its x,y coordinates

# for each populated housing, find flat related data by clicking it
for i in children_nodes:
    child.click()
    mark_node_as_visited(i)
    extract_housing_data()
    # once the build info is clicked the map is refreshed, collect new coordinates
    parent_node=driver.find_element_by_xpath('//*[@id="Flats_layer"]')
    children_nodes = parent_node.find_elements_by_tag_name("image")
    
