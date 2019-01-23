

ELECTRONIC_ZIPFILE_MANIFEST = 'metadata/electronic_zipfiles.txt'
# requires lotsa space, you may want to customize
ELECTRONIC_ZIPDIR = 'zip/electronic/'
RAW_ELECTRONIC_DIR = 'fecfilings/electronic/'


PAPER_ZIPFILE_MANIFEST = 'metadata/paper_zipfiles.txt'
# requires lotsa space, you may want to customize
PAPER_ZIPDIR = 'zip/paper/'
RAW_PAPER_DIR = 'fecfilings/paper/'


# does this refresh ? May want a different region? 
FEC_BUCKET = 'cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com'
DOWNLOAD_BASE = "https://%s/bulk-downloads/electronic/" % FEC_BUCKET


PAPER_DOWNLOAD_BASE = "https://%s/bulk-downloads/paper/" % FEC_BUCKET


# FIRST LINE OF HEADERs processed to this
HEADER_DUMP_FILE = 'headers/headers_raw.csv'

HEADER_PAPER_DUMP_FILE = 'headers/paper_headers_raw.csv'

# amendments are marked in this file, created by the amend_headers script. 
AMENDED_HEADER_FILE = 'headers/headers_amended.csv'
AMENDED_PAPER_HEADER_FILE = 'headers/paperheaders_amended.csv'


SCHEDULE_A_OUTFILE = 'schedules/ScheduleA.csv'
SCHEDULE_A_PAPER_OUTFILE = 'schedules/ScheduleA-paper.csv'

SCHEDULE_B_OUTFILE = 'schedules/ScheduleB.csv'
SCHEDULE_B_PAPER_OUTFILE = 'schedules/ScheduleB-paper.csv'



# from https://github.com/esonderegger/fecfile/blob/master/fecfile/mappings.json#L2

# Not every version completes these all
# this is for electronic only really
MASTER_HEADER_ROW = [
    "form_type",
    "filer_committee_id_number",
    "committee_name",
    "date_signed",
    "filing_number", # 
    "amends", 
    "record_type", 
    "ef_type",
    "fec_version",
    "soft_name",
    "soft_ver",
    "batch_number",
    "received_date",
    "report_id",
    "report_number",
    "comment",
    "name_delim",
]


MASTER_PAPER_HEADER_ROW = ['file_size', 'file_linecount'] +  MASTER_HEADER_ROW + ['coverage_from_date', 'coverage_through_date']




## paper filings generally leave out filer_committee_id_number, committee_name, filing_number,
## amends, 

## P1 omits report_number

FEC_API_KEY = ''
API_DUMP = 'headers/apidump.csv'




try:
    from local_settings import *
except ImportError:
    print("Error importing local_settings.py")
