#!/usr/lib/ckan/venv/bin/python3
#
# This writes the extracted strings from a
# particular log context to a JSON file.
#
# ./extract-strings.py default /tmp/default.json

import json
import sys

from coverage import Coverage
from string_extractor import StringExtractor

cov = Coverage(data_file="/coverage/coverage.dat", cover_pylib=True)
cov.start()
cov.load(init=False)
cov.stop()
context = sys.argv[1]
extractor = StringExtractor(True, "/coverage/stringextractor_cache.dat")
lines = cov.export_execution_path(context)
strings = extractor.get_batch(lines, True)
extractor.save()
result = json.dumps(strings)
with open(sys.argv[2],"w") as output:
    output.write(result)
