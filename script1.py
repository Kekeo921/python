import json

prometheusFile = open("prometheus.json", "r") 
prometheusJson = json.load(prometheusFile)
prometheusFile.close()


statusFile = open('stat.txt', 'r')
statusLines = statusFile.readlines()
statusFile.close()

for line in statusLines:
    line=line.strip()
    data, timestamp, source, app, mode, status, operator, server = line.split(' ')
    for single_value in prometheusJson['values']:
        if single_value['labels'][1] == server:
            if status == "Active":
                single_value["value"] = 1
            if status == "Down":
                single_value["value"] = 0

prometheusFile = open("prometheus.json", "w+")
prometheusFile.write(json.dumps(prometheusJson))
