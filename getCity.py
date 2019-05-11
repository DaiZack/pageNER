import requests, re

page = requests.get('https://raw.githubusercontent.com/zdrel8ed/pageNER/master/city-in-canada.csv').content.decode('utf8','ignore')
rows = page.split('\n')
parta = [','.join(r.split(',')[:-1]) for r in rows]
partb = [','.join([r.split(',')[0],r.split(',')[-1]]) for r in rows]
cities = (parta + partb)[1:-1]

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
