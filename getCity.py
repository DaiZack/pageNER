import requests, re
import pandas as pd

data = pd.read_csv('https://raw.githubusercontent.com/zdrel8ed/pageNER/master/city-in-canada.csv')
data.loc[:,['city','province']]

dataa = data.loc[:,['city','province']].to_csv(index=0, header=0)
datab = data.loc[:,['city','abbrev']].to_csv(index=0, header=0)
data0 = dataa+datab
cities = data0.replace('\r','').split('\n')[1:]
cities = [c for c in cities if ',' in c]

def get_city(url):
    if not url.startswith('http://'):
        url = 'http://'+url
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    html = requests.get(url, headers=header)
    page = str(html.content)
    with open('tt.txt','w') as t:
      t.write(page)
    page = re.sub(r'\W',' ',page)
    page = re.sub(r'\s+',' ',page).lower()
    cand = []
    for city in cities:
        cc = city.split(',')
        if city.replace(',', ' ').lower() in page:
            cand.append(city)
    if cand:
        return cand[-1], html.status_code
    else:
        return '', html.status_code
      
get_city('http://www.prestigepavingltd.ca/')
