from bs4 import BeautifulSoup
import requests
import sys
import csv
import re
import pickle
from pprint import pprint
import json

def getPageText(url):
    user_agent = {'User-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17'}
    r=requests.get(url, headers = user_agent)
    if r.status_code==200:
        return r.text
    else:
        return ""

def bs4PrettyPrint(soup):
   print (soup.prettify())

def getUrls(source):
    urls=[]
    with open(source, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            urls.append((row[0],row[1]))
    return urls

def getWords(content):
    return [x.strip() for x in re.sub("[^\w]", " ",  content).split()]

def isGitRepositoryURL(link):
    return bool(re.match("https?://github.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/*$",link))

def mstrip(t):
    if t is not None: 
        return t.strip()
    else:
        return ""
  
def getContext(gurl,surl):
    t=getPageText(surl)
    cdata=[]
    if t:
        soup=BeautifulSoup(t, 'html5lib')
        for link in soup.findAll('a'):
           #print link.string,link['href'], isGitRepositoryURL(link['href'])
           if link.get('href','')==gurl or isGitRepositoryURL(link.get('href','')):
                cdata.append( [\
                link.get('href',''),surl,mstrip(link.string),\
                mstrip(link.parent.text),
                mstrip(link.parent.parent.text),\
                mstrip(link.parent.parent.parent.text),\
                #mstrip(link.parent.parent.parent.parent.text)\
                #mstrip(link.parent.parent.parent.parent.parent.text)\
                ])
    #print len(cdata)
    return cdata     
        
def main():
    csv=sys.argv[1]
    urls=getUrls(csv)
    dataWordDict={}
    dataDict={}
    dataLoc="data/contextStrings.json"
    dataWordSplitLoc="data/contextStringsWords.json"

    for index,url in enumerate(urls[:10]):
        contexts=getContext(url[0],url[1])  
        if contexts:
            for context in contexts:
                #print context
                dataWordDict[context[0]]=[context[1]]+[getWords(x) for x in context[2:]]
                dataDict[context[0]]=context
        print "processed",url[0],index+1,"out of",len(urls),"got a match",len(contexts)>0
    
    print len(dataDict.keys()) 
    json.dump(dataWordDict,open(dataWordSplitLoc,"wb"))
    json.dump(dataDict,open(dataLoc,"wb"))
   
          
 
if __name__=="__main__":
    main()
   
 
