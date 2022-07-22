#<o- made by mercuria -o>

import requests
from selenium import webdriver
import os,time,base64,getpass,sys
from bs4 import BeautifulSoup
import re
import shutil
import random

os.environ['NO_PROXY'] = '127.0.0.1'

thisPath=os.path.dirname( os.path.realpath(__file__) )
picklefile="{}/session.pickle".format(thisPath)
imageFile='{}/images.txt'.format(thisPath)
separator=" "
downloadDirectory='F:\\regenerated'
fname=''

def countdown(t):
    t = t-1
    real = t
    while t >= 0:
        if t == real:
            sys.stdout.write('Duration : {}s'.format(t))
        else:
            sys.stdout.write('\r'+'Duration : {}s'.format(t))
        time.sleep(1)
        t -= 1
    sys.stdout.write('\r')

def uploadToVimCn(imgPath):
    #upload to Vim-cn
    imgOpen = open(imgPath, 'rb')
    files = {'file': imgOpen}
    r = requests.post('https://img.vim-cn.com/',
                      data={'name': '@/path/to/image'}, files=files)
    imgOpen.close()
    return r.text

def getImages():
    with open(imageFile, 'r') as myfile:
        htmltext=myfile.readlines()
        htmltext=[ line.replace('\n',"").split(separator) for line in htmltext]
    return htmltext


def getSimilarImagePageLink(url):
    print("getting maxsize")
    selenumdriver.get('https://images.google.com/searchbyimage?hl=en-US&image_url={}'.format(url))
    htmltext=selenumdriver.page_source
    soup = BeautifulSoup(htmltext,"lxml")

    #this is the unique label before all search results
    #load all search results
    a_matrix = soup.find('div', string=["Pages that include matching images"])
    if a_matrix:

        #"rGhul IHSDrd" is the unique label before the first search result picture
        #load all result picture
        picture = a_matrix.find_all_next('a',attrs={'class':'rGhul IHSDrd'})
        max_index = 0
        max_size = 0
        for index in range(len(picture)):
            size = picture[index].find_next('span').get_text()
            num = re.findall(r'\d+', size)
            if (int(num[0])*int(num[1])) > max_size:
                max_index = index
                max_size = int(num[0])*int(num[1])
        print("images site link: https://www.google.com{}".format(picture[max_index].get("href")))

        return "https://www.google.com{}".format(picture[max_index].get("href"))
    else:
        return None

def saveImg(src,name):
    if "data:image" in src[:20]:
        imgdata = base64.b64decode(src.split(",")[1])
        extension=src[:40].split(";")[0].split("/")[1]
    else:
        response = requests.get(src,proxies={'http': 'http://localhost:10809', 'https': 'http://localhost:10809'})
        imgdata=response.content
        extension=response.headers['content-type'].split("/")[1]
    filename="{}/{}.{}".format(downloadDirectory,name,extension)
    print("saved image at ({})".format(filename))
    if imgdata:
        with open(filename, 'wb') as f:
            f.write(imgdata)
        return True


def downloadFromSimilarImagesPage(url,name):
    global fname
    selenumdriver.get(url)
    time.sleep(2)
    htmltext=selenumdriver.page_source
    soup = BeautifulSoup(htmltext,"lxml")
    div=soup.find("img")
    src= div.get("src")
    print(src)
    saveImg(src, name)
    shutil.move(fname, 'F:\\stabled')

    

    
def main():
    global selenumdriver
    global fname
    selenumdriver = webdriver.Firefox()
    for root, _, files in os.walk(u'.', topdown=False):
        for f in files:
            fname = os.path.join(root, f)
            for ext in {".jpg", ".jpeg", ".png", ".gif", ".bmp"}:
                if fname.lower().endswith(ext) and f[0] != 'z':
                    print(fname)
                    try:
                        similarImagePageLink = getSimilarImagePageLink(uploadToVimCn(fname))
                        #countdown(random.randint(20, 50))
                        name = os.path.splitext(f)[0]
                        if similarImagePageLink:
                            downloadFromSimilarImagesPage(url=similarImagePageLink, name=name)
                        else:
                            print("cannot get maxsize image search page")
                            newfname = os.path.join(root, "zeed_notmatch_" + f)
                            print('Alter Name: ' + newfname)
                            if os.path.exists(newfname):
                                os.remove(fname)
                            else:
                                os.rename(fname, newfname)
                        #countdown(random.randint(45, 75))
                        print('\n\n')
                    except Exception as e:
                        print(str(e))
                        print("quiting")


if __name__=="__main__":
    main()
    print('All Done!')
