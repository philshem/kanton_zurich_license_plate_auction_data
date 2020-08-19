import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from datetime import datetime
import json
import os
import pandas as pd

'''
scrapes the auction price for popular Kanton Zürich license plates
'''

url = 'https://www.auktion.stva.zh.ch/'

def main():

	runtime = datetime.now()

	html = requests.get(url).content

	soup = BeautifulSoup(html, "html.parser")

	plates = soup.find("div",attrs={"class":"text-center","id":"plates"})

	plates = plates.find_all("div",attrs={"class":"plate col-sm-4"})

	d = defaultdict(list)

	for plate in plates:
	
		# get url for bids page
		href = plate.find('a')['href']#,attrs='href')
		if href.startswith('/'):
			href = href[1:]
		href = url + href

		# request individual bids page
		df_bids = pd.read_html(href)
		df_bids = df_bids[-1]
		
		# cleanup of bids dataframe
		df_bids.columns = ['bidder','price','bid_date']
		df_bids['bid_date'] = pd.to_datetime(df_bids['bid_date'], format = '%d.%m.%Y um %H:%M:%S')
		df_bids['price'] = df_bids['price'].str.replace('CHF','').str.replace('\'','').str.strip().astype(int)

		# reverse index, so early bids start at 0
		df_bids.sort_values('bid_date',inplace=True)
		df_bids.reset_index(inplace=True)
		del df_bids['index']

		# convert df to json of bids per auction
		bids = df_bids.T.to_json(index='columns', date_format = 'iso')

		# get values from html
		tag = plate.find("img",attrs={"alt":"ZH"})['title']
		number = int(tag.split()[-1].strip())
		kanton = tag.split()[0].strip()
		price = int(plate.text.split('CHF')[0].split()[-1].replace('\'','').strip())
		auction_end = plate.text.split('am:')[-1].strip()

		d[tag] = {'kanton': kanton, 'number' : number, 'price' : price, 'auction_end' : auction_end, 'href': href, 'bids' : json.loads(bids), 'runtime' : runtime.isoformat()}

		#break

	with open('data'+os.sep+runtime.strftime("%Y%m%d_%H%M%S")+'.json','w') as fp:
		json.dump(d,fp, indent=2)


if __name__ == "__main__":
	main()