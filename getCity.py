import requests, re

with open('city-in-canada.csv','rb') as f:
    cities = f.read().decode('utf8')..replace('\r','').split('\n')[1:]
    cities = [c for c in cities if ',' in c]

parta = [','.join(c.split(',')[:-1]) for c in cities]
partb = [','.join([c.split(',')[0],c.split(',')[-1]]) for c in cities]
cities = parta + partb

def get_city(url):
    if not url.startswith('http://'):
        url = 'http://'+url
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    html = requests.get(url, headers=header)
    page = str(html.content)
    print(page)
    with open('tt.txt','w') as t:
      t.write(page)
    page = re.sub(r'\W',' ',page)
    page = re.sub(r'\s+',' ',page).lower()
    print(page)
    cand = []
    for city in cities:
        cc = city.split(',')
        if city.replace(',', ' ').lower() in page:
            print('yes')
            cand.append(city)
    print(cand)
    if cand:
        return cand[-1], html.status_code
    else:
        return '', html.status_code
      
get_city('http://www.prestigepavingltd.ca/')
