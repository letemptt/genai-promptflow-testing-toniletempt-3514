import csv
import sys
import json

def write_json(csv_file=None, jsonl_file=None):
    try:
       csvfile = open(csv_file, 'r')
       jsonfile = open(jsonl_file, 'w')
       fieldnames = ("Question", "Answer", "Context")
       reader = csv.DictReader( csvfile, fieldnames)
       for row in reader:
            json.dump(row, jsonfile)
            jsonfile.write('\n')

    except Exception as e:
        print("failed to write json file %s" % (e))
    return

if __name__ == "__main__":
    write_json(sys.argv[1], sys.argv[2])
    #write_json('travelchatresults0722.csv', 'travelchatresults0722.jsonl')