
# Load the  libraries 
import pandas as pd 
import pywikibot
import requests
import csv
import time
import urllib.request, json
from urllib.parse import quote


# Read data from file 'filename.csv' 
csvfilename = "Forbes-Global-2000-List-2019.csv"
data = pd.read_csv(csvfilename) 
# Preview the first 5 lines of the loaded data 
#data.head()


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
#to test the functions to get teh qcode 
#print (getqfromurljson("Ping An Insurance Group"))

# add column to the dataframe
data['q'] = ''

#loop through the dataframe to add the qcode
for i in range(len(data)):
    data['q'].values[i] = getqfromurljson(data['name'].values[i])



# save data to json orand csv
data.to_json(r'forbes2000_q.json')
data.to_csv('forbes2000_q.csv')

