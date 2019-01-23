import csv 

from settings import *
from collections import OrderedDict

import os


## this actually shouldn't be an ordered dict
## because it's only ordered by day in the original
## and so should be sorted by numeric filing number
## before processing 


infilepath = "headers/paper_headers_raw.csv"

outfileheaders = ['filing_number', 'file_size', 'file_linecount', 'size_ratio', 'line_ratio', 'is_original', 'is_amendment', 'original_id', 'filer_committee_id_number', 'form_type', 'received_date', 'batch_number', 'date_signed', 'coverage_from_date', 'coverage_through_date']
outfile =  open(AMENDED_PAPER_HEADER_FILE, 'w')
writer = csv.DictWriter(outfile, fieldnames=outfileheaders, extrasaction='ignore')
writer.writeheader()

filing_list = []
print("Reading filing header data from file %s" % infilepath)
with open(infilepath, 'r') as infile:
    dw = csv.DictReader(infile)


    for i, row in enumerate(dw):
        filing_number = row.get('filing_number', None)
        this_filing = {
            'filer_committee_id_number':row['filer_committee_id_number'],
            'form_type':row['form_type'],
            'date_signed':row['date_signed'],
            'received_date':row['received_date'],
            'coverage_from_date':row['coverage_from_date'],
            'coverage_through_date':row['coverage_through_date'],
            'batch_number':row['batch_number'],
            'filing_number':filing_number,
            'file_size':row['file_size'],
            'file_linecount':row['file_linecount'],

            }
        filing_list.append(this_filing)



# sort the filings
sorted_filings = sorted(filing_list, key=lambda t: int(t['filing_number']))

filing_key = "%s:%s:%s" 


original_filing_dict = {}

for i, filing in enumerate(sorted_filings):
    #print("handling filing %s" % filing)
    if filing['form_type'].startswith("F3"):


        from_date = filing['coverage_from_date'][:10]
        through_date = filing['coverage_through_date'][:10]
        hash_key = filing_key % (filing['filer_committee_id_number'], from_date, through_date)
        try:
            original_filing = original_filing_dict[hash_key]
            original_id = original_filing['filing_number']
            sorted_filings[i]['is_original'] = False
            sorted_filings[i]['is_amendment'] = True
            sorted_filings[i]['original_id'] = original_id


            sorted_filings[i]['size_ratio'] = (0.0 + sorted_filings[i]['file_size']) / original_filing['file_size']
            sorted_filings[i]['line_ratio'] = (0.0 + sorted_filings[i]['file_linecount']) / original_filing['file_linecount']



        except KeyError:


            original_filing_dict[hash_key] = filing

            sorted_filings[i]['is_original'] = True
            sorted_filings[i]['is_amendment'] = False
            sorted_filings[i]['original_id'] = filing['filing_number']

            sorted_filings[i]['size_ratio'] = 1
            sorted_filings[i]['line_ratio'] = 1





for filing in sorted_filings:
     writer.writerow(filing)




