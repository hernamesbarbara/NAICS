import numpy as np
import pandas as pd
import string
import pprint as pp

pd.set_printoptions(max_columns=10, max_rows=50)

def snake(s):
    return "".join([c for c in s if c 
    				not in string.punctuation]).lower().replace(' ', '_')

def cleanHeader(s, n_chars=16):
	return snake(s)[:n_chars]

def readXls(xls):
	dirname = './data/raw/'
	wb = pd.ExcelFile(dirname + xls['name'])
	if xls['sheetname'] not in wb.sheet_names: return

	frame = wb.parse(xls['sheetname'], header=xls['header'], skiprows=xls['skiprows'], skip_footer=xls['skip_footer'])
	frame.columns = map(snake, frame.columns)
	frame['filename'] = xls['name']
	
	return frame

def getColumns(xls_list):
	colnames = []
	for xls in workbooks:
		frame = readXls(xls)
		colnames.append({xls['name']: map(cleanHeader, frame.columns)})
	return colnames

workbooks = [ {'name': '2002_NAICS_to_1987_SIC.xls', 'sheetname': 'Sheet1', 'header': 0, 'skiprows': 0, 'skip_footer': 1 } ,
			  {'name': '2002_NAICS_to_1997_NAICS.xls', 'sheetname': 'Concordance 23 US NoD', 'header': 0, 'skiprows': 0, 'skip_footer': 1 } ,
			  {'name': '2007_to_2002_NAICS.xls', 'sheetname': '07 to 02 NAICS U.S.', 'header': 2, 'skiprows': 0, 'skip_footer': 0 } ,
			  {'name': '2012_to_2007_NAICS.xls', 'sheetname': '2012 to 2007 NAICS U.S.', 'header': 2, 'skiprows': 1, 'skip_footer': 0 } ]


wbs = getColumns(workbooks)
pp.pprint(wbs)

filenames = [name for wb in wbs for name in wb.keys()]

split_names = map(lambda x: x.split('_'), filenames)

split_names = [ sorted(map(int, filter(lambda x: x.isdigit(), part_list)))
				for part_list in split_names ]

years = zip(filenames, split_names)

years =  [{'filename': k, 'start': v[0], 'end': v[1]} for k, v in years]


years_df = pd.DataFrame(years)

for wb in workbooks:
	print 'reading %s: ' % wb['name']
	df = readXls(wb)

	print 'merging %s with years_df' % wb['name']
	df = pd.merge(df, years_df)

	print 'writing to csv file: %s' % df.filename.unique()[0] + ".txt"
	df.to_csv('./data/cleaned/' + df.filename.unique()[0] + ".txt", sep="|", encoding='utf-8')

