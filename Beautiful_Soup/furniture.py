from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://newyork.craigslist.org/d/furniture/search/fua"

# Getting the webpage, creating a Response object.
response = requests.get(url)

# Extracting the source code of the page.
data = response.text

# Passing the source code to Beautiful Soup to create a BeautifulSoup object for it.
soup = BeautifulSoup(data, 'lxml')

# Extracting all the &lt;a&gt; tags whose class name is 'result-title' into a list.
titles = soup.findAll('a', {'class': 'result-title hdrlnk'})

# Extracting text from the the &lt;a&gt; tags, i.e. class titles.
lst = []
for i, title in enumerate(titles):
    lst.append([i,title.text])

print lst
