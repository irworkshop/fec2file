""" for electronic filings """ 

import requests 
from datetime import datetime 
from settings import *
import os
import os.path
 

def download_file(url, local_filename):
    start = datetime.now()
    # download a file in chunks so we never read the whole thing into RAM
    r = requests.get(url, stream=True)

    # Check the status before writing anything. Without this a 404 or a 5xx got
    # written into the .zip as the error body -- the file then looked downloaded,
    # was skipped on every rerun, and only surfaced later as a corrupt archive at
    # the unzip stage, far from the cause.
    if r.status_code != 200:
        raise RuntimeError("%s returned HTTP %s -- not saved" % (url, r.status_code))

    # Write to a .part file and rename only once the download completes, so an
    # interrupted run leaves no half-file that the "already present" check would
    # happily skip next time.
    partial = local_filename + ".part"
    size = 0
    with open(partial, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                size += len(chunk)
                f.write(chunk)

    expected = r.headers.get('Content-Length')
    if expected is not None and int(expected) != size:
        os.remove(partial)
        raise RuntimeError("%s: expected %s bytes, got %s -- not saved" % (
            url, expected, size))

    os.rename(partial, local_filename)
    end = datetime.now()
    ellapsed = end - start
    print("Downloaded %s bytes in %s" % (size, ellapsed))


if __name__ == '__main__':

    infile = open(ELECTRONIC_ZIPFILE_MANIFEST, 'r')
    filings = []
    for raw_row in infile:
        row = raw_row.replace("\n","")
        if row.endswith(".zip"):
            print("'%s'" % row)
            filings.append(row)


    for i, filing in enumerate(filings):
        print(i)
        remote_url = DOWNLOAD_BASE + filing
        local_path = ELECTRONIC_ZIPDIR + filing
        if os.path.isfile(local_path):
            print("Skipping %s file already present" % local_path)
        else:
            download_file(remote_url, local_path)
