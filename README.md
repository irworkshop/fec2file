# fec2file

Reads raw .fec files to standardized .csv files organized by original filing schedule, using Evan Sonderegger's [fecfile](https://github.com/esonderegger/fecfile). 

Most users will prefer the FEC's bulk files, which are easier to use and available [here](https://classic.fec.gov/finance/disclosure/ftp_download.shtml). 

## Local settings

You may want to set the following variables in a local\_settings.py file, which will override the settings.py values. The full download requires 14GB and 111GB for the zipped and unzipped directories respectively; the final extract schedules A and B amount to about 75GB. 

	ELECTRONIC_ZIPDIR  # where the zipped electronic filings go
	RAW_ELECTRONIC_DIR # where the unzipped electronic filings go
	SCHEDULE_A_OUTFILE # .csv of receipts from electronic filings
	SCHEDULE_B_OUTFILE # .csv of expenditures from electronic filings
	SCHEDULE_A_PAPER_OUTFILE # .csv of receipts from paper filings
	SCHEDULE_B_PAPER_OUTFILE # .csv of expenditures from electronic filings

## A. processing electronic zipfiles

### 1. Get zipped electronic .fec files 

`$ python get_daily_zipfiles.py`

retrieves the zipfiles that are listed in the metadata/electronic\_zipfiles.txt (or set in settings.ELECTRONIC\_ZIPFILE\_MANIFEST). This may take a while; you may want to run it as `nohup  python get_daily_zipfiles.py &` to detach from the process on linux and make sure it keeps running if your connection goes. 

Because there are some random names it's often easier to just grab this from the live ftp site and paste it into the manifest file. 

The zipfiles are downloaded into settings.ELECTRONIC\_ZIPDIR, which by default is zip/electronic/

### 2. Unzip the files

`$ python unzip_filings.py`

This just executes the unzip command using an old school os.system call, there's doubtless a better approach to this. 

### 3. Extract the headers

`$ python process_filing_headers.py`

Writes a .csv file to settings.HEADER\_DUMP\_FILE, by default headers/headers\_raw.csv. 

### 4. Figure out which amendments to include or not

`$ python amend_headers.py`



writes output to settings.AMENDED_HEADER_FILE. It includes  filing_number,is_superseded,amended_by,last_amendment,report_number,filer_committee_id_number,form_type,date_signed,comment. 

Filings that are not superseded by a later amendment are included, whereas those that have been replaced are not. 

It's important to note that there's some ambiguity about how "chains" of amendments get listed. The logic used here is that if 2 amends 1 and 3 amends 2, sometimes 3 will be listed as if it is amending 1. 

Another way of thinking about these filings is whether a report is the "most recent" version of an electronic filing. This works because FEC requires filers to submit an *complete replacement* of the original filing in the amendment. 


### 5. Read the most recent periodic filings and extract data

Currently we just read campaign receipts (mostly contributions) reported in Schedule A and campaign expenditures reported on Schedule B. This includes operational spending, but leaves out "independent expenditures" by super pacs and dodgy outside groups that don't report their donors. These are reported on schedule E and on form F57; we hope to have a unified output of these in the future. 

The output is written to settings.SCHEDULE_A_OUTFILE and settings.SCHEDULE_B_OUTFILE. You'll probably want to reconfigure the settings for these to a directory with plenty of room; the complete output of schedule A is bigger than 44GB. 

`$python read_filings_from_amended_headers.py`


## B. processing paper zipfiles

Overall this process is very similar to dealing with the electronic filings, but amendments are more complex because A. they can be either full or partial replacements, although there's no indication given in the filing as to which they are and B. there's no listing of the "original" filing being fixed. 

### TKTK


# Processing logic

### Overview

The FEC predates electronic record-keeping, and many of it's regulations are aimed at insuring there exists a complete paper record of campaign spending. While the FEC has done a great job at making data available, there are some limitations. 

As a matter of policy, FEC doesn't release the street addresses of people and companies named. This restriction applies to any downloads from the site, with the exception of the original filings received. This is a nod to the law: it's illegal to collect address information from campaign donors in order to make mailing lists of your own. 

For journalists, investigators and citizens interested in tracking influence, however, addresses can provide critical confirmation of a linkage between corporate entities. These addresses can be found on the original filings displayed on FEC's web site, but this is of little use if you don't know which filing to reference. 

To extract the most complete record of campaign finance available, it is necessary to download all of the originally submitted filings and process them--essentially what the FEC does in order to produce the bulk downloads. 

This only became possible around 2015, when the FEC began releasing the .fec files of submissions originally made on paper. Prior to then, complete address information was only available on electronic filings. 

TK TK TK

### Periodic versus ephemeral filngs

US election law requires "independent" election spenders to report large expenditures ahead of an election within 24 or 48 hours; candidates must also report large contributions received in the last 20 days of an election within 2 days. 

These early notifications are intended to let the public know about the spending, but in exchange for their timeliness FEC tolerates less exact numbers. The "final" version of the transactions also appear in a monthly or quarterly periodic report, which also include special pre- and post- election periods. 

This library disregards the 24 and 48 hour reports in favor of the periodic reports, as those are seen as more reliable. This means, however, that you'd have to add data from the periodic reports to make this 

### Amendments

US campaign finance rules allow filers to amend their filings as many times as they want. Dealing with files submitted electronically is relatively simple, because the original filing is listed in the report header. In other words, the amendment says which original report it is "fixing". 

Paper amendments are more difficult, because they do not say which filing they are changing. 


### Electronic filings


