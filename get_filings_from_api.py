import requests
import json
import csv
from time import sleep

from settings import FEC_API_KEY, API_DUMP

RAW_API_URL = "https://api.open.fec.gov/v1/filings/?sort_nulls_last=false&sort_hide_null=false&sort=-receipt_date&page=%s&per_page=100&sort_null_only=false&filer_type=e-file&api_key=%s" 


def get_writer(headers):
    outfile =  open(API_DUMP, 'w')
    dw = csv.DictWriter(outfile, fieldnames=headers, extrasaction='ignore')
    dw.writeheader()
    return dw


if __name__ == "__main__":


    writer = None
    page_number = 0
    pages = 1

    MAX = 20000

    while True:
        page_number += 1

        if page_number > pages:
            break
        if page_number > MAX:
            break

        api_call = RAW_API_URL% (page_number, FEC_API_KEY)
        r = requests.get(api_call)
        response = r.text
        try:
            json_response = json.loads(response)
        except Exception as e:
            print("Error in page %s: %s" % (page_number, e))
            continue
            ## occasionally we see this: json.decoder.JSONDecodeError: Extra data: line 1 column 5 (char 4)


        pages = json_response['pagination']['pages']
        print("page %s of %s" % (page_number, pages))

        for result in json_response['results']:

            if not writer:
                headers = result.keys()
                writer = get_writer(headers)
            
            writer.writerow(result)

        # rate limit is 1000 requests per hour
        print("now sleeping for 3.5 seconds")
        sleep(3.5)


