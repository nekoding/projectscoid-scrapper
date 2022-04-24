import requests
from bs4 import BeautifulSoup
import os
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0',
    'X-Requested-With': 'XMLHttpRequest'
}

def extract_data(data):
    title = data.find('h2').text.strip()
    link = data.find('a')['href'].strip()
    budget = data.select_one('strong:nth-of-type(1)').next_sibling.text.strip()
    published = data.select_one('strong:nth-of-type(2)').next_sibling.text.strip()
    deadline = data.select_one('strong:nth-of-type(3)').next_sibling.text.strip()
    status = data.find('span', { 'class': 'label-info' })
    total_bid = status.find_next_sibling().find_next_sibling().next_sibling.text.strip()

    return {
        'title': title,
        'link': link,
        'budget': budget,
        'published': published,
        'deadline': deadline,
        'status': status.text.strip(),
        'total_bid': int(total_bid)
    }


max_page = 21
filename = "data/data.json"
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w") as outfile:
    
    results = []
    for i in range(1, max_page):
        r = requests.get('https://projects.co.id/public/browse_projects/listing?page='+ str(i) +'&ajax=1', headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        projects = soup.select('div.col-md-10.align-left')

        for data in projects:
            results.append(extract_data(data))

        print('page' + str(i) + ' DONE')
    json.dump(results, outfile)
        