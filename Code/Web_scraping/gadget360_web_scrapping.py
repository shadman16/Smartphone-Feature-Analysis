#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
#from google.colab import drive
from collections import Counter
import collections
import requests
import pandas as pd
import sys
import time
import json
import traceback
import re
import json
import numpy as np

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36', 'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"', 'sec-ch-ua-mobile': '?0', 'Upgrade-Insecure-Requests': '1'}
           
           
available_products=['Mobiles']
product=available_products[0]
final_csv_file='scraped_data_'+product.lower()+'_full_csv.csv'
urls_csv=product.lower()+'urls.csv'
scraped_json='scraped_data_'+product.lower()+'.json'
           
urll='https://gadgets.ndtv.com/brand/brand-details?isajax=1&category='+product+'&page='
listt=[]
for j in range(100):
  try:
    page = requests.get(urll+str(j+1),headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    pd_name = soup.find_all('a')
    pd_name=[l for l in pd_name]
    links_list=[]
    for k in pd_name:
      try:
        links_list.append(k['href'])
      except:
        pass
    listt=listt+links_list
  except:
    traceback.print_exc()
    pass
listt=list(set(listt))
pd.DataFrame({'urls':listt}).to_csv(urls_csv, index=False)

urlss=pd.read_csv(urls_csv)
urlss.columns
           
print(len(urlss['urls']))
print(list(urlss['urls'][:10]))

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

items_list=[]
counter=0
for i in list(urlss['urls']):
  counter=counter+1
  if(counter%10==0):
    print(counter)
  try:
    pagee=requests.get(i,headers=headers)
    dfs = pd.read_html(pagee.text)
    df = pd.concat(dfs)
    # if ((True) in list(df[0]=='Genre')): ## to exclude games and include only gaming consoles in games category
    #   continue
    df=df.reset_index().drop(['index'], axis=1)
    details=df[[0,1]].dropna().reset_index().drop(['index'], axis=1)
    for j in range(len(details[0])):
      if(details[0][j]==details[1][j]):
        details=details.drop(j)
    details=details.reset_index().drop(['index'], axis=1)
    m=details[0]
    d = {a:list(range(1, b+1)) if b>1 else '' for a,b in Counter(m).items()} # use this line to differentiate multiple attributes with same name for categories except mobile category
    # details[0]=['Sim '+str(d[x].pop(0))+' '+x if len(d[x]) else x for x in m] # to differentiate sim details for multiple sim mobiles in mobile categry
    details[0]=[x+' '+str(d[x].pop(0)) if len(d[x]) else x for x in m]
    det_dict=dict()
    for k in range(len(details[0])):
      det_dict[details[0][k]]=details[1][k]

    soup = BeautifulSoup(pagee.content, 'html.parser')
    try:
      star_cols = soup.find_all('span', attrs={'class': '_rbtxt'})
      star_cols=[str(s.text).replace('★', 'Stars') for s in star_cols]
      star_cent = soup.find_all('div', attrs={'class': '_rprg'})
      star_cent=[re.search('style="width:(.*)%; background', str(c)).group(1) for c in star_cent]
      for l in range(len(star_cent)):
        det_dict[star_cols[l]]=star_cent[l]
    except:
      print('exception')
      print(star_cols)
      traceback.print_exc()
      pass
    try:
      tot_rat = soup.find('span', attrs={'class': '_rvwtxt'})
      tot_rat=re.search('class="_rvwtxt">(.*) ratings  &amp;<', str(tot_rat)).group(1)
      det_dict['Total Ratings']=tot_rat
    except:
      pass
    try:
      picture = soup.find('picture')
      picture=re.search('<source srcset="(.*)" type="', str(picture)).group(1)
      det_dict['Picture URL']=picture
    except:
      pass
    det_dict['url']=i
    try:
      names_dict=df[['Product Name','Price in India']].dropna().to_dict('records')
      for m in names_dict:
        items_list.append(Merge(det_dict,m))
    except:
      items_list.append(det_dict)
      pass
  except:
    pass

with open(scraped_json, 'w') as fp:
    json.dump(items_list, fp)
    
uniq_attr=[]
for i in items_list:
  uniq_attr=uniq_attr+list(i.keys())
uniq_attr=list(set(uniq_attr))

df = pd.DataFrame(columns = uniq_attr)   
for i in items_list:
  df = df.append(i,ignore_index = True)  

df = df.iloc[df.isnull().sum(1).sort_values(ascending=True).index].reset_index().drop(['index'], axis=1)

nan_vals=dict()
for i in df.columns:
  nan_vals[i]=df[i].isnull().sum()

x=nan_vals
sorted_x = sorted(x.items(), key=lambda kv: kv[1])
import collections
sorted_dict = collections.OrderedDict(sorted_x)
sorted_x[50:]

order=[]
for w in sorted(nan_vals, key=nan_vals.get, reverse=False):
    order.append(w)
    
x=nan_vals
sorted_x = sorted(x.items(), key=lambda kv: kv[1])
import collections
sorted_dict = collections.OrderedDict(sorted_x)
len(sorted_x)

df = df[order]
df=df.reset_index().drop(['index'], axis=1)
df.head(1)

other_info=[]
for i in range(len(df)):
  temp_dict=dict()
  for j in order[50:]:
    if (str(df[j][i]) != str(list(df.head(1)['Height'])[0])): #  replace 'Voice Remote' with column name with nan in df.head(1)
      temp_dict[j]=df[j][i]
  other_info.append(temp_dict)

df=df.drop(order[50:], axis=1)
df['other_info']=other_info

df.to_excel("gadget360.xlsx", index=False, sheet_name='data')


# In[ ]:




