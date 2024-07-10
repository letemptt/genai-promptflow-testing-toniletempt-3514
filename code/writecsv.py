import csv
import sys

def write_header(output_file=None, header_list=None):
    try:
        with open(output_file, mode='w') as csvfile:
            #write rows
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=header_list)
            writer.writeheader()
    except Exception as e:
        print("failed to write header csv file %s" % (e))
    return

def write_csv(output_file=None, question=None, answer=None, chat_context=None):
    try:
        with open(output_file, mode='a') as csvfile:
            #write rows
            writer = csv.writer(csvfile)
            writer.writerow([question, answer, chat_context])
    except Exception as e:
        print("failed to write csv file %s" % (e))
    return

if __name__ == "__main__":
    write_csv(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])