import requests
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime

# suppress automated browser window
options = webdriver.FirefoxOptions()
options.add_argument('-headless')

# test webdriver
drivertest = webdriver.Firefox()
drivertest.get('https://www.goabase.net/')
sleep(3)
drivertest.close()

# download website
page = requests.get("https://www.archiv-buergerbewegung.de/themen-sammlung/demonstrationen/")

# check status
page.status_code

# check HTML text
if page.status_code == 200:
    print(page.text)

# parse site and find map tag using bs4
soup = BeautifulSoup(page.content, 'html.parser')
x1 = soup.find_all("option")
date_hrefs = []
for tag in x1:
    date_hrefs.append(tag.get("value"))

date_hrefs = date_hrefs[1:]

# create URLs
date_hrefs1 = []

for i in date_hrefs:
    j = "https://www.archiv-buergerbewegung.de" + i
    date_hrefs1.append(j)

# scrape locations from date urls
dateloc = []

for i in tqdm(range(len(date_hrefs1))):
    urlx = date_hrefs1[i]
    driverx = webdriver.Firefox(options=options)  # add 'options=options' for headless webdriver
    driverx.get(urlx)
    soupx = BeautifulSoup(driverx.page_source, 'html.parser')
    overlay_div = soupx.find("div", id="overlay-content")
    links = overlay_div.find_all("a")
    for link in links:
        x = link.get("href")
        y = "https://www.archiv-buergerbewegung.de" + x
        dateloc.append(y)

    driverx.close()

# scrape data
data = []

for i in tqdm(range(len(dateloc))):
    urly = dateloc[i]
    drivery = webdriver.Firefox(options=options)  # add 'options=options' for headless webdriver
    drivery.get(urly)
    soupy = BeautifulSoup(drivery.page_source, 'html.parser')
    entries = soupy.find_all("div", class_="entry")

    if entries is not None:
        for entry in entries:
            x = entry.find_all("p")
            y = [tag.get_text().strip() for tag in x]
            z = y[1:]
            z1 = [elem.split(":", 1)[1].strip() for elem in z]
            z1.append(urly)
            data.append(z1)
    else:
        z1 = [urly]
        data.append(z1)

    drivery.close()

# check length of lists in data
len_list = []

for i in data:
    len_list.append(len(i))

unique_nums = set(len_list)
print(unique_nums)

# create df from lists
data_list = []

for i in data:
    datax = {"date": i[0], "location": i[1], "district (gdr)": i[2], "state (frg)": i[13], "population (1989)": i[12],
             "participants_min": i[4], "participants_max": i[3], "church": i[5], "organizer": i[7], "description": i[6],
             "subject": i[8], "specifics": i[9], "demonstration": i[10], "rally": i[11], "url": i[14]}
    data_list.append(datax)

df = pd.DataFrame(data_list)

# data mods for date, numerical values and binary variables
df = df.drop(['url'], axis=1)

date_new = []

for i in df["date"]:
    date_obj = datetime.strptime(i, "%d.%m.%Y")
    date_isoformat = date_obj.date().isoformat()
    date_new.append(date_isoformat)

df["date"] = date_new

df["population (1989)"] = pd.to_numeric(df['population (1989)'])


def convert_to_numeric(m):
    if m == 'keine Angaben':
        return np.nan
    else:
        return int(m)


df["participants_min"] = df["participants_min"].apply(convert_to_numeric)
df["participants_max"] = df["participants_max"].apply(convert_to_numeric)


def convert_to_binary(m):
    if m == 'x':
        return 1
    else:
        return 0


df["church"] = df["church"].apply(convert_to_binary)
df["demonstration"] = df["demonstration"].apply(convert_to_binary)
df["rally"] = df["rally"].apply(convert_to_binary)

# export to csv
df.to_csv('protest_raw.csv')
