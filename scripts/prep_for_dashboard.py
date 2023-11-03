import argparse
import pandas as pd

from src.utils.utils import DataHeaders


INCIDENT_ZIP = DataHeaders.IncidentZip.value
OPENED_AT_COLUMN_NAME = DataHeaders.OpenedDate.value
CLOSED_AT_COLUMN_NAME = DataHeaders.ClosedDate.value
DURATION_COLUMN_NAME = "Duration"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Prep data for dashboard",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--input",
        type=argparse.FileType("r"),
        required=True,
        help="Path to input csv file",
    )
    parser.add_argument(
        "--output",
        type=argparse.FileType("w"),
        required=True,
        default="prepped.csv",
        help="Path to output csv file",
    )
    args = parser.parse_args()
    input = args.input
    output = args.output
    return input, output


def main():
    input, output = parse_args()

    print("Read csv")
    df = pd.read_csv(input)

    # Convert to datetimes
    df[OPENED_AT_COLUMN_NAME] = pd.to_datetime(df[OPENED_AT_COLUMN_NAME])
    df[CLOSED_AT_COLUMN_NAME] = pd.to_datetime(df[CLOSED_AT_COLUMN_NAME])

    # Calculate duration
    df[DURATION_COLUMN_NAME] = df[CLOSED_AT_COLUMN_NAME] - df[OPENED_AT_COLUMN_NAME]

    # Convert to hours
    df[DURATION_COLUMN_NAME] = df[DURATION_COLUMN_NAME].dt.total_seconds() / 60 / 60

    df[OPENED_AT_COLUMN_NAME] = df[OPENED_AT_COLUMN_NAME].dt.month

    df = df[[INCIDENT_ZIP, OPENED_AT_COLUMN_NAME, DURATION_COLUMN_NAME]]

    df = df.dropna(subset=[DURATION_COLUMN_NAME])

    df = df.groupby([INCIDENT_ZIP, OPENED_AT_COLUMN_NAME]).agg(
        {DURATION_COLUMN_NAME: "mean"}
    )

    print(df.head())
    print("Write csv to", output.name)
    df.to_csv(output)


if __name__ == "__main__":
    main()
