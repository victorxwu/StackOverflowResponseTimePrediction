
# filter.py
# Filter data from the Stack Overflow export into a data
# format that is easier to work with (json) and is filtered
# such that it only returns records in a specific range.
# It also removes anything that is not a question or answer.
# H.E. Added encoding type to file open 

import sys
import json
import xml.sax
from datetime import date
from datetime import datetime

class PostHandler(xml.sax.ContentHandler):

    DATE_FROM = date(2017, 6, 1)
    DATE_TO   = date(2017, 12, 31)

    def __init__(self, output):
        self.output = output
        self.first = True
        self.count = 0

    def startDocument(self):
        self.output.write('[\n')

    def startElement(self, name, attrs):
        if name == 'row' and self.isAcceptable(attrs):
            self.writeRow(attrs)
            self.count += 1

    def endDocument(self):
        self.output.write(']')

    def parseDate(self, date_str):
        fmt = '%Y-%m-%dT%H:%M:%S.%f'
        return datetime.strptime(date_str, fmt)

    def writeRow(self, attrs):
        if self.first: self.first = False
        else: self.output.write(',')
        json_data = json.dumps(dict(attrs.items()))
        self.output.write(json_data + '\n')

    def isQuestionOrAnswer(self, post_type):
        return True if post_type == '1' or post_type == '2' else False

    def isWithinDateRange(self, date):
        start = datetime.combine(self.DATE_FROM, datetime.min.time())
        end = datetime.combine(self.DATE_TO, datetime.min.time())
        return True if start < date < end else False

    def isAcceptable(self, attrs):
        ptype = attrs['PostTypeId']
        pdate = self.parseDate(attrs['CreationDate'])
        if not self.isWithinDateRange(pdate): return False
        if not self.isQuestionOrAnswer(ptype): return False
        return True

def filter_xml(in_file, out_file):
    parser = xml.sax.make_parser()
    handler = PostHandler(out_file)
    parser.setContentHandler(handler)
    parser.parse(in_file)
    return handler.count

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 filter_year2017.py posts.xml filtered2017.json')
        sys.exit(1)
    out_file = open(sys.argv[2], 'w')
    in_file = open(sys.argv[1], 'r', encoding='utf-8')
    print('Running filter...')
    rslt = filter_xml(in_file, out_file)
    print('Exported ' + str(rslt) + ' posts')
