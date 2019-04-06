""" reads from header excerpts """

import csv
import os
from datetime import datetime

from settings import AMENDED_HEADER_FILE, RAW_ELECTRONIC_DIR
from collections import Counter, OrderedDict

import fecfile

from schedule_headers import *
from settings import SCHEDULE_A_OUTFILE, SCHEDULE_B_OUTFILE

# process these
main_forms = ['F3X', 'F3', 'F3P', 'F13']

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

legal_skeds = ['A', 'B','F132']

# To really do sked E we gotta include F57, from the F5's

YEARS = [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]


schedule_writer = {
    'A':{
        'headers': SCHEDULE_A_HEADERS,
        'outfile': SCHEDULE_A_OUTFILE,
    },
    'B':{
        'headers': SCHEDULE_B_HEADERS,
        'outfile': SCHEDULE_B_OUTFILE,
    },
    'F132':{
        'headers':SCHEDULE_A_HEADERS,
        'outfile':SCHEDULE_F132_OUTFILE
    }
}

def readfile(path_to_file, schedule_writer, year):
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
                try:
                    parsed = fecfile.parse_line(line, version)
                except fecfile.cache.FecParserMissingMappingError as e:
                    print("error in %s line %s: %s" % (filenumber, linecount, e))
                    continue
                if not parsed:
                    pass
                    print("** not parsed %s" % line)
                else:   
                    # count the form type, if given
                    try:
                        formtypecount.update({parsed['form_type'].upper():1})
                    except KeyError:
                        continue

                    form_type = parsed['form_type'].upper()

                    parsed['filing_number'] = filenumber
                    parsed['line_sequence'] = linecount


                    print("\t Form type is %s" % form_type)

                    if form_type.startswith("SA"):
                        schedule_writer['A'][year]['writer'].writerow(parsed)

                    elif form_type.startswith("F132"):
                        remapped = remap_132_to_a(parsed)
                        schedule_writer['F132'][year]['writer'].writerow(remapped)

                    elif form_type.startswith("SB"):
                        schedule_writer['B'][year]['writer'].writerow(parsed)

                    else:
                        print("Ignoring form type %s - filing %s line %s" % (form_type, filenumber, linecount) )


                    
                    

                
                #print("%s %s" % (linecount, parsed))

    return formtypecount


if __name__ == '__main__':




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
    year_missing = 0
    for i,row in enumerate(reader):
        raw_form_type = row['form_type']
        form_type = raw_form_type.rstrip('ANT')
        max=i

        if form_type in main_forms and row['is_superseded'] == 'False':
            year_raw = row.get('coverage_from_date')
            #print("%s" % year_raw)
            year = None
            if year_raw:
                year_left = year_raw[:4]
                try:
                    year = int(year_left)
                    row['year'] = year
                    #print("Found year %s from %s" % (year, year_raw))
                except (ValueError, TypeError) as e:
                    print("Missing year in %s" % row)
                    year_missing += 1

                if year > 2006 and year < 2020:

                    #print("Got form to process %s %s" % (row['filing_number'], row['form_type']))
                    live_filing_list[row['filing_number']] = year
                    included += 1


    hash_done = datetime.now()
    print("Read %s rows and hashed %s in %s" % (max, included, hash_done-start))
    print("Years missing: %s" % year_missing)



    # set up the writers
    for sked in legal_skeds:
        for year in YEARS:

            outfile = schedule_writer[sked]['outfile'] % year
            headers = schedule_writer[sked]['headers']

            schedule_writer[sked][year] = {}
            
            schedule_writer[sked][year]['writer'] = csv.DictWriter(open(outfile, 'w'), fieldnames=headers, extrasaction='ignore')
            schedule_writer[sked][year]['writer'].writeheader()


    # num processed 
    

    files_found = []

    # Walk the electronic dir and find files. 
    print("Finding local fec files, please be patient")
    walk_start = datetime.now()
    filesfound = 0
    for root, dirs, files in os.walk(RAW_ELECTRONIC_DIR):
        path = root.split(os.sep)
        for file in files:
            if file.endswith(".fec"):
                filing = int(file.split(".")[0])
                datestring = path[-1:]
                path_list = path + [file]
                filepath = os.path.join(*path_list) # unpack list to args with *
                
                this_file = {
                    'filepath':filepath,
                    'filing':filing,
                    'datestring':datestring
                }
                files_found.append(this_file)
                filesfound+= 1

    walk_done = datetime.now()
    print("Filewalk completed. Found %s in %s" % (filesfound, walk_done-walk_start))

    
    files_found_sorted = sorted(files_found, key=lambda x: x['filing'])


    num_processed = 0
    formtypecount = Counter()
    process_start = datetime.now()
    NOTIFY = 100

    for filingdict in files_found_sorted:
        filenumber = filingdict['filing']
        filepath = filingdict['filepath']
        datestring = filingdict['datestring']

        year = None
        try:
            year = live_filing_list[str(filenumber)]
            #print("* Found live %s - date: %s" % (filenumber, datestring))
        except KeyError:
            #print("  Not live for %s" % filenumber)
            continue

        result = readfile( "/" + filepath, schedule_writer, year)
        formtypecount.update(result)
        num_processed += 1

        if num_processed % NOTIFY == 0:

            process_time = datetime.now() - process_start 
            total = sum(formtypecount.values())
            print("time %s total rows processed %s, filings processed = %s datestring %s" % (process_time, total, num_processed, datestring))
