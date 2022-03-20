This program is used to process the vice dataset for analysis.

usage: processer.py [-h] [--outputname OUTPUTNAME] datapath

positional arguments:
  datapath              Path to data

optional arguments:
  -h, --help            show this help message and exit
  --outputname OUTPUTNAME
                        Name to save processed data as

** Note: ** Dataset is expected to contain at least the following important columns
['Post Created', 'Video Share Status', 'Total Views', 'Total Views For All Crossposts', 'Video Length', 
'Message', 'Link Text', 'Likes at Posting','Likes','Comments','Shares','Love','Wow','Haha','Sad', 'Angry', 
'Care'] 

Result of analysis can be found in: https://datastudio.google.com/reporting/5f526187-6b3c-404c-87bc-97be2b3c7827
Writeup from analysis can be found in: https://docs.google.com/document/d/1LxjQnJccyx_ZPSBNJ7nX9VTJKjG_QxYi/edit?usp=sharing&ouid=116983985507069912443&rtpof=true&sd=true