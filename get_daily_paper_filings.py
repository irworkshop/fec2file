""" for electronic filings """ 

import requests 
from datetime import datetime 
from settings import *
import os.path
 

def download_file(url, local_filename):
    start = datetime.now()
    # download a file in chunks so we never read the whole thing into RAM
    r = requests.get(url, stream=True)
    size = 0
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                size += 1024
                f.write(chunk)
    end = datetime.now()
    ellapsed = end - start
    print("Downloaded %s in %s" % (size, ellapsed))


if __name__ == '__main__':

    infile = open(PAPER_ZIPFILE_MANIFEST, 'r')
    filings = []
    for raw_row in infile:
        row = raw_row.replace("\n","")
        if "nofiles" in row:
            # rows like this: 20181223.nofiles.zip contain no files and can be ignored
            continue

        if row.endswith(".zip"):
            print("'%s'" % row)
            filings.append(row)


    for i, filing in enumerate(filings):
        print(i)
        remote_url = PAPER_DOWNLOAD_BASE + filing
        local_path = PAPER_ZIPDIR + filing
        if os.path.isfile(local_path):
            print("Skipping %s file already present" % local_path)
        else:
            print("downloading %s to %s" % (remote_url, local_path))
            download_file(remote_url, local_path)
