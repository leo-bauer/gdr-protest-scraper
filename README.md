# GDR Peaceful Revolution Protest Data Scraper

Python scraper for East German Peaceful Revolution Protest Data

The file scraper_protest.py contains the scraper. As it stands, the scraper stores individual protest events and records data for all 15 variables provided on the website: date, location, GDR district, post-unification state, population size of protest event locality in 1989, minimum estimate of participants, maximum number of participants, whether the church organized the protest, organizing entity, event description, protest event subject, specific details, whether the event is a demonstration, whether the event is a rally, and finally the url of the page from where the event was scraped.

Using the scraper is straightforward. Simply install the packages needed and run the code. In scraping, event data is stored in lists and subsequently transformed into a dataframe with one event per row and the variables in the columns. The only changes necessary when running the scraper on Mac and Windows and maybe some Linux distributions other than mine may be around the webdriver. The scraper uses the one provided by the selenium package and in my case works flawlessly with Firefox 112 without any further configurations necessary. 
