from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
from datetime import datetime
import time
import os
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException      

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

options = Options()
options.add_argument('disable-infobars')
options.add_argument('--incognito')
options.add_argument("start-maximized")
service = Service('insert path to your own chromedriver download')




def get_server_links():
    driver = webdriver.Chrome(service=service)
    URL = 'https://www.g2g.com/categories/lost-ark-gold'

    # initialize empty list to store links to visit to get data
    links = []
    #----------------------------------------------------------------------
    driver.get(URL)
    time.sleep(5) #wait for page to load
    html = driver.page_source
    soup = bs(html, features="html.parser")

    #get the links to gold selers for all servers on the page
    boxes = soup.find_all('div', class_='col-12 col-md-3')
    for box in boxes:
        #print(box.find('a', href=True)['href'])
        links.append(box.find('a', href=True)['href'])
    
    URL = URL + '?page=2'
    driver.get(URL)
    time.sleep(5) #wait for page to load
    html = driver.page_source
    soup = bs(html, features="html.parser")

    #get the links to gold selers for all servers on the page
    boxes = soup.find_all('div', class_='col-12 col-md-3')
    for box in boxes:
        #print(box.find('a', href=True)['href'])
        links.append(box.find('a', href=True)['href'])
    
    print(len(links))
    driver.quit()
    return links



links = get_server_links()
driver = webdriver.Chrome(service=service, options=options)
dates = []
servers = []
regions = []
names = []
prices = []
dt = datetime.now()


for link in links:
    driver.get(link)
    time.sleep(6)
    html = driver.page_source
    soup = bs(html, features="html.parser")
    
    title = soup.find('div', class_='main__title-skin').text
    #case for the Russian servers
    if ('server_31156' in link or 'server_36615' in link):
        server = title.split('-')[1].strip()
        region = title.split('-')[0].strip()
        region = re.sub('\[', '', region)
        region = re.sub('\]', '', region)
    else:
        server = title.split('-')[0].strip()
        region = title.split('-')[1].strip()

    #get all of the individual gold seller data and get them into their respective lists
    offer_boxes = soup.find_all('div', class_='other_offer-desk-main-box other_offer-div-box')
    for box in offer_boxes:
        name = box.find('div', class_='seller__name-detail').text.strip()
        price = box.find('span', class_='offer-price-amount').text.strip()
        price = re.sub(',', '', price)
        price = float(price)
        if (price > 1.2):
            continue
            
        dates.append(dt)
        servers.append(server)
        regions.append(region)
        names.append(name)
        prices.append(price)

    #check if the server has more than one paginated page of seller results
    #if it does, then go through all the pages t collect the data
    if check_exists_by_xpath(driver, "//a[contains(text(),'>')]/preceding-sibling::a[1]"):
        number_of_pages = int(driver.find_element(By.XPATH, "//a[contains(text(),'>')]/preceding-sibling::a[1]").text)
        #print(number_of_pages)
        for j in range(number_of_pages - 1):
            element = driver.find_element(By.XPATH, "//a[contains(text(),'>')]")
            
            #scroll the buttons into view that we need to click
            driver.execute_script('arguments[0].scrollIntoView();', element)
            driver.execute_script('window.scrollBy(0, -100);')
            element.click()
            time.sleep(4)
            html = driver.page_source
            soup = bs(html, features="html.parser")
            offer_boxes = soup.find_all('div', class_='other_offer-desk-main-box other_offer-div-box')

            for box in offer_boxes:
                name = box.find('div', class_='seller__name-detail').text.strip()
                price = box.find('span', class_='offer-price-amount').text.strip()
                price = re.sub(',', '', price)
                price = float(price)
                if price > 1.2:
                    continue
            
                dates.append(dt)
                servers.append(server)
                regions.append(region)
                names.append(name)
                prices.append(price)
    else: #no additional pages
        print('Only one page!')

    

driver.quit()
df1 = pd.DataFrame(zip(dates, servers, regions, names, prices), columns=['date', 'server', 'region', 'name', 'price'])
print(df1.head())

if not os.path.isfile('.\\gold_info.csv'):
    df1.to_csv('.\\gold_info.csv', header=True, index=False)
else:
    df1.to_csv('.\\gold_info.csv', mode='a', header=False, index=False)





#getting data for global means and such
df = pd.read_csv('gold_info.csv')
df.date = pd.to_datetime(df.date)
global_means = df.groupby(pd.Grouper(key='date', axis=0, freq='D'))['price'].mean()
global_means = global_means.rename('mean')

global_mins = df.groupby(pd.Grouper(key='date', axis=0, freq='D'))['price'].min()
global_mins = global_mins.rename('min')

global_info = pd.concat([global_means, global_mins],axis=1).reset_index()



#getting data for server means and such
server_means = df.groupby(['server', 'date'])['price'].mean().reset_index().rename(columns={'price':'mean'})
server_mins = df.groupby(['server', 'date'])['price'].min().reset_index().rename(columns={'price':'min'})
server_info = pd.concat([server_means, server_mins], axis=1)
server_info = server_info.loc[:,~server_info.columns.duplicated()]



#getting data for region means and such
region_means = df.groupby(['region', 'date'])['price'].mean().reset_index().rename(columns={'price':'mean'})
region_mins = df.groupby(['region', 'date'])['price'].min().reset_index().rename(columns={'price':'min'})
region_info = pd.concat([region_means, region_mins], axis=1)
region_info = region_info.loc[:,~region_info.columns.duplicated()]


global_info.to_csv('global_info.csv')
server_info.to_csv('server_info.csv')
region_info.to_csv('region_info.csv')


names_df = df.groupby(['date', 'name'])['price'].count().reset_index().sort_values(by=['price', 'name', 'date'], ascending=False)
historical_names_df = names_df.sort_values(by=['date'], ascending=True)
historical_names_df.to_csv('names_historical.csv')

current_names = names_df.drop_duplicates(subset=['name'])
current_names = current_names.reset_index().drop('index', axis=1).rename(columns={'name':'Seller', 'price':'Listings'})
current_names.to_csv('current_names.csv')
