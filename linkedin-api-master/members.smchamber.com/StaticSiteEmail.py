from requests import get
from requests import request
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time

global i
global internalLinks
AllInternalLinks = set()
global AllInternalEmails
AllInternalEmails = set()
search_results = pd.DataFrame()

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

staticSiteURL = "https://buyingtimellc.com"
websitepage = get(staticSiteURL)
websitepage_soup = BeautifulSoup(websitepage.text, 'html.parser')
new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z0-9\.\-+_]+", websitepage.text, re.I))
AllInternalEmails.update(new_emails)
getInternalLinks(websitepage_soup, splitaddress(staticSiteURL)[0])
AllInternalLinks.clear()
print(AllInternalEmails)
data_dict = {
    "SiteURL": splitaddress(staticSiteURL)[0],
    "EmailAddress": AllInternalEmails
}
search_results = search_results.append([data_dict])

timestamp = str(int(time.time()))
address = splitaddress(staticSiteURL)[0]
filename = address + 'email.csv'
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
                          columns=["SiteURL", "EmailAddress"])

AllInternalEmails.clear()
