import os 
import fecfile
import json
import csv 
import sys

from settings import RAW_ELECTRONIC_DIR, MASTER_HEADER_ROW, HEADER_DUMP_FILE

START_YEAR = 2021

ERROR_HEADERS = ['path', 'error', ]

def readfile(filepath, writer):

    filename = os.path.basename(filepath)
    filename = filename.replace(".fec", "")
    file_number = int(filename)


    file = open(filepath, encoding = "ISO-8859-1")
    #file = open(filepath)

    firstline = file.readline()
    secondline = file.readline()
    firstline = firstline.replace("\n", "")
    raw_results = fecfile.parse_header(firstline)
    results = raw_results[0]
    results["filing_number"] = file_number
    version = raw_results[1]
    lines = None
    if len(raw_results)==3:
        lines = raw_results[1]

    original_report = results.get('report_id', None)
    report_number = results.get('report_number', None)
    if original_report:
        original_report = original_report.replace("FEC-", "")
        original_report_number = int(original_report)
        results["amends"] = original_report_number
        #print("Found amended filing %s amends %s # %s" % (file_number, original_report_number, report_number))

    secondlineparsed = fecfile.parse_line(secondline, version)
    #print(secondlineparsed)
    results["form_type"] = secondlineparsed.get('form_type', '')
    results["filer_committee_id_number"] = secondlineparsed.get('filer_committee_id_number', '')
    results["committee_name"] = secondlineparsed.get('committee_name', '')
    results["date_signed"] = secondlineparsed.get('date_signed', '')
    results["coverage_from_date"] = secondlineparsed.get('coverage_from_date', '')
    results["coverage_through_date"] = secondlineparsed.get('coverage_through_date', '')

    writer.writerow(results)

if __name__ == '__main__':


    outfile =  open(HEADER_DUMP_FILE, 'w')
    dw = csv.DictWriter(outfile, fieldnames=MASTER_HEADER_ROW, extrasaction='ignore')
    dw.writeheader()
    print("Writing output to %s" % HEADER_DUMP_FILE)

    errorfile = open("header_read_errors.csv", 'w')
    error_writer = csv.DictWriter(errorfile, fieldnames=ERROR_HEADERS, extrasaction='ignore')
    error_writer.writeheader()

    for dirName, subdirList, fileList in os.walk(RAW_ELECTRONIC_DIR, topdown=False):
        try:

            directory_year = int(dirName.split("/")[-1][0:4])
            if directory_year < START_YEAR:
                print("Ignoring directory %s" % dirName)
                continue
        except ValueError:
            continue

        
        for fname in fileList:
            if fname.endswith(".fec"):
                full_path = os.path.join(dirName, fname)
                #readfile(full_path, dw)
                #print("Found file %s" % full_path)

                try:
                    readfile(full_path, dw)
                except Exception as e:
                    print("error reading %s: %s" % (full_path, e))

                    error_writer.writerow({
                        'path':full_path,
                        'error':e
                        })
                    
                    

