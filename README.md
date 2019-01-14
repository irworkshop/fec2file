# fec2file

Dumps FEC form schedules to file.

Most users will prefer the fec's bulk files, which are available here. 

## local settings

You may want to set the following variables in a local\_settings.py file, which will override the settings.py values. The full download requires 14GB and 111GB for the zipped and unzipped directories respectively. 

	ELECTRONIC\_ZIPDIR  # where the zipped electronic filings go
	RAW\_ELECTRONIC\_DIR # where the unzipped electronic filings go


## processing zipfiles

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

