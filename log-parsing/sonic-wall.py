#!/usr/bin/env python
import re
import json

class SonicWallLogParser(object):
    def __init__(self):
        pass

    def _create_json_entry(self, fields_data):
        timestamp = fields_data[0].replace('/','-')
        #redundant code
        if len(fields_data[4]) > 2:
            source = re.split(r',', fields_data[4])
        if len(fields_data[5]) > 2:
            destination = re.split(',', fields_data[5])
        json_entry = {
            '@timestamp' :  timestamp,
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
    # filename = '/home/punisher/Documents/NacoLabs/client-logs/gerri-logs/home-router-traffic.txt'
    filename = 'tz205.txt'
    parser.process_file(filename)
    
