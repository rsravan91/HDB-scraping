# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
import time # time delay
import re #regular expression subselection of address
#import exceptions
from selenium.common.exceptions import NoSuchElementException,WebDriverException
import numpy as np # to calculate distances between points
import pandas as pd
import math


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
time.sleep(10) # wait for 10 seconds for the location to searched
# now click on housing button
driver.find_element_by_id("menuHouse").click()

# now wait for 30 seconds for map to load
time.sleep(30)

        
    


def extract_housing_data():
    df=pd.DataFrame()
    
    address=driver.find_element_by_xpath('//*[@id="addr"]').get_attribute("textContent")
    
    # extract pincode from the address
    pincode=str(re.search('S\(([0-9]+)\)',address).group(1))
    
    try:
        #lease_start_date=driver.find_element_by_xpath('//*[@id="sRLI"]/div[1]').text
        # The above doesnt work on hidden elemts
        lease_start_date=driver.find_element_by_xpath('//*[@id="sRLI"]/div[1]').get_attribute("textContent")
        lease_start_date=re.search(': (.*)',lease_start_date).group(1)
    except NoSuchElementException:
        lease_start_date='NA'
        
    try:
        lease_duration=driver.find_element_by_xpath('//*[@id="sRLI"]/div[2]').get_attribute("textContent")
        lease_duration=re.search(': (.*)',lease_duration).group(1)
    
    except NoSuchElementException:
        lease_duration='NA'
    
    try:
        remaining_lease=driver.find_element_by_xpath('//*[@id="sRLI"]/div[3]').get_attribute("textContent")
        remaining_lease=re.search(': (.*) \(',remaining_lease).group(1)
    except NoSuchElementException:
        remaining_lease='NA'
    
        
    # extract flat types
    # click flat type dropdown
    driver.find_element_by_xpath('//*[@id="sBFTh"]').click()
    time.sleep(4)
    try:
        table = driver.find_element_by_xpath('//*[@id="sBFT"]/div/div/table')
        rows= table.find_elements_by_xpath('.//tbody')
        # create a temp variable to store flat and units for each row
        flats_units=[]
        for row in rows:
            flat=row.find_element_by_xpath('.//tr/td[1]').get_attribute("textContent")
            units=row.find_element_by_xpath('.//tr/td[2]').get_attribute("textContent")
            flats_units.append([flat,units])
    except NoSuchElementException:
        flats_units='No Records Found'

    
    # append above vaiables as columns into dataframe
    df=df.append({"address":address,"pincode":pincode,"lease_start_date":lease_start_date,"lease_duration":lease_duration,"remaining_lease":remaining_lease,"flats_units":flats_units},ignore_index=True)
    return df


def get_coordinates_from_node(node):
    coord=(int(node.get_attribute('x')),int(node.get_attribute('y')))
    return coord
          
def get_node_from_coordinate(coordinate):
    nodes=driver.find_element_by_xpath('//*[@id="Flats_layer"]')
    xpath='//*[@x="'+str(coordinate[0])+'" and @y="'+str(coordinate[1])+'"]'
    node=nodes.find_element_by_xpath(xpath)
    return node
    
              
          
def mark_node_as_visited(node,visited_nodes):
    coord=get_coordinates_from_node(node)
    visited_nodes.append(coord)
    return visited_nodes
    

def get_coordinates_of_all_nodes():
    nodes=driver.find_element_by_xpath('//*[@id="Flats_layer"]').find_elements_by_tag_name("image") 
    all_nodes=[]
    for node in nodes:
        coord=get_coordinates_from_node(node)
        all_nodes.append(coord)
    return all_nodes

    
def find_non_visited_nodes(all_nodes,visited_nodes):
    # get list of non visited nodes
    if not visited_nodes: # if visited nodes is empty array then return all nodes (all unvisited)
        return all_nodes
    else:
        non_visited_nodes=list(set(all_nodes)-set(visited_nodes))
        # now find a non visited node which is nearest to just visited node--> to be tested later(dfs)
        return non_visited_nodes


        
# gloabal array to keep track of visited nodes
visited_nodes=[]
   
    
# randomly click on one building to start the program 
# randomly start scraping from one point and and as map gets updated
# keep scraping till you have seen all pincodes

# create a list of visited nodes, each node is represented by its x,y coordinates

# for each populated housing, find flat related data by clicking it

housing_data=pd.DataFrame()


flag=True
#def visit_unvisited_node():
while(flag):
    all_nodes=get_coordinates_of_all_nodes()
    non_visited_nodes=find_non_visited_nodes(all_nodes,visited_nodes)
    # check for emptyness of non_visited_nodes before returning
    if not non_visited_nodes: 
        flag=False
    else:
        loop=True
        i=0
        while loop:
            try:
                node=get_node_from_coordinate(non_visited_nodes[i])
                node.click()
                time.sleep(5) # wait for 5 seconds for the card to appear
                df=extract_housing_data()
                housing_data=pd.concat([housing_data,df])
                visited_nodes=mark_node_as_visited(node,visited_nodes)
                loop=False # break the loop
            except WebDriverException:
                # when building is hidden under the info card popup,
                # choose other building
                i=i+1
            except IndexError:
                loop=False
                
