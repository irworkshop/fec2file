

ELECTRONIC_ZIPFILE_MANIFEST = 'metadata/electronic_zipfiles.txt'
ELECTRONIC_ZIPDIR = 'zip/electronic/'
RAW_ELECTRONIC_DIR = 'fecfilings/electronic/'


PAPER_ZIPFILE_MANIFEST = 'metadata/paper_zipfiles.txt'
PAPER_ZIPDIR = 'zip/paper/'



# does this refresh ? May want a different region? 
FEC_BUCKET = 'cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com'
DOWNLOAD_BASE = "https://%s/bulk-downloads/electronic/" % FEC_BUCKET


PAPER_DOWNLOAD_BASE = "https://%s/bulk-downloads/paper/" % FEC_BUCKET


# FIRST LINE OF HEADERs processed to this
HEADER_DUMP_FILE = 'headers/headers_raw.csv'
# amendments are marked in this file, created by the amend_headers script. 
AMENDED_HEADER_FILE = 'headers/headers_amended.csv'

SCHEDULE_A_OUTFILE = 'schedules/ScheduleA.csv'
SCHEDULE_B_OUTFILE = 'schedules/ScheduleB.csv'


# from https://github.com/esonderegger/fecfile/blob/master/fecfile/mappings.json#L2

# Not every version completes these all
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

FEC_API_KEY = ''
API_DUMP = 'headers/apidump.csv'




try:
    from local_settings import *
except ImportError:
    print("Error importing local_settings.py")
