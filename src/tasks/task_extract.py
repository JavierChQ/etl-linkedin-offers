import requests
from bs4 import BeautifulSoup
from prefect import task

URL = "https://www.linkedin.com/jobs/search/?currentJobId=4122411676&f_TPR=r86400&keywords="

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

skill = "Python"

@task(name="Extraer datos")
def task_extract():
    url = requests.get(URL+skill,headers=HEADERS)

    if(url.status_code == 200):
        html = BeautifulSoup(url.text,'html.parser')
        ul_offers = html.find('ul',{'class':'jobs-search__results-list'})
        li_offers = ul_offers.find_all('li')

        offer_list = []
        
        for offer in li_offers:
            offer_title = offer.find('h3',{'class':'base-search-card__title'})
            offer_location = offer.find('span',{'class':'job-search-card__location'})
            offer_url = offer.find('a')
            offer_company = offer.find('a',{'class':'hidden-nested-link'})
            offer_date = offer.find('time',{'class':'job-search-card__listdate'})
            
            title = offer_title.get_text().strip() if offer_title else ''
            location = offer_location.get_text().strip() if offer_location else ''
            url_value = offer_url['href'].strip() if offer_url else ''
            company = offer_company.get_text().strip() if offer_company else ''
            date_value = offer_date['datetime'].strip() if offer_date else None
            offer_list.append((title,location,company,date_value,url_value,skill))
            
        return offer_list
    else:
        print(f"error : {url.status_code}")