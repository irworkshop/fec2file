import csv 

from settings import *
from collections import OrderedDict

## this actually shouldn't be an ordered dict
## because it's only ordered by day in the original
## and so should be sorted by numeric filing number
## before processing 


infilepath = "headers/headers1.csv"

outfileheaders = ['filing_number', 'is_superseded', 'amended_by', 'last_amendment', 'report_number', 'filer_committee_id_number', 'form_type', 'date_signed', 'coverage_from_date', 'coverage_through_date', 'comment']
outfile =  open(AMENDED_HEADER_FILE, 'w')
writer = csv.DictWriter(outfile, fieldnames=outfileheaders, extrasaction='ignore')
writer.writeheader()


filing_amendment_dict = {}

with open(infilepath, 'r') as infile:
    dw = csv.DictReader(infile)


    for i, row in enumerate(dw):
        filing_number = row.get('filing_number', None)
        this_filing = {
            'amended_by':[], 
            'is_superseded':False, 
            'report_number':row['report_number'],
            'filer_committee_id_number':row['filer_committee_id_number'],
            'form_type':row['form_type'],
            'date_signed':row['date_signed'],
            'coverage_from_date':row['coverage_from_date'],
            'coverage_through_date':row['coverage_through_date'],
            'comment':row['comment']
            }
        amends = row.get('amends', None)
        if amends:
            #print("filing number %s amends %s" % (filing_number, amends))
            this_filing['amends'] = amends

        filing_amendment_dict[filing_number]=this_filing


# sort the filings
sorted_filings = OrderedDict(sorted(filing_amendment_dict.items(), key=lambda t: int(t[0])))

# save space? Maybe too  late...
filing_amendment_dict = {}

for filing in sorted_filings:
    
    amends = sorted_filings[filing].get('amends', None)
    if amends:
        try:
            sorted_filings[amends]

        except KeyError:
            #print("original out of set, ignoring %s" % amends)
            continue

        #print("Marking original %s as amended by %s" % (amends, filing))
        sorted_filings[amends]['is_superseded'] = True
        sorted_filings[amends]['last_amendment'] = filing

        prior_amendments = sorted_filings[amends]['amended_by']

        if prior_amendments:
            for prior_amendment in prior_amendments:
                sorted_filings[prior_amendment]['is_superseded'] = True
                sorted_filings[prior_amendment]['last_amendment'] = filing

                prior_amendment_amended_by_list = sorted_filings[prior_amendment]['amended_by']
                if filing not in prior_amendment_amended_by_list:
                    sorted_filings[prior_amendment]['amended_by'].append(filing)


        sorted_filings[amends]['amended_by'].append(filing)


for filing in sorted_filings:
    this_row = sorted_filings[filing]
    this_row['filing_number'] = filing
    writer.writerow(this_row)




