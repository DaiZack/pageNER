with open('city-in-canada.csv','rb') as f:
    cities = f.read().decode('utf8').split('\n')[1:]
    cities = [c for c in cities if ',' in c]

def get_city(url):
    if not url.startswith('http://'):
        url = 'http://'+url
    page = str(requests.get(url).content)
    print(page)
    with open('tt.txt','w') as t:
      t.write(page)
    page = re.sub(r'\W',' ',page)
    page = re.sub(r'\s+',' ',page).upper()
    print(page)
    cand = []
    for city in cities:
        cc = city.split(',')
        if city.replace(',', ' ').upper() in page:
            cand.append(city)
    print(cand)
    if cand:
        return cand[-1]
        return ''
      
get_city('www.fenigo.com')
