import sys
import json
from traitlets import link
import os
from linkedin_api import Linkedin
import pandas as pd
import time
linkedin_api = Linkedin("mayurshin.vaghela43@gmail.com","password", refresh_cookies=True, debug=True)
comapany = linkedin_api.get_company(public_id="google")
comapanyid = int(comapany['url'].split('/')[len(comapany['url'].split('/')) - 1])
results = linkedin_api.search_people1(start=0,limit=10,current_company=comapanyid,regions="us:49",keywords="Software Engineer")
print(len(results))

search_results = pd.DataFrame()
for result in results:
        contact_info = linkedin_api.get_profile_contact_info(public_id=result['public_id'])
        profile = linkedin_api.get_profile(urn_id=result['urn_id'])
        data_firstname = profile['firstName']
        data_lastname = profile['lastName']
        data_url = "https://www.linkedin.com/in/%s" % \
                   result['public_id']
        data_location = profile['locationName']   if "locationName" in profile else " "
        data_country = profile['geoCountryName']   if "geoCountryName" in profile else " "
        data_jobpost = profile['headline']   if "headline" in profile else " "
        data_exp = ""
        for exp in profile['experience']:
            data_exp += "["
            data_exp += exp['locationName']  + "|" if "locationName" in exp else " "
            data_exp += exp['companyName'] + "|" if "companyName" in exp else " "
            data_exp += str(exp['timePeriod']['startDate']['month']) + " " if "timePeriod" in exp and "startDate" in exp['timePeriod'] and "month" in exp['timePeriod']['startDate']  else " "
            data_exp += str(exp['timePeriod']['startDate']['year']) + "|" if "timePeriod" in exp and "startDate" in exp['timePeriod'] and "year" in exp['timePeriod']['startDate']  else " "
            data_exp += str(exp['timePeriod']['endDate']['month']) + " " if "timePeriod" in exp and "endDate" in exp['timePeriod'] and "month" in exp['timePeriod']['endDate'] else " "
            data_exp += str(exp['timePeriod']['endDate']['year']) + "|" if "timePeriod" in exp and "endDate" in exp['timePeriod'] and "year" in exp['timePeriod']['endDate'] else " "
            data_exp += exp['title'] if "title" in exp else " "
            data_exp +=  "]"

        data_skill = ""
        for sk in profile['skills']:
            data_skill += "[" + sk['name'] + "]" if "name" in sk else " "
        data_edu = ""
        for education in profile['education']:
            data_edu += "["
            data_edu += education['schoolName'] + "|" if "schoolName" in education else " "   + education['degreeName'] + "|" if "degreeName" in education else " "  + str(education['timePeriod']['startDate']['year']) + "|" if "timePeriod" in education and "startDate" in education['timePeriod']  else " "   +str(education['timePeriod']['endDate']['year']) if "timePeriod" in education and "endDate" in education['timePeriod']   else " "
            data_edu += "]"

        data_email = contact_info['email_address']
        data_dict = {
            "name": data_firstname + " " + data_lastname,
            "occupation": data_jobpost,
            "email": data_email,
            "location": data_location,
            "country": data_country,
            "experience": data_exp,
            "skills": data_skill,
            "education": data_edu,
            "url": data_url
            # "pic": data_picture  # Doesn't work
        }
        
        search_results = search_results.append([data_dict])

timestamp = str(int(time.time()))
filename = timestamp + '.csv'
outdir = './data/search_result'
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
                          columns=["name", "occupation", "email",
                                   "location", "country", "experience", "skills", "education", "url"])

else:
    print("Zero valid search results! Increase amount to scrape in config")
    exit(0)
