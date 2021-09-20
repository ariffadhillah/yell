import requests
from bs4 import BeautifulSoup
import csv

Searchterm = 'hotels'
location = 'london'

url = 'https://www.yell.com/ucs/UcsSearchAction.do?scrambleSeed=1218841838&keywords={}&location={}&pageNum='.format(Searchterm, location)

header = {
    'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
}

datas = []
for page in range(1, 3):
    req = requests.get(url+str(page), headers=header)
    soup = BeautifulSoup(req.text, 'html.parser')
    item = soup.findAll('div','row businessCapsule--mainRow')
    for it in item:
        name = it.find('h2', 'businessCapsule--name text-h2').text
        address = ''.join(it.find('span', {'itemprop':'address'}).text.strip().split('\n'))
        try : web = it.find('a', {'rel':'nofollow noopener'})['href'].replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0]
        except : web = ''
        try : telp = it.find('span' ,'business--telephoneNumber').text
        except: telp = ''
        image = it.find('div', 'col-sm-4 col-md-4 col-lg-5 businessCapsule--leftSide').find('img')['data-original']
        if 'http' not in image: image = 'https://www.yell.com{}'.format(image)
        datas.append([name, address, web, telp, image])

headerfile = ['Name', 'Address', 'Website', 'Phone Number', 'Image URL']
writer = csv.writer(open('results/{}_{}.csv'.format(Searchterm, location), 'w', newline=''))
writer.writerow(headerfile)
for d in datas: writer.writerow(d)
    
