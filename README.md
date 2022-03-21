# List a GitHub Users Public Gist's.

## Requirements

Python 3.7 or later

Ensure the following modules are installed in python environment.

- requests
- pandas
- tabulate

There is requirements.txt included

e.g 
pip install -r requirements.txt 

NOTE: you may run this differently depending on your loacl pythin environment configuration.

## How to run the application

There are 2 files python files to run.

NOTE: the scripts have no reference to paths for any files used and will run in the directory you have downloaded both py scripts into.
### Run createinvocationdb.py ONCE !

./createinvocationdb.py

This will create create an empty database in the directory you run it in with an empty table (invocations) and 2 columns, gist_user and last_date.

### Run eegistpython.py 

./eegistpython.py

You will be promted to enter the GitHIb user you wish to list the gist's for.

On first invocation the script will list ALL gist's for that user. Any subsequent runs will only list any new gist's CREATED since the last of invocation of the script. 

NOTE: the recorded date is "created date" so it will not pick up revisions of gist's.


### Functional overide

If you wish to overide the script functionality and list ALL gist's for a user then run the script with the "-f yes" flag. 

./eegistpython.py -f yes

NOTE: no need to set the -f no flag as it is set to no as default.