from requests import get
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

global i
global internalLinks
AllInternalLinks = set()
global AllInternalEmails
AllInternalEmails = set()

driver = webdriver.Chrome('/home/vanrajsinh/Downloads/chromedriver_linux64r/chromedriver')
url = 'https://socalbni.com/en-US/chapterlist?chapterName=&chapterCity=&chapterArea=&chapterMeetingDay=&chapterMeetingTime=&regionIds=4810,4828,4868'
chrome_options = Options()
chrome_options.add_argument("--headless")
driver.get(url)
time.sleep(7)
html = driver.page_source

html_soup = BeautifulSoup(html, 'html.parser')
type(html_soup)

def getInternalLinks(bsobj, includeurl):
    internalLinks = []
    for links in bsobj.findAll("a", {"href": re.compile("^(/|.*" + includeurl + ")")}):
        if links.attrs['href'] is not None:
            if links.attrs["href"] not in internalLinks:
                internalLinks.append(links.attrs['href'])

    for link in internalLinks:
        truncURL = link.replace("http://", "").replace("https://", "").replace(includeurl, "")
        sep = "/"
        spliturl = truncURL.split(sep, 2)
        if len(spliturl) >= 2:
            truncURL = spliturl[1]
            removeParameterURL = spliturl[1].split("?", 1)
            if len(removeParameterURL) >=1:
                truncURL = removeParameterURL[0]
        else:
            truncURL = ""
        if truncURL not in AllInternalLinks:
            if link != "http://"+includeurl and link != "https://"+includeurl and link != '/' and link != "http://"+includeurl+'/' and link != "https://"+includeurl+'/':
                AllInternalLinks.add(truncURL)
                print("http://"+includeurl+"/" + truncURL)
                try:
                    websitepage = get("http://"+includeurl+"/" + truncURL)
                except:
                    continue
                new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z0-9\.\-+_]+", websitepage.text, re.I))
                AllInternalEmails.update(new_emails)
                websitepage_soup = BeautifulSoup(websitepage.text, 'html.parser')
                getInternalLinks(websitepage_soup,includeurl)
    return (internalLinks)

def splitaddress(address):
    return (address.replace("http://", "").replace("https://", "").split("/"))


URLList = ["https://socalbni.com/en-US/chapterdetail?chapterId=xCkE5vu819%2FvDbucp8uBZw%3D%3D&name=BNI+The+Hidden+Jewel+BNI", "https://socalbni.com/en-US/chapterdetail?chapterId=VuBqs7BrLzebrLxfCVtZDw%3D%3D&name=BNI+Top+Producers+BNI", "https://socalbni.com/en-US/chapterdetail?chapterId=qSzDBfC0yl%2F%2BLlHedPr5UQ%3D%3D&name=BNI+Trusted+Referral+Partners+BNI", "https://socalbni.com/en-US/chapterdetail?chapterId=wQXoG8u7vxiPk8xVDCbBoA%3D%3D&name=BNI+Waterfront+BNI", "https://socalbni.com/en-US/chapterdetail?chapterId=XZh00hvkVJxbQMnbtjMS8w%3D%3D&name=BNI+WOMBATs+BNI","https://socalbni.com/en-US/chapterdetail?chapterId=5o%2FqmiPnZn38DqHcNT37rA%3D%3D&name=BNI+World+Famous+Tustin+BNI","https://socalbni.com/en-US/chapterdetail?chapterId=6Q0j11rOkKSncpkAn%2FWEJQ%3D%3D&name=BNI+Yorba+Linda+BNI"]
for row in URLList:
    memberListURL = row
    BNIName = "The Hidden Jewel BNI - CA Orange Co. North"
    driver.get(memberListURL)
    time.sleep(7)
    memberListSite = driver.page_source
    memberListSoup = BeautifulSoup(memberListSite, 'html.parser')
    memberList = memberListSoup.find('table', class_="table table-hover listtables dataTable no-footer dtr-inline")
    inner_rows = memberList.findChildren(['tr'])

    for inner_row in inner_rows:
        if inner_row.a == None:
            continue
        memberURL = "https://socalbni.com/en-US/" + inner_row.a['href']

        if memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=oB3j%2BjWyzYlUsQKwGLiEEw%3D%3D&cmsv3=true&name=Brooke+Stephens" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=oB3j%2BjWyzYlUsQKwGLiEEw%3D%3D&cmsv3=true&name=Brooke+Stephens" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=uMPmoBkhQwdaqkBCNqbYIA%3D%3D&cmsv3=true&name=Charlie+Gallagher" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=qvTXVwxw4H9P4l%2BiQYz9vA%3D%3D&cmsv3=true&name=Christina+Clayson" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=53jGuq5GJ2DbZl1yARxfag%3D%3D&cmsv3=true&name=Craig+Pearcy" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=K0rwiJKcFjD1xdRZsYQLuw%3D%3D&cmsv3=true&name=Daryl+Pierce" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=Jyvay%2FE9%2Bk7mfNuvM5cTyw%3D%3D&cmsv3=true&name=Edward+Carter" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=1yBMSG%2BM7aEPhd1AtATgzg%3D%3D&cmsv3=true&name=Eric+Dyer" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=hpSIP%2BQWFJzVNGhemrMI9A%3D%3D&cmsv3=true&name=Genene+Dunn" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=6VqgfqebVy9eUcU0dNGnWw%3D%3D&cmsv3=true&name=Greg+Berardino" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=JaNGfoB%2BhUlpK8D5MUlqgg%3D%3D&cmsv3=true&name=Greg+T+Davies" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=MAT6neWpgt4P9K1NvFpeZA%3D%3D&cmsv3=true&name=Jeff+Oymaian" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=jG4nGFDIQAJawvEypm4yFA%3D%3D&cmsv3=true&name=Josh+White" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=xDTAoILbVjon4us8XdP%2B8g%3D%3D&cmsv3=true&name=Joshua+Wyper" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=2Y8UcQ%2Fhm%2BnPzo6XiFxk8g%3D%3D&cmsv3=true&name=Judi+Jordan" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=0gwB7N%2B%2BxILI2ypKOx10tA%3D%3D&cmsv3=true&name=Kerry+Snyder" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=ZuwGJmwp8PT%2FB3EZa3RGEQ%3D%3D&cmsv3=true&name=Marco+Apanco" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=VMKpdfypk80CeALtZaOmiA%3D%3D&cmsv3=true&name=Mark+Kanitra" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=wBQJ2m2EeazYuwnko4Bb%2BA%3D%3D&cmsv3=true&name=Natalie+Ortiz" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=61AzABk%2BIT3m1rpSXBd1IQ%3D%3D&cmsv3=true&name=Nina+Afshar" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=WGs8Uomxa3tzwzDrnKqMqg%3D%3D&cmsv3=true&name=Pamela+Dunn" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=ZyH75qkmAmUgJN02ecevmQ%3D%3D&cmsv3=true&name=Rona+Gallagher" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=s8wzruyqgsCPs0chV4lSPg%3D%3D&cmsv3=true&name=William+Lunger" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=%2BsqTmRgmm53Awat%2BWeNJdg%3D%3D&cmsv3=true&name=Anthony+Dang" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=9Wwvwi4qU9OdseblKiOXBQ%3D%3D&cmsv3=true&name=Beatriz+Phipps%2C+MBA%2C+CPA" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=IIWk0gqdUA3imBJUhN33lg%3D%3D&cmsv3=true&name=Brian+Mayhall" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=hJjCQ0JD2QIfxZv%2BHusgiA%3D%3D&cmsv3=true&name=Elizabeth+Johnson" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=VBqlh5Ny0%2BCyJWOmMv%2FxBQ%3D%3D&cmsv3=true&name=Emanuel+Avina" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=6BB42AdR6aQrcRJi2HEOFg%3D%3D&cmsv3=true&name=Eric+P.+Francisconi" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=ZwxmYm6VvlVQu%2FGnirGahw%3D%3D&cmsv3=true&name=Fabio+Soto" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=XJEweGVTeOjdySt5FHtZDA%3D%3D&cmsv3=true&name=Jennifer+C.+Carter" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=eNRKgOdhJ%2FVj0GK9moL1Ww%3D%3D&cmsv3=true&name=Justin+Tipton" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=cBHaIUhttb9bEJ8TDRsdHQ%3D%3D&cmsv3=true&name=Liz+Apodaca" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=GO%2BFBuT%2F6162QSzymEcShA%3D%3D&cmsv3=true&name=Maria+Basler" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=9zfIIx%2FOGnansyu%2FqXfCcg%3D%3D&cmsv3=true&name=Martha+De+La+Torre" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=lZmNSaFGHhwptkBrcdUuRA%3D%3D&cmsv3=true&name=Michael+A.+Vasquez" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=EbztXAeu%2FBOJL3uwIgmUEg%3D%3D&cmsv3=true&name=Nick+Inchausti" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=8%2Fh4lHJsvoHVOIp9Lc49pQ%3D%3D&cmsv3=true&name=Raul+Mercado" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=PErhgG%2BchkMmEZw4Ey2cQg%3D%3D&cmsv3=true&name=Robert+Colangeli" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=UDHQLIk6aiWjkYxtE42trQ%3D%3D&cmsv3=true&name=Rosalia+Garcia" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=EMxnhbYlR3xVFXHJqtHP4w%3D%3D&cmsv3=true&name=Adam+Fomotor" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=Usimft0OccZCN5z52NbbUA%3D%3D&cmsv3=true&name=Anastasia+++Lander" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=vM%2FmjzS6P3dV74q1EonR8w%3D%3D&cmsv3=true&name=Anna+Ready" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=LvPR%2BHGxdmmSB6nK4IOmBQ%3D%3D&cmsv3=true&name=Brian+Young" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=aN5C%2FqPLohCXKBQbr0kGaw%3D%3D&cmsv3=true&name=C.+Khari+Knight" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=1QR5gSne4PwAsuD9eLOCjw%3D%3D&cmsv3=true&name=Carole+Markee" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=mnmQ%2B9dMJI7BFvAeck8zKg%3D%3D&cmsv3=true&name=Deborah+Kerr" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=VY%2BHnp%2BQ7Z2vMq5OvOwMvA%3D%3D&cmsv3=true&name=Derick+Roberts" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=Eybvcwk6GAokleh0Oan9BQ%3D%3D&cmsv3=true&name=Edward+Alberola" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=yZ5vQh5VC74nTZc9N%2BgTEA%3D%3D&cmsv3=true&name=Ely+Lun-Chial" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=CTTHOIW9yjDzmmak29yqwg%3D%3D&cmsv3=true&name=Eric+Padilla" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=C6xgJPb05yhBp9CNWY1Dlw%3D%3D&cmsv3=true&name=George+Varela" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=gTBxLCoJ4reOa%2FgKLU%2FGNw%3D%3D&cmsv3=true&name=Hector+Gonzalez" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=drcyDqY%2FGKVMqdIIgzFNMw%3D%3D&cmsv3=true&name=Jacqueline+Sobral" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=3TtX%2BKxFmhaUm2b38Z1QHw%3D%3D&cmsv3=true&name=Jared+Rau" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=UAKVAg4wLAs9kk7PmkXDVg%3D%3D&cmsv3=true&name=Jason+Clements" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=QwaPbkyNvrARl57xX2xbmA%3D%3D&cmsv3=true&name=Jenni+Peterson" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=tqRLFgftO7FOpJTqzXG3SQ%3D%3D&cmsv3=true&name=Jennifer+Oliveros" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=j6B%2Bn6LeozuTMEMhYdAw%2BQ%3D%3D&cmsv3=true&name=Jim+Moazez" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=NGvgzJYOFXX%2BdiLMvjkeQg%3D%3D&cmsv3=true&name=Joe+Gutierrez+Diaz" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=m6j%2B6REQL2KRVyMx9Cvr3Q%3D%3D&cmsv3=true&name=Jon+M.+Perez" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=VQpVht%2F6eEZxPxScDyUC8Q%3D%3D&cmsv3=true&name=Juan+Zapata" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=jyZgfoZ%2FqJSS4FFN7pfiyQ%3D%3D&cmsv3=true&name=Justin+Fellenz" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=c%2B94EDbhPYnthc2q%2B%2BPemw%3D%3D&cmsv3=true&name=Katie+Eldredge" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=v3EFDBroOHUQrlts%2BPjsVA%3D%3D&cmsv3=true&name=Lisa+Bryant" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=tdJCOXta5TIMW3UxYYOf3A%3D%3D&cmsv3=true&name=Luis+Echeveste" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=6qGA0PJmqeSVBAOpGo3X6g%3D%3D&cmsv3=true&name=Mark+Mackanic%2C+MBA%2C+CPA" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=Q22d7lELwi68Z0utmK6XxQ%3D%3D&cmsv3=true&name=Matthew+Schlau" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=fARSscc2jR5JdWuEuZadjA%3D%3D&cmsv3=true&name=Melissa+Delgado" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=WxTy1LhVuo5PjOdQleW3Sg%3D%3D&cmsv3=true&name=Michael+Kloka" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=YnHS0F%2B2ijS6cRLIFIXvkA%3D%3D&cmsv3=true&name=Sarah+Rodriguez" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=pSJLCks8JAR24ITKds6J2w%3D%3D&cmsv3=true&name=Susan+Klaren-Hatzenbuhler" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=bRINwO%2Fwpn9AryBYIXrPAw%3D%3D&cmsv3=true&name=Susan+Moore" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=miUbXH9azmZo511%2Bd7Q2Yg%3D%3D&cmsv3=true&name=Victor+Tinoco" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=Yp6b4PmKP50b5NpiuH6inw%3D%3D&cmsv3=true&name=Alice+Rodriguez" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=UWnTbE09mA7AOAnJlhk1tw%3D%3D&cmsv3=true&name=Bridget+Deason" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=wQF9L%2FfatfoAPo10xLeGMw%3D%3D&cmsv3=true&name=Donald+Hammond" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=a7v5GlEjL%2Bk%2BWbAv0FS1Sg%3D%3D&cmsv3=true&name=Gilbert+Garcia" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=UFUyDPYv7aPu3YIlRSPKuA%3D%3D&cmsv3=true&name=Ian+Adduru" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=l7sl%2Fs1pj4Rbcx5VKcaxxA%3D%3D&cmsv3=true&name=Julia+Burdick" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=yrcLxzQeCbDmHGXL9J4lzA%3D%3D&cmsv3=true&name=Kathy+Gardner" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=2JseD%2BUBRZheWgOy%2Bx9DgQ%3D%3D&cmsv3=true&name=Mariela+Leon" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=UrbOSra2XD0gowuo0kf%2Bbw%3D%3D&cmsv3=true&name=Rodrigo+Vasquez" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=qvfMWH1hDyJK3clYU358Wg%3D%3D&cmsv3=true&name=Sareta+Fernandes" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=EHav%2FylHvH5w%2FmffAyjGQg%3D%3D&cmsv3=true&name=Stephanie+Ann+Ortega" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=%2BriDM%2F6VcdsNam8k1vpQvA%3D%3D&cmsv3=true&name=Tamera+Wattenbarger" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=GmyIIWwK6qsnSvBFBK9EWg%3D%3D&cmsv3=true&name=Anita+Curtis+Reyes" \
        or memberURL == "https://socalbni.com/en-US/memberdetails?encryptedMemberId=iXsGPqIYqLJpCYv79wp2Pw%3D%3D&cmsv3=true&name=Brian+Armstrong":
            continue

        print(memberURL)
        driver.get(memberURL)
        time.sleep(7)
        memberPage = driver.page_source
        memberSoup = BeautifulSoup(memberPage, 'html.parser')
        memberDetailsSection = memberSoup.find('div', class_="col-xs-12 col-sm-12 col-md-3 col-lg-3 photoCol")
        if memberDetailsSection == None:
            Neme  = "NULL"
        else:
            Name = memberDetailsSection.find("h2").text

        contactDetails = memberSoup.find('div', class_="col-xs-12 col-sm-4 col-md-3 col-lg-3 contactCol")
        if contactDetails.a == None:
            continue
        memberSiteURL = contactDetails.a['href']
        if memberSiteURL == "http://www.CaroleOberto.com" \
        or memberSiteURL == "http://www.premiumtpc.com" \
        or memberSiteURL == "http://www.allcityheating-air.com" \
        or memberSiteURL == "http://www.rugitcleaning.com" \
        or memberSiteURL == "http://www.qacollision.com" \
        or memberSiteURL == "http://www.herbertwiggins.com" \
        or memberSiteURL == "http://www.lifeonthrive.com" \
        or memberSiteURL == "http://www.gnosistherapy.com" \
        or memberSiteURL == "http://www.sparkleanlaundry.com" \
        or memberSiteURL == "http://careerguy.com" \
        or memberSiteURL == "http://adt.com" \
        or memberSiteURL == "http://www.substrata.com" \
        or memberSiteURL == "http://cwalters.wearelegalshield.com" \
        or memberSiteURL == "http://www.seniorhelpers.com" \
        or memberSiteURL == "http://TicketGiant.com" \
        or memberSiteURL == "http://www.ahoy.dreamvacations.com" \
        or memberSiteURL == "http://www.eatonstaxservices.com" \
        or memberSiteURL == "http://www.coverlaw.com" \
        or memberSiteURL == "http://swolflegal.com" \
        or memberSiteURL == "http://www.agileient.com" \
        or memberSiteURL == "http://www.tritonair.net" \
        or memberSiteURL == "http://www.chainringbiz.com" \
        or memberSiteURL == "http://www.essentialhr.org" \
        or memberSiteURL == "http://www.harborwestinsurance.com" \
        or memberSiteURL == "http://coverlaw.com" \
        or memberSiteURL == "http://jlwinsurance.com" \
        or memberSiteURL == "http://www.katzfinancialLLC.com" \
        or memberSiteURL == "http://www.esopcorporateresources.com" \
        or memberSiteURL == "http://www.spinalvitality.com" \
        or memberSiteURL == "http://atozleakdetection.com" \
        or memberSiteURL == "http://accountabilities-oc.com" \
        or memberSiteURL == "http://www.GreenMapleLaw.com" \
        or memberSiteURL == "http://www.californiacreationz.com" \
        or memberSiteURL == "https://www.tandvllp.com/" \
        or memberSiteURL == "http://www.abccomputech.com" \
        or memberSiteURL == "http://www.voitenkowellness.com" \
        or memberSiteURL == "http://www.advancedplanningfinancial.com" \
        or memberSiteURL == "http://www.creativemktgservices.com" \
        or memberSiteURL == "http://www.homevestors.com" \
        or memberSiteURL == "http://www.samanthamark.nylagents.com" \
        or memberSiteURL == "http://www.harmony3productions.com" \
        or memberSiteURL == "http://www.pactechnologies.net" \
        or memberSiteURL == "https://www.mane-escape.com" \
        or memberSiteURL == "http://allegrabeachcities.com" \
        or memberSiteURL == "https://www.starcrestescrow.com" \
        or memberSiteURL == "http://www.lindseyiskierka.firstteam.com" \
        or memberSiteURL == "http://stonesalluslaw.com" \
        or memberSiteURL == "http://www.newerachiro.com" \
        or memberSiteURL == "http://www.toplineautorepair.com" \
        or memberSiteURL == "http://jacobsmalaw.net" \
        or memberSiteURL == "http://www.cutco.com" \
        or memberSiteURL == "http://www.thejasonspalding.com" \
        or memberSiteURL == "https://www.substrata.com" \
        or memberSiteURL == "http://www.seniorhelpers.com" \
        or memberSiteURL == "http://www.Premiertax.us.com" \
        or memberSiteURL == "http://www.thryv.com" \
        or memberSiteURL == "https://www.facebook.com/brizzo.net/" \
        or memberSiteURL == "http://Gettouchedmassage.com" \
        or memberSiteURL == "http://www.buyingtimellc.com" \
        or memberSiteURL == "http://www.claritydesignworks.com" \
        or memberSiteURL == "http://myuhcagent.com/debra.bernstein" \
        or memberSiteURL == "http://www.StamblerLaw.com" \
        or memberSiteURL == "http://www.tranquilpet.com" \
        or memberSiteURL == "http://www.JeffLewisLaw.com" \
        or memberSiteURL == "http://www.cihfc.com" \
        or memberSiteURL == "http://www.kimgirard.com" \
        or memberSiteURL == "http://www.konnitanaka.com" \
        or memberSiteURL == "http://www.allthingshealthy.org" \
        or memberSiteURL == "http://veteranair99.com" \
        or memberSiteURL == "http://www.shahshethlaw.com" \
        or memberSiteURL == "http://lifepartners.anallianceforlife.com/" \
        or memberSiteURL == "http://www.benefits4u2.com" \
        or memberSiteURL == "http://henrykimdmdpc.com/crowns" \
        or memberSiteURL == "http://www.seniorhelpers.com" \
        or memberSiteURL == "http://www.seniorhelpers.com/ut" \
        or memberSiteURL == "http://www.seniorhelpers.com/arcadia" \
        or memberSiteURL == "http://henrykimdmdpc.com"\
        or memberSiteURL == "http://www.WarmStoneMassage.net" \
        or memberSiteURL == "http://www.whpminc.com" \
        or memberSiteURL == "http://www.thriveloans.com":
            continue
        companyAddressDetails = memberSoup.find('div', class_="col-xs-12 col-sm-4 col-md-3 col-lg-3 companyCol")
        if companyAddressDetails.findChildren(['p'])[0].findChildren(['strong']) == None:
            companyName = "NULL"
        else:
            companyName = companyAddressDetails.findChildren(['p'])[0].findChildren(['strong'])[0].text
        if len(companyAddressDetails.findChildren(['p'])) < 2:
            Address = "NULL"
        else:
            Address = companyAddressDetails.findChildren(['p'])[1].findChildren(['strong'])[0].text
        if contactDetails.findChildren(['p'])[0].findChildren(['strong']) == None:
            phoneNUmber = "NULL"
        else:
            phoneNUmber = contactDetails.findChildren(['p'])[0].findChildren(['strong'])[0].find(['bdi']).text

        print(memberSiteURL)
        try:
            websitepage = get(memberSiteURL)
        except:
            continue
        time.sleep(2)
        websiteSoup = BeautifulSoup(websitepage.text, 'html.parser')
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z0-9\.\-+_]+", websitepage.text, re.I))
        AllInternalEmails.update(new_emails)
        getInternalLinks(websiteSoup, splitaddress(memberSiteURL)[0])
        AllInternalLinks.clear()
        print(AllInternalEmails)
        if len(AllInternalEmails) == 0:
            data_dict = {
                "BNIName": BNIName,
                "Name": Name,
                "Company Name" : companyName,
                "SiteURL": splitaddress(memberSiteURL)[0],
                "Address": Address,
                "Phone": phoneNUmber,
                "EmailAddress": "NULL"
            }
        else:
            data_dict = {
                "BNIName": BNIName,
                "Name": Name,
                "Company Name" : companyName,
                "SiteURL": splitaddress(memberSiteURL)[0],
                "Address": Address,
                "Phone": phoneNUmber,
                "EmailAddress": AllInternalEmails
            }
        search_results = pd.DataFrame()
        search_results = search_results.append([data_dict])
        df = pd.read_csv('../data/search_result/BNI.csv')
        if df.empty:
            timestamp = str(int(time.time()))
            filename = 'BNI.csv'
            outdir = '../data/search_result'
            if not os.path.exists(outdir):
                os.mkdir(outdir)

            full_file_path = os.path.join(outdir, filename)
            amount_results = len(search_results)

            if amount_results > 0:
                print("Stored total of " + str(amount_results)
                      + " search results in file "
                      + str(full_file_path))

                search_results.to_csv(full_file_path,
                                      index=False,
                                      columns=["BNIName","Name","Company Name","SiteURL","Address","Phone","EmailAddress"])
        else:
            search_results.to_csv('../data/search_result/BNI.csv',index=False, mode='a', header=False, columns=["BNIName","Name","Company Name","SiteURL","Address","Phone","EmailAddress"])
        AllInternalEmails.clear()