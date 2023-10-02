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
    (df, start_date, end_date, output_file) = parseArgs()
    filtered_df = filter_boroughs_and_complaint_types(df, start_date, end_date)
    results = complaints_per_borough(filtered_df)

    # if output_file is not specified, print results to stdout
    if (output_file == sys.stdout):
        print(results)
    else:
        # write results to csv file
        results.to_csv(output_file, index=False)


def parseArgs():
    parser = argparse.ArgumentParser(description='Outputs the number of each complaint type per borough for a given (creation) date range.')
    parser.add_argument('-i', help='the input csv file', required=True, nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-s', help='start date in YYYY-MM-DD format', required=True, type=valid_date)
    parser.add_argument('-e', help='end date in YYYY-MM-DD format', required=True, type=valid_date)
    parser.add_argument('-o', help='the output file', required=False, nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()
    file = args.i
    start_date = args.s
    end_date = args.e
    output_file = args.o
    df = pandas.read_csv(file)
    return (df, start_date, end_date, output_file)

def filter_boroughs_and_complaint_types(df, start_date, end_date):
    boroughs_and_complaints = df[["Borough", "Complaint Type", "Created Date"]].copy()
    # Update this to convert to datetime
    boroughs_and_complaints["Created Date"] = pandas.to_datetime(boroughs_and_complaints["Created Date"]).dt.date
    filtered_data = boroughs_and_complaints[(boroughs_and_complaints["Created Date"] >= start_date) & (boroughs_and_complaints["Created Date"] <= end_date)]
    return filtered_data

def complaints_per_borough(boroughs_and_complaints):
    boroughs_and_complaints = boroughs_and_complaints.groupby(["Complaint Type", "Borough"]).size().reset_index(name='count')
    boroughs_and_complaints = boroughs_and_complaints.sort_values(by=['count'], ascending=False)
    return boroughs_and_complaints

    
if __name__ == "__main__":
    main()