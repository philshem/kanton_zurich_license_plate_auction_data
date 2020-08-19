from glob import glob
import os
import pandas as pd
from pandas.io.json import json_normalize

'''
takes individual json files from folder 'data/' and writes to one big all.csv
'''

def main():

	# get all matching files
	all_json = glob('data'+os.sep+'*.json')
	#print(all_json)

	all_df = []
	for f in all_json:
		tmp = pd.read_json(f).T
		
		# working on unpacking bids
		# for now, they are excluded from csv		
		#tmp2 = pd.json_normalize(tmp["bids"]).T

		del tmp['bids']

		all_df.append(tmp)
		#break # debuggin

	# combine all dataframes from each json file
	df = pd.concat(all_df)

	# clean up dates
	# auction_end 19.08.2020 19:00
	df['auction_end'] = pd.to_datetime(df['auction_end'], format = '%d.%m.%Y %H:%M')

	# runtime 2020-08-19T12:04:43.027392
	df['runtime'] = pd.to_datetime(df['runtime'], format = '%Y-%m-%dT%H:%M:%S.%f')

	# reset index to print it in csv
	df.reset_index(inplace=True)
	df = df.rename(columns={'index':'plate'})
	df.to_csv('all.csv',index=False)
	#print(df)

if __name__ == "__main__":
	main()