import argparse
import sys
import pandas
import datetime

def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def main():
    parseArgs()
    pass


def parseArgs():
    parser = argparse.ArgumentParser(description='Outputs the number of each complaint type per borough for a given (creation) date range.')
    parser.add_argument('-i', help='the input csv file', required=True, nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-s', help='start date in YYYY-MM-DD format', required=True, type=valid_date)
    parser.add_argument('-e', help='end date in YYYY-MM-DD format', required=True, type=valid_date)
    parser.add_argument('-o', help='the output file', required=False, nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()
    file = args.i
    df = pandas.read_csv(file)
    print(df.columns[:4])
    
if __name__ == "__main__":
    main()