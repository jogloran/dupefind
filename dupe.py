import argparse
import os
import sys
from collections import defaultdict

def _hash(fn, h=hash):
    return h(file(fn, 'r').read())
    
class Record(object):
    __slots__ = ['size', 'files']
    def __init__(self):
        self.size = None
        self.files = []
    def __repr__(self): return '<%s %d>' % (self.size, len(self.files))
    def __len__(self): return len(self.files)
    
def walk_tree(rootpath):
    hashes = defaultdict(Record)
    for path, dirs, files in os.walk(rootpath):
        for file in files:
            full_path = os.path.join(path, file)
            if os.path.exists(full_path):
                h = _hash(full_path)
                hashes[h].files.append(full_path)
                hashes[h].size = os.path.getsize(full_path)
    return {k:v for k,v in hashes.iteritems() if len(v) > 1}
    
def make_template(largest_file_size, largest_record):
    def nchars(s):
        return len(str(s))
    f, r = map(nchars, (largest_file_size, largest_record))
    return (
        '%%%dd (%%%dd) | %%s' % (f, r),
        ' ' * (f + r + 3 + 1) + '| %s')
    
def output_largest(hashes):
    largest_file_size = max(hashes.values(), key=lambda record: record.size).size
    largest_record    = max(hashes.values(), key=lambda record: len(record)).__len__()
    
    first_template, other_template = make_template(largest_file_size, largest_record)
    for record in sorted(hashes.values(), key=lambda record: record.size * len(record), reverse=True):
        print first_template % (record.size, len(record), record.files[0])
        for file in record.files[1:]:
            print other_template % file
                       
if __name__ == '__main__':
    # parser = make_parser()
    # args = parser.parse_args()
    hashes = walk_tree(os.path.expanduser(sys.argv[1]))
    output_largest(hashes)