from bs4 import BeautifulSoup
import requests
import sys

def getPageText(url):
    user_agent = {'User-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17'}
    r=requests.get(url, headers = user_agent)
    if r.status_code==200:
        return r.text
    else:
        return ""

def bs4PrettyPrint(soup):
   print (soup.prettify())

def getLinks(soup):
   for link in soup.findAll('a'):
        #print link['href']
        if 'github' in link['href']:
            print link.string,"\n----------------\n",link['href'],"\n----------------\n",link.parent.parent.text,"\n----------------\n"
        
def main():
    url=sys.argv[1]
    soup=BeautifulSoup(getPageText(url), 'html.parser')
    #bs4PrettyPrint(BeautifulSoup(getPageText(url), 'html.parser'))
    getLinks(soup)
    
  
if __name__=="__main__":
    main()
   
 
