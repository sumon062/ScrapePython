# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 16:00:10 2019

@author: Towfik
"""
# Here, I am importing Beautiful Soup,csv and the Requests library
import requests as r
from bs4 import BeautifulSoup
import csv
# this is the url that we've already determined to scrape from.
urltoget = 'http://drd.ba.ttu.edu/2019c/isqs6339/hw1'
#this is the filepath to copy 
filepath = 'C:\\users\\Sumon\\Desktop\\dataout.csv'
# here,I fetch the content from the url, using the requests library
res = r.get(urltoget)
#Check if we have a good request
if res.status_code == 200:
    print('request is good')
else:
    print('bad request, received code ' + str(res.status_code))
    
#Soup Object 
soup = BeautifulSoup(res.content,'lxml')
#Let's find the table.  Note, there is only 1 table so this works well.
results = soup.find("table")
#print (results)

#Now, let's find all rows within the table
rowresults = results.find_all("tr")
#print (rowresults)
#Opening the csv file to write and providing the column names
with open(filepath, 'w') as dataout:
    datawriter = csv.writer(dataout, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    datawriter.writerow(['id','quality', 'name', 'hp','level','elite','damage','money_drop','drop_mask'])
#Now, let's iterate on all the rows within the table.   
    for row in rowresults:
    #Locate the cells in the row
        cells = row.find_all("td")
    #This checks to see if we have a header row.  Notice the first row of the
    #table is using <th> instead of <td> tags.  
        if len(cells) != 0:
            #Access the data.  Note, the cells[#] syntax.
            #print these on console
            #print('\n*************MOBS INFO************\n')
            #print("Quality:  " + cells[1].text)
            #print(cells[0].find('a')['href'])
            find_id = cells[0].find('a')['href']
            id=find_id[15:]
            #checking the extended link, put it in an object 
            link= ('/' + cells[0].find('a')['href'])
            # creating the link by concetanating with the extended link
            new_link= urltoget+link
            # here,I fetch the content from the updated url, using the requests library
            mobs = r.get(new_link)
            #soup Object from the updated url
            mobssoup = BeautifulSoup(mobs.content,'lxml')
            #finding the mobcard id
            mobs_all = mobssoup.find_all('div', attrs={'id' : 'mobcard'})
            #print (mobs_all)
            #print('\mobcard INFORMATION\n  ')
            #Iterate on all the values within the table where id is not blank(as here we have a blank id) and writing into the csv file
            for item in mobs_all:
                if id!='':
                    mobstats = item.findAll('span', attrs={'class' : 'val'})
                    #print on console
                    #print('name:  ' + mobstats[0].text)
                    #print('hp:  ' + mobstats[3].text)
                    #print('level:  ' + mobstats[2].text)
                    #print('elite:  ' + mobstats[1].text)
                    #print('manage:  ' + mobstats[6].text)
                    #print('money_frop:  ' + mobstats[5].text)
                    #print('drop_mask:  ' + mobstats[4].text)
                    #print('------------------------------')
                    datawriter.writerow([id,cells[1].text,mobstats[0].text,mobstats[3].text,mobstats[2].text,
                                    '0'if mobstats[1].text=='Normal' else '1',mobstats[6].text,mobstats[5].text,
                                    mobstats[4].text.strip()])
        
            
        
           