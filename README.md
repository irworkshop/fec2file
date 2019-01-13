# fec2file

Dumps FEC form schedules to file.

Most users will prefer the fec's bulk files, which are available here. 



## processing zipfiles


`$ python get_daily_zipfiles.py`

retrieves the zipfiles that are listed in the metadata/electronic_zipfiles.txt (or set in settings.ELECTRONIC_ZIPFILE_MANIFEST). 

Because there are some random names it's often easier to just grab this from the live ftp site and paste it into the manifest file. 

The zipfiles are downloaded into settings.ELECTRONIC_ZIPDIR, which by default is zip/electronic/
