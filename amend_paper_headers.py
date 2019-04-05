import csv 

from settings import *
from collections import OrderedDict

import os



infilepath = "headers/paper_headers_raw.csv"
print("Reading filing header data from file %s" % infilepath)


outfileheaders = ['filing_number', 'file_size', 'file_linecount', 'size_ratio', 'line_ratio', 'is_original', 'most_recent', 'is_amendment', 'original_id', 'filer_committee_id_number', 'form_type', 'received_date', 'batch_number', 'date_signed', 'coverage_from_date', 'coverage_through_date']
outfile =  open(AMENDED_PAPER_HEADER_FILE, 'w')
print("Writing output to %s" % AMENDED_PAPER_HEADER_FILE)
writer = csv.DictWriter(outfile, fieldnames=outfileheaders, extrasaction='ignore')
writer.writeheader()

filing_list = []

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
    if filing['form_type'].startswith("F3") or filing['form_type'].startswith("F13"):

        from_date = filing['coverage_from_date'][:10]
        through_date = filing['coverage_through_date'][:10]
        hash_key = filing_key % (filing['filer_committee_id_number'], from_date, through_date)
        
        sorted_filings[i]['most_recent'] = True

        try:
            # is there already an earlier filing entered for this key? 
            original_filing = original_filing_dict[hash_key]
            # if one exists, is it a full replacement or not? 
            # if it's not a full replacement, ignore it. 
            # this means we ignore the effects of minor amendments
            # in practice this is usually because they made a few mistakes
            # or got the summary totals wrong


            original_id = original_filing['filing_number']

            # file size, in bytes
            size_ratio = (0.0 + int(sorted_filings[i]['file_size'])) / int(original_filing['file_size'])
            # number of lines of files
            # I think lengthy memo text fields that are added in explanation / removed
            # contributes to the weirder size changes
            line_ratio = (0.0 + int(sorted_filings[i]['file_linecount'])) / int(original_filing['file_linecount'])

            sorted_filings[i]['size_ratio'] = size_ratio
            sorted_filings[i]['line_ratio'] = line_ratio



            if line_ratio > 0.8:
                # it's a full replacement mark it as such
                print("Found full replacement for %s to be %s" % (original_id, filing['filing_number']))

                sorted_filings[i]['original_id'] = original_id
                sorted_filings[i]['is_original'] = False
                sorted_filings[i]['is_amendment'] = True
                sorted_filings[i]['most_recent'] = True


                original_filing_dict[hash_key]['most_recent'] = False

            elif line_ratio < 0.65 and line_ratio > 0.5:
                print("line ratio of %s for %s" % (line_ratio, sorted_filings[i]))

            else:

                sorted_filings[i]['original_id'] = original_id
                sorted_filings[i]['is_original'] = False
                sorted_filings[i]['is_amendment'] = True
                sorted_filings[i]['most_recent'] = False



        except KeyError:


            original_filing_dict[hash_key] = filing

            sorted_filings[i]['is_original'] = True
            sorted_filings[i]['is_amendment'] = False
            sorted_filings[i]['original_id'] = filing['filing_number']



for filing in sorted_filings:
     writer.writerow(filing)




