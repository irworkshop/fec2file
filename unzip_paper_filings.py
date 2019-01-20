import requests 
import os
from datetime import datetime 

from settings import *

def makedir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

if __name__ == '__main__':

    infile = open(PAPER_ZIPFILE_MANIFEST, 'r')
    filings = []
    for raw_row in infile:
        row = raw_row.replace("\n","")
        if row.endswith(".zip"):
            print("'%s'" % row)
            filings.append(row)


    for i, filing in enumerate(filings):
        raw_name = filing.replace(".zip", "")
        directory_path = RAW_PAPER_DIR + raw_name
        makedir(directory_path)

        unzip_cmd = "unzip %s%s -d %s%s/" % (PAPER_ZIPDIR, filing, RAW_PAPER_DIR, raw_name)
        print(i)
        print(unzip_cmd)
        os.system(unzip_cmd)

