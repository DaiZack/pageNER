import requests,re,json
from bs4 import BeautifulSoup,Comment
from collections import Counter

import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()

def site_ner(url):
  if not url.endswith('/'):
    url += '/'
  ner = {'EMAIL':[],'PHONE':[],'ADDRESS':[],'POSTALCODE':[],'LOC':[],'ORG':[],'GPE':[],'PERSON':[],'EVENT':[], 'KEYWORDS':[]}
  level = 0
  def page_ner(url0):
      print(url0)
      page = requests.get(url0)
      if page.status_code == 200:
          soup = BeautifulSoup(page.content, 'html5lib')
          comm = soup.findAll(text=lambda text:isinstance(text, Comment))
          [cm.extract() for cm in comm]
          alltags = soup.findAll(text=True)
          visable_tags = [t for t in alltags if t.parent.name not in ['style','nav', 'script','script', 'head', 'title', 'meta','nav','link','footer','base','applet','iframe','embed','nodembed','object','param','source','[document]']]
          
          tags = soup.select("a['href']")
          links = [tag['href'] for tag in tags if tag['href'].startswith(url) or tag['href'].startswith(url.replace('http','https')) or not tag['href'].startswith('http')]
          if links:
            links = [link if link.startswith(url) else url+re.findall(r'\W*(\w.*)',link)[0] for link in links if re.findall(r'\W*(\w.*)',link)]
            links = list(set(links))
            contactlinks = [cl for cl in links if 'contact' in cl]
          
          text = '. '.join(visable_tags)
          token = nlp(text.lower())
          token = [tk.lemma_ for tk in token if (not tk.is_stop) and tk.is_alpha]
          keywords = [c[0] for c in Counter(token).most_common(20)]
          webstopwords = ['http','www','home','page','time','out','error','service','server','connect','fail','fobiden','skip','start','contact','email','facebook','read','more','help','hour','twitter','google','about','back','search','next','last','menu','news','blog','solution','address','phone','website','copyright','reserved','english']
          keywords = [keyword for keyword in keywords if 3<len(keyword)<20 and keyword not in webstopwords][:20]
          ner['KEYWORDS'] += keywords
          
          for tag in visable_tags:
              tag = re.sub(r'[\n\s\r\t/]+',' ', tag)
              if re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', tag):
                  phone = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', tag)
                  for ph in phone:
                      ner['PHONE'].append(ph)
              else:
                  phone = []
              if re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", tag):
                  email = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", tag)
                  for em in email:
                      ner['EMAIL'].append(em)
              else:
                  email = []         
              if re.findall(r'\b[0-9]{5}(?:-[0-9]{4})?\b', tag) or re.findall(r'\b([A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d)\b', tag):
                  postalcode = re.findall(r'\b[0-9]{5}(?:-[0-9]{4})?\b', tag) + re.findall(r'\b([A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d)\b', tag)
                  for pc in postalcode:
                      ner['POSTALCODE'].append(pc)
              else:
                  postalcode = []

              doc = nlp(str(tag))
              if len(doc.ents)>0:
                for x in doc.ents:
                  for lb in ['LOC','ORG','GPE','PERSON','EVENT']:
                    if x.label_ == lb:
                      ner[lb].append(x.text)
                labels = [x.label_ for x in doc.ents]
                texts = [x.text for x in doc.ents]
                if tag not in ' '.join(phone+email+postalcode):
                  if len(labels) >1:
                    if labels[0] in ['CARDINAL','DATE'] and labels[1] in ['LOC','ORG','GPE','PERSON']:
                      ner['ADDRESS'].append(' '.join(texts))
          return contactlinks
      else:
          print(url0, ' connection failed!')
          
  contactlinks = page_ner(url)
  for cl in contactlinks:
    page_ner(cl)

  for key in ner.keys():
    print(ner[key])
    ner[key] = list(set(ner[key]))
  return ner

url = 'https://brocku.ca'
info = site_ner(url)
print(info)

