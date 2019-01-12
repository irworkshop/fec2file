import requests 
import os
from datetime import datetime 

from settings import RAW_ELECTRONIC_DIR


filings = ['20180905.zip', '20180906.zip','20180907.zip']


def makedir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


for filing in filings:
    raw_name = filing.replace(".zip", "")
    directory_path = RAW_ELECTRONIC_DIR + raw_name
    makedir(directory_path)

    unzip_cmd = "unzip zip/electronic/%s -d fecfilings/electronic/%s/" % (filing, raw_name)
    os.system(unzip_cmd)

