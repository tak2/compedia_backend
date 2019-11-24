#%%
# Load the  libraries 
import pandas as pd 
import pywikibot
import requests
import csv
import time
import urllib.request, json
from urllib.parse import quote

#%%
# Read data from file 'filename.csv' 
csvfilename = "forbes2000_q.csv"
data = pd.read_csv(csvfilename) 
# Preview the first 5 lines of the loaded data 
data.head()
#if you import drop the first column
data= data.drop(data.columns[0], axis=1)
#%%
 

def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []
    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr
    results = extract(obj, arr, key)
    return results
def getqfromurljson(corpname):
    try:
        urlc = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search="+ quote(corpname,safe='/:?=&') +"&format=json&language=en&uselang=en&type=item"
        #print(urlc)
        with urllib.request.urlopen(urlc) as url:
            data1 = json.loads(url.read().decode())
            name = extract_values(data1, 'id')[0]
    except:
        name = ""
    return name
 
#%%
def getcountryfromurljson(qcode):
    try:
        urlc = "https://www.wikidata.org/w/api.php?action=wbgetclaims&entity="+ qcode +"&property=P17&format=json"
                #print(urlc)
        with urllib.request.urlopen(urlc) as url:
            dataq = json.loads(url.read().decode())
            nameq = extract_values(dataq, 'id')[0]
        urlc = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids="+ nameq +"&props=labels&languages=en&format=json"
        with urllib.request.urlopen(urlc) as url:
            data1 = json.loads(url.read().decode())
            name = extract_values(data1, 'value')[0]

     
    except:
        name = ""
    return name

print (getcountryfromurljson("Q148"))

# %%
data['q'] = ''
#quote('http://www.oschina.net/search?scope=bbs&q=C语言',safe='/:?=&')
#quote(,safe='/:?=&')
for i in range(len(data)):
    data['q'].values[i] = getqfromurljson(data['name'].values[i])
#%% country
data['country'] = ''
#quote('http://www.oschina.net/search?scope=bbs&q=C语言',safe='/:?=&')
#quote(,safe='/:?=&')
for i in range(len(data)):
    data['country'].values[i] = getcountryfromurljson(data['q'].values[i])


# %%
# save data to json or csv
data.to_json(r'forbes2000_q_country.json')
data.to_csv('forbes2000_q_country.csv')


# %%
