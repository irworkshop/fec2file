""" the raw contribution files only give an id for the committee name; match them to the committee file. """

import csv
import settings



COMMITTEE_FILES = ['data/20/cm.txt','data/18/cm.txt', 'data/16/cm.txt', 'data/14/cm.txt', 'data/12/cm.txt', 'data/10/cm.txt', 'data/08/cm.txt']
CANDIDATE_FILES = ['data/20/cm.txt','data/18/cn.txt', 'data/16/cn.txt', 'data/14/cn.txt', 'data/12/cn.txt', 'data/10/cn.txt', 'data/08/cn.txt']

SKEDA_PROCESSED = settings.SCHEDULE_A_OUTFILE 
SKEDA_OUTFILE = SKEDA_PROCESSED.replace(".csv", "_annotated.csv")

SKEDA_PAPER_PROCESSED = settings.SCHEDULE_A_PAPER_OUTFILE 
SKEDA_PAPER_OUTFILE = SKEDA_PAPER_PROCESSED.replace(".csv", "_annotated.csv")


SKEDB_PROCESSED = settings.SCHEDULE_B_OUTFILE 
SKEDB_OUTFILE = SKEDB_PROCESSED.replace(".csv", "_annotated.csv")

SKEDB_PAPER_PROCESSED = settings.SCHEDULE_B_PAPER_OUTFILE 
SKEDB_PAPER_OUTFILE = SKEDB_PAPER_PROCESSED.replace(".csv", "_annotated.csv")

SCHEDULE_F132_PROCESSED = settings.SCHEDULE_F132_OUTFILE
SCHEDULE_F132_ANNOTATED = SCHEDULE_F132_PROCESSED.replace(".csv", "_annotated.csv")


SCHEDULE_F132_PAPER_PROCESSED = settings.SCHEDULE_F132_PAPER_OUTFILE
SCHEDULE_F132_PAPER_ANNOTATED = SCHEDULE_F132_PAPER_PROCESSED.replace(".csv", "_annotated.csv")


COMMITTEE_HEADERS = ['CMTE_ID', 'CMTE_NM', 'TRES_NM', 'CMTE_ST1', 'CMTE_ST2', 'CMTE_CITY', 'CMTE_ST', 'CMTE_ZIP', 'CMTE_DSGN', 'CMTE_TP', 'CMTE_PTY_AFFILIATION', 'CMTE_FILING_FREQ', 'ORG_TP', 'CONNECTED_ORG_NM', 'CAND_ID']
CANDIDATE_HEADERS = ['CAND_ID','CAND_NAME','CAND_PTY_AFFILIATION','CAND_ELECTION_YR','CAND_OFFICE_ST','CAND_OFFICE','CAND_OFFICE_DISTRICT','CAND_ICI','CAND_STATUS','CAND_PCC','CAND_ST1','CAND_ST2','CAND_CITY','CAND_ST','CAND_ZIP']


SKEDA_HEADERS = ['filing_number','line_sequence','form_type','filer_committee_id_number','transaction_id','back_reference_tran_id_number','back_reference_sched_name','entity_type','contributor_organization_name','contributor_name','contributor_last_name','contributor_first_name','contributor_middle_name','contributor_prefix','contributor_suffix','contributor_street_1','contributor_street_2','contributor_city','contributor_state','contributor_zip_code','election_code','election_other_description','contribution_date','contribution_amount','contribution_aggregate','contribution_purpose_descrip','contributor_employer','contributor_occupation','donor_committee_fec_id','donor_committee_name','donor_candidate_fec_id','donor_candidate_last_name','donor_candidate_first_name','donor_candidate_middle_name','donor_candidate_prefix','donor_candidate_suffix','donor_candidate_office','donor_candidate_state','donor_candidate_district','conduit_name','conduit_street1','conduit_street2','conduit_city','conduit_state','conduit_zip_code','memo_code','memo_text_description','reference_code']
SKEDA_RESULT_HEADERS = SKEDA_HEADERS + ['year','CMTE_NM', 'CMTE_ST1','CMTE_ST2','CMTE_CITY', 'CMTE_ST', 'CMTE_ZIP', 'CAND_ID', 'CAND_NAME']

SKEDB_HEADERS = ['filing_number','line_sequence','form_type','filer_committee_id_number','transaction_id_number','back_reference_tran_id_number','back_reference_sched_name','entity_type','payee_organization_name','payee_name', 'payee_last_name','payee_first_name','payee_middle_name','payee_prefix','payee_suffix','payee_street_1','payee_street_2','payee_city','payee_state','payee_zip_code','election_code','election_other_description','expenditure_date','expenditure_amount','semi_annual_refunded_bundled_amt','expenditure_purpose_descrip','category_code','beneficiary_committee_fec_id','beneficiary_committee_name','beneficiary_candidate_fec_id','beneficiary_candidate_last_name','beneficiary_candidate_first_name','beneficiary_candidate_middle_name','beneficiary_candidate_prefix','beneficiary_candidate_suffix','beneficiary_candidate_office','beneficiary_candidate_state','beneficiary_candidate_district','conduit_name','conduit_street_1','conduit_street_2','conduit_city','conduit_state','conduit_zip_code','memo_code','memo_text_description','reference_to_si_or_sl_system_code_that_identifies_the_account']
SKEDB_RESULT_HEADERS = SKEDB_HEADERS + ['year', 'CMTE_NM', 'CMTE_ST1','CMTE_ST2','CMTE_CITY', 'CMTE_ST', 'CMTE_ZIP', 'CAND_ID', 'CAND_NAME']

COMMITTEE_DICT_KEY = "%s-%s" 
CANDIDATE_DICT_KEY = "%s-%s" 

MIN_YEAR = 2007

def dictify_row(line, headers):
    line = line.rstrip("\n")
    line_array = line.split("|")
    dict = {}
    for i, header in enumerate(headers):
        try:
            dict[header]=line_array[i]
        except IndexError:
            dict[header] = None
    return dict


def get_committee_dict():
    print("Making committee dictionary")
    comdict = {}
    i=0
    for committee_file in COMMITTEE_FILES:
        year = committee_file.split("/")[1]
        infile = open(committee_file, 'r')
        
        while True:
            i+=1
            this_line = infile.readline()
            if not this_line:
                break

            linedict = dictify_row(this_line, COMMITTEE_HEADERS)
            committee_key = COMMITTEE_DICT_KEY % (linedict['CMTE_ID'], year)
            comdict[committee_key] = {  
                'NAME':linedict['CMTE_NM'],
                'CAND_ID':linedict['CAND_ID'],
                'CMTE_ST1':linedict['CMTE_ST1'], 
                'CMTE_ST2':linedict['CMTE_ST2'], 
                'CMTE_CITY':linedict['CMTE_CITY'], 
                'CMTE_ST':linedict['CMTE_ST'],
                'CMTE_ZIP':linedict['CMTE_ZIP'],
                }
            #print("adding key %s" % committee_key)
        infile.close()
    
    print("Created committee lookup with %s keys" % i)
    return comdict

def get_candidate_dict():
    print("Making candidate dictionary")
    candict = {}
    i=0
    for candidate_file in CANDIDATE_FILES:
        year = candidate_file.split("/")[1]
        infile = open(candidate_file, 'r')
        
        while True:
            i+=1
            this_line = infile.readline()
            if not this_line:
                break

            linedict = dictify_row(this_line, CANDIDATE_HEADERS)
            candidate_key = CANDIDATE_DICT_KEY % (linedict['CAND_ID'], year)
            candict[candidate_key] = {  
                'CAND_NAME':linedict['CAND_NAME'],
                }
            #print("adding key %s %s" % (candidate_key, candict[candidate_key]))
        infile.close()
    
    print("Created candidate lookup with %s keys" % i)
    return candict

def process_sked_F132(committeedict, candidatedict,  year, sked132_infile, sked132_outfile):
    f = open(sked132_outfile % year, 'w')
    dw = csv.DictWriter(f, fieldnames=SKEDA_RESULT_HEADERS)
    dw.writeheader()

    infile = open(sked132_infile % year, 'r')
    reader = csv.DictReader(infile)

    for (i,row) in enumerate(reader):

        CMTE_NAME = ''
        try:
            CMTE_ID = row['filer_committee_id_number']

            raw_year = row['contribution_date']
            year = 0
            year = int(raw_year[:4])
        except:
            #pint("no year in %s line %s: %s" % (row['filing_number'], row['line_sequence'], raw_year))
            continue

        if year < MIN_YEAR:
            continue

        row['year'] = year

        if year % 2 ==1:
            year += 1

        year_string = str(year)[-2:]

        # add the committee name
        committee_key = COMMITTEE_DICT_KEY % (CMTE_ID, year_string)
        try:
            thisdict = committeedict[committee_key]
            #print("Got committee dict %s" % thisdict)
            row['CMTE_NM'] = thisdict['NAME']
            row['CAND_ID'] = thisdict['CAND_ID']
            row['CMTE_ST1'] = thisdict['CMTE_ST1']
            row['CMTE_ST2'] = thisdict['CMTE_ST2'] 
            row['CMTE_CITY'] = thisdict['CMTE_CITY'] 
            row['CMTE_ST'] = thisdict['CMTE_ST']
            row['CMTE_ZIP'] = thisdict['CMTE_ZIP']

            #print("Found match * %s %s" % (row['CMTE_NM'], committee_key))
        except KeyError:
            print("line %s: missing %s" % (i, committee_key))
            dw.writerow(row)
            continue

        # add the candidate name, if applicable
        if row['CAND_ID']:
            candidate_key = CANDIDATE_DICT_KEY % (row['CAND_ID'], year_string)
            try:
                thisdict = candidatedict[candidate_key]
                row['CAND_NAME'] = thisdict['CAND_NAME']

                #print("Found match * %s %s" % (row['CMTE_NM'], committee_key))
            except KeyError:
                print("line %s: missing %s" % (i, committee_key))
                pass

        dw.writerow(row)


def process_sked_a(committeedict, candidatedict,  year, skeda_infile, skeda_outfile):

    f = open(skeda_outfile % year, 'w')
    dw = csv.DictWriter(f, fieldnames=SKEDA_RESULT_HEADERS)
    dw.writeheader()

    infile = open(skeda_infile % year, 'r')
    reader = csv.DictReader(infile)

    for (i,row) in enumerate(reader):

        CMTE_NAME = ''
        CMTE_ID = row['filer_committee_id_number']

        raw_year = row['contribution_date']
        year = 0
        try:
            year = int(raw_year[:4])
        except ValueError:
            #print("no year in %s line %s: %s" % (row['filing_number'], row['line_sequence'], raw_year))
            continue

        if year < MIN_YEAR:
            continue

        row['year'] = year

        if year % 2 ==1:
            year += 1

        year_string = str(year)[-2:]

        # add the committee name
        committee_key = COMMITTEE_DICT_KEY % (CMTE_ID, year_string)
        try:
            thisdict = committeedict[committee_key]
            #print("Got committee dict %s" % thisdict)
            row['CMTE_NM'] = thisdict['NAME']
            row['CAND_ID'] = thisdict['CAND_ID']
            row['CMTE_ST1'] = thisdict['CMTE_ST1']
            row['CMTE_ST2'] = thisdict['CMTE_ST2'] 
            row['CMTE_CITY'] = thisdict['CMTE_CITY'] 
            row['CMTE_ST'] = thisdict['CMTE_ST']
            row['CMTE_ZIP'] = thisdict['CMTE_ZIP']

            #print("Found match * %s %s" % (row['CMTE_NM'], committee_key))
        except KeyError:
            print("line %s: missing %s" % (i, committee_key))
            dw.writerow(row)
            continue

        # add the candidate name, if applicable
        if row['CAND_ID']:
            candidate_key = CANDIDATE_DICT_KEY % (row['CAND_ID'], year_string)
            try:
                thisdict = candidatedict[candidate_key]
                row['CAND_NAME'] = thisdict['CAND_NAME']

                #print("Found match * %s %s" % (row['CMTE_NM'], committee_key))
            except KeyError:
                print("line %s: missing %s" % (i, committee_key))
                pass

        dw.writerow(row)

def process_sked_b(committeedict, candidatedict, year, skedb_infile, skedb_outfile):
    f = open(skedb_outfile % year, 'w')
    dw = csv.DictWriter(f, fieldnames=SKEDB_RESULT_HEADERS)
    dw.writeheader()

    infile = open(skedb_infile % year, 'r')
    reader = csv.DictReader(infile)

    for (i,row) in enumerate(reader):

        CMTE_NAME = ''
        CMTE_ID = row['filer_committee_id_number']

        raw_year = row['expenditure_date']
        year = 0
        try:
            year = int(raw_year[:4])
        except ValueError:
            #print("no year in %s line %s: %s" % (row['filing_number'], row['line_sequence'], raw_year))
            continue
        if year < MIN_YEAR:
            continue
        row['year'] = year
        if year % 2 ==1:
            year += 1

        year_string = str(year)[-2:]

        # add the committee name
        committee_key = COMMITTEE_DICT_KEY % (CMTE_ID, year_string)
        try:
            thisdict = committeedict[committee_key]
            #print("Got committee dict %s" % thisdict)
            row['CMTE_NM'] = thisdict['NAME']
            row['CAND_ID'] = thisdict['CAND_ID']
            row['CMTE_ST1'] = thisdict['CMTE_ST1']
            row['CMTE_ST2'] = thisdict['CMTE_ST2'] 
            row['CMTE_CITY'] = thisdict['CMTE_CITY'] 
            row['CMTE_ST'] = thisdict['CMTE_ST']
            row['CMTE_ZIP'] = thisdict['CMTE_ZIP']

            #print("Found match * %s %s" % (row['CMTE_NM'], committee_key))
        except KeyError:
            print("line %s: committee missing %s" % (i, committee_key))
            dw.writerow(row)
            continue


        # add the candidate name, if applicable
        
        if row['CAND_ID']:
            candidate_key = CANDIDATE_DICT_KEY % (row['CAND_ID'], year_string)
            try:
                thisdict = candidatedict[candidate_key]
                row['CAND_NAME'] = thisdict['CAND_NAME']

                #print("Found match * %s %s" % (row['CMTE_NM'], committee_key))
            except KeyError:
                print("line %s: candidate missing %s" % (i, committee_key))


        
        dw.writerow(row)

if __name__ == '__main__':
    
    committeedict = get_committee_dict()
    candidatedict = get_candidate_dict()

    YEARS = [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]

    # YEARS = [2018, 2019]

    for year in YEARS: 
        if year in [2018, 2019]: 

            print("Running year %s" % year)
            process_sked_a(committeedict, candidatedict, year, SKEDA_PROCESSED, SKEDA_OUTFILE)
            process_sked_a(committeedict, candidatedict, year, SKEDA_PAPER_PROCESSED, SKEDA_PAPER_OUTFILE)
            process_sked_b(committeedict, candidatedict, year, SKEDB_PROCESSED, SKEDB_OUTFILE)
            process_sked_a(committeedict, candidatedict, year, SKEDB_PAPER_PROCESSED, SKEDB_PAPER_OUTFILE)

        # based on filing research; Obama 08/12 filed electronically; Trump 16 filed on paper
        if year in [2008, 2012]: 
            process_sked_F132(committeedict, candidatedict, year, SCHEDULE_F132_PROCESSED, SCHEDULE_F132_ANNOTATED)
        if year in [2016]:
            process_sked_F132(committeedict, candidatedict, year, SCHEDULE_F132_PAPER_PROCESSED, SCHEDULE_F132_PAPER_ANNOTATED)


        # TK F132.

    

