import csv
from pressevents.models import EventCode

def run():
    with open('/home/capooti/git/github/capooti/smartfeeds/pressevents/doc/CAMEO.eventcodes.txt', 'rb') as csvfile:
        codereader = csv.reader(csvfile, delimiter='\t')
        for row in codereader:
            print row
            ec = EventCode()
            ec.code = row[0]
            ec.description = row[1]
            ec.save()

