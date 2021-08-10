from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import sys,os,time
import re
import tldextract
import urllib
import requests

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome("./chromedriver", options=chrome_options) 
driver.set_page_load_timeout(20)

count_js = 0
js_files=[]
js_file_faild=[]
count_urls = 0
count_domain=0
w=open(sys.argv[1],'r')
for jj in w:
    count_domain += 1 
w.seek(0)
for j in w:
    count_urls+=1
    print("\033[39m["+str(count_urls)+"/"+str(count_domain)+"] [+] "+j.rstrip('\n'))
    try:
        driver.get(j)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        l = [i.get('src') for i in soup.find_all('script') if i.get('src')]
    except Exception as e:
        continue	
    for k in l:
        count_js+=1
        if k.startswith('//') and 'www.' not in k:
            try:
                url = "https:"+k
                status_code = urllib.request.urlopen(url).getcode()
                print("\033[32m["+str(status_code)+"] "+url)
                res = requests.et(url)
                source = res.text
                
            except:
                js_files.append(url)
        elif k.startswith('/') and 'www' not in k:
            url=j.rstrip('\n')+k
            try:
                status_code = urllib.request.urlopen(url).getcode()
                print("\033[32m["+str(status_code)+"] "+url)
            except:
                js_files.append(url)
        elif k[0:8] != 'https://' and k[0:7] != 'http://' and 'www.' not in k:
            try:
                url = j.rstrip('\n')+'/'+''.join(k)
                status_code = urllib.request.urlopen(url).getcode()
                print("\033[32m["+str(status_code)+"] "+url)
            except:
                js_files.append(url)
        elif k.startswith('http:'):
            try:
                url = "https://"+k
                status_code = urllib.request.urlopen(url).getcode()
                print("\033[32m["+str(status_code)+"] "+url)
            except:
                js_files.append(url)
        elif k.startswith('//') and 'www.'in k:
            try:
                url = "https:"+k
                status_code = urllib.request.urlopen(url).getcode()
            except:
                js_files.append(url)
        else:
            try:
                status_code = urllib.request.urlopen(k).getcode()  
                print("\033[32m["+str(status_code)+"] "+k)
            except:
                js_files.append(k)

print("\033[39m[*] Rechecking")
for ii in js_files:
    if ii.startswith('http://'):
        try:
            url = ii.replace("http://","http://www.")
            status_code = urllib.request.urlopen(url).getcode()
            print("\033[32m["+str(status_code)+"] "+url)
        except:
            js_file_faild.append("[404] "+url)	
    elif ii.startswith('https://'):
        try:
            url = ii.replace("https://","https://www.")
            status_code = urllib.request.urlopen(url).getcode()
            print("\033[32m["+str(status_code)+"] "+url)
        except:
            js_file_faild.append("\033[31m[404] "+url)
    else:
        pass
for faild in js_file_faild:
    print(faild)
driver.quit()
w.close()
print("\033[39m\n[+] Task Completed!")
print("\033[39m---------------------") 
print('[+] Total urls    :'+str(count_urls))
print('[+] Total js files:'+str(count_js))   
