import os 
import fecfile
import json
import csv 
import sys
import warnings

# try to better catch parser warnings and record them as errors
warnings.filterwarnings("error")

from settings import RAW_PAPER_DIR, MASTER_PAPER_HEADER_ROW, HEADER_PAPER_DUMP_FILE

ERROR_HEADERS = ['filing_number', 'form', ]

def readfile(filepath, writer):

    filename = os.path.basename(filepath)
    filename = filename.replace(".fec", "")
    file_number = int(filename)


    firstline = None
    secondline = None
    linecount = 2 # header + formline
    with open(filepath, encoding = "ISO-8859-1") as file:
        firstline = file.readline()
        secondline = file.readline()


        while True:
            nextline = file.readline()
            if not nextline:
                break
            linecount += 1


    file_size = os.path.getsize(filepath)

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
    results["form_type"] = secondlineparsed.get('form_type', '')
    results["coverage_through_date"] = secondlineparsed.get('coverage_through_date', '')
    results["coverage_from_date"] = secondlineparsed.get('coverage_from_date', '')
    results["file_size"] = file_size
    results["file_linecount"] = linecount

    # hack for F7 / F5 / F9
    if not results["committee_name"]:
        results["committee_name"] = secondlineparsed.get('organization_name', '')


    writer.writerow(results)


if __name__ == '__main__':


    outfile =  open(HEADER_PAPER_DUMP_FILE, 'w')
    print("Writing out to %s" % HEADER_PAPER_DUMP_FILE)
    dw = csv.DictWriter(outfile, fieldnames=MASTER_PAPER_HEADER_ROW, extrasaction='ignore')
    dw.writeheader()
    print("Writing output to %s" % HEADER_DUMP_FILE)


    #errorfile = open("header_read_errors.csv", 'w')
    #print("error file %s - headers %s" % (errorfile, ERROR_HEADERS))
    #error_writer = csv.DictWriter(errorfile, fieldnames=ERROR_HEADERS, extrasaction='ignore')
    #error_writer.writeheader()

    for dirName, subdirList, fileList in os.walk(RAW_PAPER_DIR, topdown=False):
        #print('Found directory: %s' % dirName)
        for fname in fileList:
            if fname.endswith(".fec"):
                full_path = os.path.join(dirName, fname)
                #readfile(full_path, dw)
                #print("Found file %s" % full_path)

                try:
                     readfile(full_path, dw)
                except Exception as e:
                    print("-Error in %s: %s" % (full_path, e))

    #errorfile.close()
    outfile.close()
