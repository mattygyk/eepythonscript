# List a GitHub Users Public Gist's.

## Requirements

Python 3.7 or later

Ensure the following modules are installed in python environment.

- requests
- json
- sqlite3
- pandas
- argparse
- tabulate
- datetime

## How to run the application

There are 2 files python files to run.

NOTE: the scripts have no reference to paths for any files used and will run in the directory you have downloaded both py scripts into.
### Run createinvocationdb.py ONCE !

./createinvocationdb.py

This will create create an empty database in the directory you running the scripts form with 2 tables, gist_user and last_date.

### Run eegistpython.py 

./eegistpython.py

You will be promted to enter the GitHIb user you wish to list the gist's for.

On first invocation the script will list ALL gist's for that user. Any subsequent runs will only list any new gist's CREATED since the last of invocation of the script. 

NOTE: the recorded date is "created date" so it will not pick up revisions of gist's.


### Functional overide

If you wish to overide the script functionality and list ALL gist's for a user then run the script with the "-f yes" flag. 

./eegistpython.py -f yes

NOTE: no need to set the -f no flag as it is set to no as default.