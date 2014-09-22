#!/usr/bin/env python
import re
import json

class SonicWallLogParser(object):
    def __init__(self):
        pass

    def _create_json_entry(self, fields_data):
        json_entry = {
            'date' :  fields_data[0],
            'type' :  fields_data[1],
            'action' : fields_data[2],
            'message' : fields_data[3],
            'source' : fields_data[4],
            'destination' : fields_data[5],
            'info' : fields_data[6]
        }
        data = json.dumps(json_entry)
        return data
        
    def parse(self, line):
        fields = re.split(r'-\s*', line)
        if len(fields) == 7:
            json_data = self._create_json_entry(fields)
            print json_data
        # print len(fields) 
        
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
    filename = '/home/punisher/Documents/NacoLabs/client-logs/Aug-24-2014-1.txt'
    parser.process_file(filename)
    