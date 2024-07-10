import csv
import sys

def write_csv(output_file=None, question=None, answer=None):
    try:
        with open(output_file, mode='a') as csvfile:
            #write rows
            writer = csv.writer(csvfile)
            writer.writerow([question, answer])
    except Exception as e:
        print("failed to write csv file %s" % (e))
    return

if __name__ == "__main__":
    write_csv(sys.argv[1], sys.argv[2])