""" reads from header excerpts """

import csv
import os
from datetime import datetime

from settings import AMENDED_HEADER_FILE, RAW_ELECTRONIC_DIR
from collections import Counter

import fecfile

from schedule_headers import *
from settings import SCHEDULE_A_OUTFILE, SCHEDULE_B_OUTFILE

# process these
main_forms = ['F3X', 'F3', 'F3P']

# file on skeds a, b, c, d, e
# F3X - unaffiliated committee
# F3 - candidate committee
# F3P - presidential committee


# these use "normal" skeds
extra_forms = ['F3L', 'F4']
# F3L - lobbyist bundled contributions, might need to be saved elsewhere
# F4 - convention committee


# would like to add these but they use weird skeds
other_forms = [ 'F5', 'F7', 'F13'] 
# F5 noncommittee filers, uses F56/57 
# F7 communication costs, uses F76
# F13 inaugural committee, uses F132/F133

#legal_skeds = ['A', 'B', 'C', 'D']

legal_skeds = ['A', 'B']

# To really do sked E we gotta include F57, from the F5's



schedule_writer = {
    'A':{
        'headers': SCHEDULE_A_HEADERS,
        'outfile': SCHEDULE_A_OUTFILE,
    },
    'B':{
        'headers': SCHEDULE_B_HEADERS,
        'outfile': SCHEDULE_B_OUTFILE,
    },
}

def readfile(path_to_file, schedule_writer):
    filename = os.path.basename(path_to_file)
    filenumber = int(filename.replace(".fec", ""))
    #print("reading filing %s from %s" % (filenumber, path_to_file))

    formtypecount = Counter()

    version = None
    with open(path_to_file, encoding = "ISO-8859-1") as file:
        linecount = 0
        for line in file:
            linecount+=1
            if version is None:
                results = fecfile.parse_header(line)
                header = results[0]
                version = results[1]

            else:
                parsed = fecfile.parse_line(line, version)
                if not parsed:
                    pass
                    #print("** not parsed %s" % line)
                else:   
                    # count the form type, if given
                    try:
                        formtypecount.update({parsed['form_type']:1})
                    except KeyError:
                        continue

                    form_type = parsed['form_type'].upper()

                    parsed['filing_number'] = filenumber
                    parsed['line_sequence'] = linecount

                    if form_type.startswith("SA"):
                        schedule_writer['A']['writer'].writerow(parsed)

                    if form_type.startswith("SB"):
                        schedule_writer['B']['writer'].writerow(parsed)


                
                #print("%s %s" % (linecount, parsed))

    #print(formtypecount)


if __name__ == '__main__':




    build_hash = True

    if build_hash: 

        # hash the most recent filings here,
        # we'll run through all of them and use 
        # this to check if they should be processed 
        live_filing_list = {}
        start = datetime.now()
        print("Building a hash of files to process... ")
        reader = csv.DictReader(open(AMENDED_HEADER_FILE, 'r'))
        count = {}
        max = 0
        included = 0
        for i,row in enumerate(reader):
            raw_form_type = row['form_type']
            form_type = raw_form_type.rstrip('ANT')
            max=i

            if form_type in main_forms and row['is_superseded'] == 'False':
                #print("Got form to process %s %s" % (row['filing_number'], row['form_type']))
                live_filing_list[row['filing_number']] = row['form_type']
                included += 1


        hash_done = datetime.now()
        print("Read %s rows and hashed %s in %s" % (max, included, hash_done-start))


    # set up the writers
    for sked in legal_skeds:
        outfile = schedule_writer[sked]['outfile']
        headers = schedule_writer[sked]['headers']

        schedule_writer[sked]['writer'] = csv.DictWriter(open(outfile, 'w'), fieldnames=headers, extrasaction='ignore')
        schedule_writer[sked]['writer'].writeheader()

    # num processed 
    num_processed = 0
    NOTIFY = 100
    # Walk the electronic dir and find files. 
    for root, dirs, files in os.walk(RAW_ELECTRONIC_DIR):
        path = root.split(os.sep)
        for file in files:
            if file.endswith(".fec"):
                filenumber = file.split(".")[0]

                if build_hash:
                    try:
                        live_filing_list[filenumber]
                    except KeyError:
                        continue


                    path_list = path + [file]
                    filepath = os.path.join(*path_list) # unpack list to args with *
                    readfile(filepath, schedule_writer)
                    num_processed += 1
                    if num_processed % NOTIFY == 0:
                        print("processed = %s" % num_processed)

                