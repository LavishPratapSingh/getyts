from bs4 import BeautifulSoup
import requests
import json
def conv(js1,js2):
    with open('yts.json') as file:
        old=json.load(file)
    with open('yts.json','w') as file:    
        if json.dumps(old)=="{}":
            json.dump(js1,file,indent=4)
        else:
            if old.get(js2):
                old[js2]=old[js2]+js1[js2]
            else:
                old[js2]=js1[js2]
            json.dump(old,file,indent=4)
def getmd(soup):
    js={}
    content=soup.find('div',{'class':"col-xs-10 col-sm-14 col-md-7 col-lg-8 col-lg-offset-1"}).find('div',{'class':'hidden-xs'}).text.strip()
    name,year,genre=content.splitlines()
    genre=genre.split(' / ')
    alllink=soup.find('p',{'class':'hidden-md hidden-lg'}).find_all('a')
    links={}
    for i in alllink:
        links[i.text]=i['href']
    js[year]=[{"name":name,"genre":genre,"links":links}]
    return js,year
def geturl(response):
    link=[]
    soup=BeautifulSoup(response.text,'lxml')
    content=soup.find_all('div',{'class':'browse-movie-wrap col-xs-10 col-sm-4 col-md-5 col-lg-4'})
    for id in content:
        link.append(id.find('a',{'class':'browse-movie-link'})['href'])
    if link==[]:
        return 1
    else:
        for id in link:
            newres=requests.get(id)
            newsoup=BeautifulSoup(newres.text,'lxml')
            js1,js2=getmd(newsoup)
            conv(js1,js2)
    return 0
def main(s,e,a,b):
    if a<=b and s>=e:
        if a!=1:
            x=geturl(requests.get("http://yts.mx/browse-movies/0/all/all/0/latest/"+str(s)+"/all?page="+str(a),verify=False))
            if x==1:
                main(s+1,e,1,b)
            else:
                main(s,e,a+1,b)
        else:
            x=geturl(requests.get("http://yts.mx/browse-movies/0/all/all/0/latest/"+str(s)+"/all",verify=False))
            if x==1:
                main(s+1,e,1,b)
            else:
                main(s,e,a+1,b)            
    else:
        print("done")
#s=int(input())
#e=int(input())          
main(2022,2022,1,2)