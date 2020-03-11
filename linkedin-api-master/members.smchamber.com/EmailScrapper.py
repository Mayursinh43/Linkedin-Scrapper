from requests import get
from requests import request
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time


url = 'http://members.smchamber.com/list/ql/advertising-media-1?q=&c=&sa=False'
response = get(url)
global i
global internalLinks
AllInternalLinks = set()
global AllInternalEmails
AllInternalEmails = set()

html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)

company_container = html_soup.find_all('div', class_="gz-list-card-wrapper col-sm-6 col-md-4")

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


for company in company_container:
    siteresponse = get(company.a['href'])
    html_soup1 = BeautifulSoup(siteresponse.text, 'html.parser')
    websitecontainer = html_soup1.find_all('li', class_="list-group-item gz-card-website")
    try:
        ChamberName = html_soup1.find_all('h1', class_="gz-pagetitle")[0].text
        PhoneNumber = html_soup1.find_all('li', class_="list-group-item gz-card-phone")[0].text
        Address = html_soup1.find_all("span", class_="gz-street-address")[0].text +  html_soup1.find_all("span", class_="gz-address-city")[0].text + html_soup1.find_all(attrs = {"itemprop": "addressRegion"})[0].text + html_soup1.find_all(attrs = {"itemprop": "postalCode"})[0].text
    except IndexError:
        Address = "NULL"

    for websitecontainer_1 in websitecontainer:
        print(websitecontainer_1.a['href'])
        if websitecontainer_1.a['href'] == "http://www.jci worldwide inc.com" \
        or websitecontainer_1.a['href'] == 'http://www.elevatepublicaffairs.com' \
        or websitecontainer_1.a['href'] == "http://www.lavecchiacucina.com" \
        or websitecontainer_1.a['href'] == "http://www.becrystalclear.com" \
        or websitecontainer_1.a['href'] == "http://www.themiddleland.com" \
        or websitecontainer_1.a['href'] == "http://www.chelseakwoka.com" \
        or websitecontainer_1.a['href'] == "http://www.drivetrafficmedia.net" \
        or websitecontainer_1.a['href'] == "http://www.elcholo.com" \
        or websitecontainer_1.a['href'] == "http://www.bubbagump.com" \
        or websitecontainer_1.a['href'] == "http://www.tiato.com" \
        or websitecontainer_1.a['href'] == "http://www.sparkrise.com" \
        or websitecontainer_1.a['href'] == "http://www.talk2tish.com" \
        or websitecontainer_1.a['href'] == "http://www.41oceanclub.com" \
        or websitecontainer_1.a['href'] == "http://www.linkedin.com" \
        or websitecontainer_1.a['href'] == "http://www.recasher.com" \
        or websitecontainer_1.a['href'] == "http://www.flashtrackdigital.com" \
        or websitecontainer_1.a['href'] == "http://www.kaleomarketing.com" \
        or websitecontainer_1.a['href'] == "http://www.watergrill.com" \
        or websitecontainer_1.a['href'] == "http://annenbergbeachhouse.com/contact.aspx" \
        or websitecontainer_1.a['href'] == "http://www.lasocialkarma.com" \
        or websitecontainer_1.a['href'] == "http://www.brandbrasserie.com" \
        or websitecontainer_1.a['href'] == "http://www.smdp.com" \
        or websitecontainer_1.a['href'] == "http://www.1212santamonica.com" \
        or websitecontainer_1.a['href'] == "http://XrossWorld.net" \
        or websitecontainer_1.a['href'] == "http://www.sweetvirtues.com" \
        or websitecontainer_1.a['href'] == "http://www.energyupgradeca.org" \
        or websitecontainer_1.a['href'] == "http://www.belairbranding.com" \
        or websitecontainer_1.a['href'] == "http://www.themisfitbar.com" \
        or websitecontainer_1.a['href'] == "http://www.barkerhangar.com" \
        or websitecontainer_1.a['href'] == "http://www.shuttersonthebeach.com" \
        or websitecontainer_1.a['href'] == "http://www.mochabearmarketing.com" \
        or websitecontainer_1.a['href'] == "http://www.processgreen.com" \
        or websitecontainer_1.a['href'] == "http://sunriseseniorliving.com" \
        or websitecontainer_1.a['href'] == "http://www.fluencebrands.com" \
        or websitecontainer_1.a['href'] == "http://www.fairmont.com" \
        or websitecontainer_1.a['href'] == "http://www.c-istudios.com":
            continue
        websitepage = get(websitecontainer_1.a['href'])
        websitepage_soup = BeautifulSoup(websitepage.text, 'html.parser')
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z0-9\.\-+_]+", websitepage.text, re.I))
        AllInternalEmails.update(new_emails)
        getInternalLinks(websitepage_soup, splitaddress(websitecontainer_1.a['href'])[0])
        AllInternalLinks.clear()
        print(AllInternalEmails)
        if len(AllInternalEmails) == 0:
            data_dict = {
                "SiteURL": splitaddress(websitecontainer_1.a['href'])[0],
                "Chamber Name": ChamberName,
                "PhoneNumber": PhoneNumber,
                "Address": Address,
                "EmailAddress": "NULL"
            }
        else:
            data_dict = {
                "SiteURL": splitaddress(websitecontainer_1.a['href'])[0],
                "Chamber Name": ChamberName,
                "PhoneNumber": PhoneNumber,
                "Address": Address,
                "EmailAddress": AllInternalEmails
            }
        search_results = pd.DataFrame()
        search_results = search_results.append([data_dict])

        df = pd.read_csv('../data/search_result/members.smchamber.com_email.csv')
        if df.empty:
            timestamp = str(int(time.time()))
            filename = 'members.smchamber.com_email.csv'
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
                                      columns=["SiteURL","Chamber Name","PhoneNumber","Address","EmailAddress"])
        else:
            search_results.to_csv('../data/search_result/members.smchamber.com_email.csv',index=False, mode='a', header=False, columns=["SiteURL","Chamber Name","PhoneNumber","Address","EmailAddress"])
        AllInternalEmails.clear()