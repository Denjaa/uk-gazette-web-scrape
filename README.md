# gazette-scrape

## Description
Gazette is a place where the insolvencies are being published. The script is going into a specific gazette URL that is being filtered on specific criteria and scrapes data.

## What script does:
1. Goes to allocated website
2. Loops through all URLs available for all companies that have insolvencies published
3. Goes into each inidivual company and scrapes data
4. Once data is scraped it saves all data to CSV
5. Once CSV is done and no duplicates available it appends all data to backup file
6. Goes to sleep for 20 minutes and then reactivate itself and looks for new adds if available

To run the script you would need Python 3.6 version.

## Commmand line:
```
python gazette_v1.py
```


Once that command is ran it automatically generates backup.csv and output.csv that the script requires.
