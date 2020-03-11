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

BNI_List = html_soup.find('table', class_="table table-hover listtables dataTable no-footer dtr-inline")
rows = BNI_List.findChildren(['tr'])
for row in rows:
    if row.a == None:
        continue
    memberListURL = "https://socalbni.com/en-US/" + row.a['href']
    BNIName = row.a.text
    if memberListURL == "https://socalbni.com/en-US/chapterdetail?chapterId=guO6Z5InT4YuNqtXbNMbjg%3D%3D&name=BNI+Pipeline+BNI" \
    or memberListURL == "https://socalbni.com/en-US/chapterdetail?chapterId=cQ037zlwHW3OAPOh3aAIUg%3D%3D&name=BNI+BNI+South+Bay+Business+Alliance" \
    or memberListURL == "https://socalbni.com/en-US/chapterdetail?chapterId=ybWMiJGXNfkPfLrulbavxQ%3D%3D&name=BNI+BNI+Rock+Solid+Referrals":
        continue
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