import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

def scrap_data():
    #in below there is a common URL named as source_url
    source_url = 'https://www.timesjobs.com/candidate/job-search.html?from=submit&searchType=Home_Search&luceneResultSize=25&postWeek=60&cboPresFuncArea=35&pDate=Y&sequence='
    #using loop function for adding number of pages to source_url
    all_urls = []
    for val in range(1,41):
        all_urls.append(source_url+str(val))

    all_job_list = []    #Empty list created to insert list of dictionary
    count=0           #for serialzation
    # Using loop to fetch all urls data.
    for url in all_urls:
        all_urls_data = requests.get(url).text              #used requests to import all data from url page
        all_soup_data = BeautifulSoup(all_urls_data,'lxml')           #changes the data type from 'str' to 'BeautifulSoup' lxml format.
        all_box_data = all_soup_data.find_all('li',class_='clearfix job-bx wht-shd-bx')    #To find all box data of all urls data.
        
        # Using for loop to get data of every single box one by one.
        for item in all_box_data:
            job_title = item.find('a').text
            company = item.find('h3',class_='joblist-comp-name').text
            company_name = company.replace('(More Jobs)','')
            exp = item.find('li').text
            experience = exp.replace('card_travel','')
            loc = item.find('span').text
            location = loc.replace('(More Jobs)','')
            description = item.find('ul',class_='list-job-dtl clearfix').text
            job_description = description.replace('Job Description:','')
            key_skills = item.find('span',class_='srp-skills').text
            key_skills_new = key_skills.lstrip()
            job_url = item.find('a')['href']
            count = count + 1
            # Following process to make dictionary for every box data.
            all_job_info = {
                'Serial_No.':count,
                'Job_title':job_title,
                'Company_name':company_name,
                'Experience':experience,
                'Location':location,
                'Job_description':job_description,
                'Key_skills':key_skills_new,
                'Job_Detail_link':job_url
                }

            all_job_list.append(all_job_info)    # inserts every single dictionary data to all_job_list.


    df1 = pd.DataFrame(all_job_list)        #creates a data structure with rows and columns with all existing data.
    df1.to_excel('Times_Jobs.xlsx')         #creates an Excel file of given data.

scrap_data()            #calling the function.