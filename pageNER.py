import requests,re,json
from bs4 import BeautifulSoup,Comment
import pandas as pd 

import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()


def page_ner(url):
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html5lib')
        comm = soup.findAll(text=lambda text:isinstance(text, Comment))
        [cm.extract() for cm in comm]
        alltags = soup.findAll(text=True)
        visable_tags = [t for t in alltags if t.parent.name not in ['style','nav', 'script','script', 'head', 'title', 'meta','nav','link','footer','base','applet','iframe','embed','nodembed','object','param','source','[document]']]

        ner = []
        for tag in visable_tags:
            tag = re.sub(r'[\n\s\r\t/]+',' ', tag)
            if re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', tag):
                phone = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', tag)
                for ph in phone:
                    ner.append({'phone':ph})
            else:
                phone = []
            if re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text):
                email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)
                for em in email:
                    ner.append({'email':em})
            else:
                email = []         
            if re.findall(r'^[0-9]{5}(?:-[0-9]{4})?$', text) or re.findall(r'^[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d$', text):
                postalcode = re.findall(r'^[0-9]{5}(?:-[0-9]{4})?$', text) + re.findall(r'^[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d$', text)
                for pc in postalcode:
                    ner.append({'postalCode':pc})
            else:
                postalcode = []

            doc = nlp(str(tag))
            if len(doc.ents)>0:
                if tag not in ' '.join(phone+email+postalcode):
                    label = ','.join([x.label_ for x in doc.ents])
                    ner.append({label:tag})
            dd = pd.read_json(json.dumps(ner))
            dd.drop_duplicates(inplace=True)
            dd['link'] = url
        return dd
    else:
        print(url, ' connection failed!')


url = 'http://www.rel8ed.to/contact-us/'
info = page_ner(url)
print(info)




