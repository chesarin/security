#!/usr/bin/env python
from M2Crypto import SSL
import re

serv_addr = ('www.american-giant.com', 443)
ctx = SSL.Context()
s = SSL.Connection(ctx)
s.connect(serv_addr)
mycert = s.get_peer_cert()
plain_text = re.sub('\n', '', mycert.as_text())
p = re.compile(r"Signature Algorithm: \w+ ")
match = p.search(plain_text)
print match.group()
# subject = mycert.get_subject()

class ProcessFile(object):
    def __init__(self, filename):
        self.sites = []
        self.filename = filename
        with open(filename, 'r') as datfile:
            self._parse(datfile)
            
    def _check_entry(self, line, pattern):
        match = pattern.search(line)
        if match:
            self.sites.append(match.group())
            
    def _parse(self, datfile):
        pattern = re.compile(r"\w+.\w+.\w+")
        read_line = datfile.readline()
        self._check_entry(read_line, pattern)
        while read_line:
            read_line = datfile.readline()
            if not read_line:
                break
            self._check_entry(read_line, pattern)
            
    def get_domains(self):
        return self.sites


if __name__ == "__main__":
    
    process_file = ProcessFile('domains.txt')
    domains = process_file.get_domains()
    for domain in domains:
        print domains
