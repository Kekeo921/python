import re
import json

statusFile = open('stat.txt', 'r')
statusLines = statusFile.readlines()
statusFile.close()

prometheusFile = open("prometheus.json", "r") 
prometheusJson = json.load(prometheusFile)
prometheusFile.close()

regexp = re.compile(
    r'(?P<data>\d{1,4}-\d{1,2}-\d{1,2}\s)' +
    '(?P<timestamp>(\d{1,2}\:\d{1,2}\:\d{1,2}\s))' +
    '(?P<source>(\w{1,11}\s))' +  
    '(?P<app>(\w{8,12}\s))' +
    '(?P<mode>(\w{6,}\s))' +
    '(?P<operation>(\w{4,}\s))' +
    '(?P<operator>(-\s))' +
    '(?P<server>([s][r][v][0-9][0-9]))' 
)
for element in statusLines:
    m=regexp.match(element)
    
    if not m:
        continue

#    print (m.group('data'), m.group('timestamp'), m.group('source'), m.group('app'), m.group('mode'), m.group('operation'), m.group('operator'), m.group('server'))

    for single_value in prometheusJson['values']:
        if single_value['labels'][1] == m.group('server'):
            if "Active" in m.group('operation'):
                single_value["value"] = 1
            if "Down" in m.group('operation'):
                single_value["value"] = 0

    prometheusFile = open("prometheus.json", "w+")
    prometheusFile.write(json.dumps(prometheusJson))
    prometheusFile.close()