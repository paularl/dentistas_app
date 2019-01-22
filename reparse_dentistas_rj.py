# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 10:42:49 2019

@author: paula.romero.lopes
"""
from bs4 import BeautifulSoup
import urllib.request
import csv
import time
import os.path
import re

def load_url(url):
    retries = 3
    for i in range(retries):
        try:
            handle = urllib.request.urlopen(url)
            return handle.read()
        except urllib.request.URLError:
            if i+1 == retries:
                raise
            else: time.sleep(12)
def take_directions(l):
    
    try:
        details = l.find('li').find_all('p')
        try:
            direc = details[0].get_text().strip()
        except:
            direc=''
        try:
            type_cons = details[1].get_text().strip()
        except:
            type_cons = ''
        try:
            convenio = details[2].get_text().strip()
        except:
            convenio = ''
    except:
        direc, type_cons, convenio = '','','','' 
    return direc, type_cons, convenio
         
def take_speciality(l):
    exp = l.find('h4').getText()
    try:
        spec = re.search(r'\((.*?)\)',exp).group(1)
    except:
        spec = ''
    return spec

def take_url(l):
    a = l.find('a')
    return a.get('href')

def extract_data(l):
    props = l.find('div','panel-body rank-element padding-top-2 padding-bottom-1').attrs
    lat = props['data-object-lat']
    long = props['data-object-lon']
    name = props['data-eecommerce-name']
    exp = take_speciality(l)
    direc, type_c, conv = take_directions(l)
    link = take_url(l)
    return (name,exp,direc,type_c,conv,lat,long,link)
    
if __name__=='__main__':
    
    bairros = ['gloria','humaita','ipanema','jardim-botanico','lagoa','laranjeiras','leblon',
    'leme','rocinha','sao-conrado','urca','vidigal']
        
    fout = 'dentistas_2019_bairros.csv'
    
    if not os.path.isfile(fout):
        print('creating output file')   
        with open(fout,'w') as f:
            writer=csv.writer(f, delimiter=';', quotechar='"', lineterminator = '\n', quoting=csv.QUOTE_ALL)
            row = ['NAME','ESPECIALIDADE','ENDERECO','TIPO_CONSULTA','CONVENIOS','LAT','LONG','LINK']
            writer.writerow(row)
    div_old = []
    print('file already exists')
    with open(fout,'a') as f:
        writer=csv.writer(f, delimiter=';', quotechar='"', lineterminator = '\n', quoting=csv.QUOTE_ALL)
        for bairro in bairros:
            for p in range(1,100):
                base_url = 'https://www.doctoralia.com.br/local/%s-rio-de-janeiro-rj/dentista/%d' % (bairro,p)
                print(base_url)
                r = load_url(base_url)
                soup = BeautifulSoup(r, 'lxml')
                div = soup.find('ul', {'class':'search-list list-unstyled'})
                div = soup.find('div',{'data-id':'search-results-container'})
                if div_old == div:
                    break
                div_ul = div.find('ul',{'data-id':'search-list'})
                list_doctors = div_ul.find_all('li', recursive=False)
                for l in list_doctors:
                    row = extract_data(l)
                    writer.writerow(row)
                div_old = div