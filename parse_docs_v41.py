#! python

from bs4 import BeautifulSoup
import urllib.request
import unicodecsv as csv
import time
import os.path

def data_extract(target,prefix):
        try:          
            link = target.a['href']
            link = prefix+link
            print('processing...', link)
        except: 
            print('erro link')
            pass
        try:
            r = load(str(link))
            soup = BeautifulSoup(r, 'lxml')
        except: 
            print('erro bs4')
            error = 2
            pass
        try:
            data = soup.find("span", class_="location").a  
            name = data.attrs['data-name']
            lat = data.attrs['data-lat']
            lon = data.attrs['data-lng']
            addresspeq = data.attrs['data-address']
            fulladdress = data.attrs['data-full-address']
            error = 0
        except:
            error = 1
            try:
                full_address = soup.find("span", class_="street").text
                name = soup.find("div", class_="title").h1.text
                print('no loc, returning full address')
            except:
                pass
            pass
        if error == 0:
            return (name, lat, lon, addresspeq, fulladdress, error)
        if error == 1:
            return (name, full_address, error)
        if error == 2:
            return (None)

def parse_city(city):
        
        r = load('http://www.doctoralia.com.br/%s' % (city))
        soup = BeautifulSoup(r, 'lxml')
        c = city.split('/')[-1].split('-')[0].upper()
        print('city', c)
        targets = soup.find_all("section", class_="content" )
        print('number of doctors:',len(targets))

        if len(targets) > 0 & len(targets) < 20:
            for i in range(len(targets)):
                d = data_extract(targets[i],'http://www.doctoralia.com.br')
                writer.writerow(d)

        if len(targets) == 20:
            while soup.find("li",class_="PagedList-skipToNext"):
                link = soup.select("li.PagedList-skipToNext a")[0]
                print(link)
                pages = link.get('href')
                r = load('http://www.doctoralia.com.br/%s' % (pages))
                c = city.split('/')[-1].split('-')[0].upper()
                print('city', c)
                soup = BeautifulSoup(r, 'lxml')
                targets = soup.find_all("section", class_="content" )
                for i in range(len(targets)):
                    d = data_extract(targets[i],'http://www.doctoralia.com.br')
                    writer.writerow(d)

def parse_state(state):
    city_list = []
    r = load('http://www.doctoralia.com.br/sitemap/medicos/estado/%s/odontologia-1433' % state)
    print('Satate:', state.split('+')[-1].split('-')[0].upper())
    soup = BeautifulSoup(r, 'lxml')
    for a in soup.select("div.sitemap li a"):
        city = a.get('href')
        print(city)
        city_list.append(city)
    return city_list
    
def load(url):
    retries = 3
    for i in range(retries):
        try:
            handle = urllib.request.urlopen(url)
            return handle.read()
        except urllib.request.URLError:
            if i+1 == retries:
                raise
            else: time.sleep(42)

#--------------------------------- For doctors ------------------------------------------------

state_list=['ceara+ce-10378','distrito+federal+df-10399','espirito+santo+es-10379','goias+go-10380',
            'maranhao+ma-10381','mato+grosso+do+sul+ms-10383','mato+grosso+mt-10382','minas+gerais+mg-10384',
            'para+pa-10385','paraiba+pb-10386','parana+pr-10387','pernambuco+pe-10388','piaui+pi-10389',
            'rio+de+janeiro+rj-10390','rio+grande+do+norte+rn-10391','rio+grande+do+sul+rs-10392','rondonia+ro-10393',
            'roraima+rr-10394','santa+catarina+sc-10395','sao+paulo+sp-10396','sergipe+se-10397','tocantins+to-10398']

fout = 'dentistas.csv' # file name

if os.path.isfile(fout):
    print('file already exists')
    with open(fout,'a') as f:
        print('coco')
        writer=csv.writer(f, delimiter='\t', quotechar='"', lineterminator = '\n', quoting=csv.QUOTE_ALL)
        for state in state_list:
            print(state)
            try:
                city_list = parse_state(state)
                print(city_list)
                for city in city_list:
                    parse_city(city)
            except: pass

else:
    with open(fout,'w') as f:
        writer=csv.writer(f, delimiter='\t', quotechar='"', lineterminator = '\n', quoting=csv.QUOTE_ALL)
        for state in state_list:
            city_list = parse_state(state)
            print(city_list)
            for city in city_list:
                parse_city(city)
