import os
import pandas as pd

'''
reads historical winning bids, last 60 days, appends historical.csv
'''

def main():

	csv_path = 'historical.csv'

	url = 'https://www.auktion.stva.zh.ch/order/altpast'
	df = pd.read_html(url)
	df = df[0]

	print(len(df),'new rows in html')


	# cleanup of table data	
	df['Preis'] = df['Preis'].str.replace('\'','').str.strip().astype(int)
	df['Ende'] = pd.to_datetime(df['Ende'], format = '%d.%m.%Y %H:%M')

	# read old/existing file
	try:
		old = pd.read_csv(csv_path)
		df = pd.concat(old,df)
	except:
		pass

	# it's highly likely to have duplicates
	df.drop_duplicates(subset=None, keep='first', inplace=True)

	# write to same csv
	df.to_csv(csv_path, index=False)

	print(len(df),'total rows in csv')

if __name__ == "__main__":
	main()