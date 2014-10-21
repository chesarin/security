#!/usr/bin/env python
import re
import json
from datetime import datetime,tzinfo,timedelta

class TZ(tzinfo):
    def utcoffset(self, dt): 
        return timedelta(minutes=-399)

class SonicWallLogParser(object):
    def __init__(self):
        pass
    def fix_date(self, tdate):
        mydate = re.split(r'[-:.\s]\s*', tdate)
        # print mydate
        mdate = datetime(int(mydate[2]),int(mydate[0]), int(mydate[1]), int(mydate[3]), int(mydate[4]), int(mydate[5]), int(mydate[6]), tzinfo=TZ()).isoformat()
        # print mdate
        return mdate
    def _create_json_entry(self, fields_data):
        timestamp = fields_data[0].replace('/','-')
        mdate = self.fix_date(timestamp)
        #redundant code
        if len(fields_data[4]) > 2:
            source = re.split(r',', fields_data[4])
        if len(fields_data[5]) > 2:
            destination = re.split(',', fields_data[5])
        json_entry = {
            '@timestamp' :  mdate,
            'type' :  fields_data[1],
            'action' : fields_data[2],
            'message' : fields_data[3],
            'source-ip' : source[0],
            'source-port' : source[1],
            'destination-ip' : destination[0],
            'destination-port' : destination[1],
            'info' : fields_data[6]
        }
        data = json.dumps(json_entry)
        return data
        
    def parse(self, line):
        fields = re.split(r'-\s*', line)
        if len(fields) == 7:
            source = re.split(r',', fields[4])
            destination = re.split(',', fields[5])
            if len(source) > 2 and len(destination) > 2:
                json_data = self._create_json_entry(fields)
                print json_data
        
    def process_file(self, filename):
        with open(filename, 'r') as f:
            line = f.readline()
            while line:
                self.parse(line.rstrip())
                line = f.readline()
                if not line:
                    break
            
if __name__ == '__main__':
    parser = SonicWallLogParser()
    # filename = '/home/punisher/Documents/NacoLabs/client-logs/retake-gerri-logs/tz205-august-sep-2014.txt'
    filename = '/tmp/tz205.txt'
    parser.process_file(filename)
    
