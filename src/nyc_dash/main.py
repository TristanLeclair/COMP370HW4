from pathlib import Path
import sys
from typing import List

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Dropdown
from bokeh.plotting import curdoc, figure
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent.absolute()))

from src.utils.utils import DataHeaders, get_datafile_path


# global data
zipcodes = None
nyc311_df: pd.DataFrame = pd.DataFrame()
fig_data = ColumnDataSource(data=dict(month=[], all_zips=[], zip1=[], zip2=[]))

all_zips_data: List = []

zip1 = None
zip2 = None

months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

MONTH_COLUMN_NAME = "month"
ZIP1_COLUMN_NAME = "zip1"
ZIP2_COLUMN_NAME = "zip2"
ALLZIP_COLUMN_NAME = "allzips"

INCIDENT_ZIP = DataHeaders.IncidentZip.value
OPENED_AT_COLUMN_NAME = DataHeaders.OpenedDate.value
CLOSED_AT_COLUMN_NAME = DataHeaders.ClosedDate.value
DURATION_COLUMN_NAME = "Duration"


def import_data():
    global nyc311_df, zipcodes, zip1, zip2, all_zips_data

    csv_path = get_datafile_path(__file__, "prepped.csv")
    print(csv_path)
    nyc311_df = pd.read_csv(csv_path)

    # Get zipcodes
    print("Getting zipcodes")
    zipcodes = [str(int(x)) for x in nyc311_df[INCIDENT_ZIP].unique().tolist()]
    zipcodes = list(filter(lambda x: len(x) == 5, zipcodes))

    # Get all zipcodes data
    all_zips_df = nyc311_df.groupby([OPENED_AT_COLUMN_NAME], as_index=False).agg(
        {DURATION_COLUMN_NAME: "mean"}
    )

    all_zips_data = [
        all_zips_df.loc[all_zips_df[OPENED_AT_COLUMN_NAME] == month][
            DURATION_COLUMN_NAME
        ]
        for month in range(1, len(all_zips_df) + 1)
    ]
    zip1 = zipcodes[0]
    zip2 = zipcodes[1]


def build_zipcode_data(zip1, zip2):
    zip1 = int(zip1)
    zip2 = int(zip2)

    def get_zip_data(zipcode):
        return [
            nyc311_df.loc[
                (nyc311_df[INCIDENT_ZIP] == zipcode)
                & (nyc311_df[OPENED_AT_COLUMN_NAME] == month)
            ][DURATION_COLUMN_NAME]
            for month in range(1, len(all_zips_data) + 1)
        ]

    zip1_data = get_zip_data(zip1)
    zip2_data = get_zip_data(zip2)

    return {
        MONTH_COLUMN_NAME: [m for m in months[: len(all_zips_data)]],
        ZIP1_COLUMN_NAME: zip1_data,
        ZIP2_COLUMN_NAME: zip2_data,
        ALLZIP_COLUMN_NAME: all_zips_data,
    }


def update_zip1(event):
    global zip1, zip2

    zip1 = event.item
    fig_data.data = build_zipcode_data(zip1, zip2)


def update_zip2(event):
    global zip1, zip2
    zip2 = event.item
    fig_data.data = build_zipcode_data(zip1, zip2)


def main():
    global fig_data, zipcodes

    print("Importing data")
    import_data()
    print("Data imported")

    fig_data.data = build_zipcode_data(zip1="10001", zip2="10002")

    max_duration = nyc311_df[DURATION_COLUMN_NAME].max()

    p = figure(
        x_range=months,
        y_range=(0, 500),
        x_axis_label="Month",
        y_axis_label="Duration",
        height=500,
    )
    p.line(
        x=MONTH_COLUMN_NAME,
        y=ZIP1_COLUMN_NAME,
        source=fig_data,
        color="red",
        legend_label="Zipcode 1",
    )
    p.line(
        x=MONTH_COLUMN_NAME,
        y=ZIP2_COLUMN_NAME,
        source=fig_data,
        color="green",
        legend_label="Zipcode 2",
    )
    p.line(
        x=MONTH_COLUMN_NAME,
        y=ALLZIP_COLUMN_NAME,
        source=fig_data,
        color="blue",
        legend_label="All Zipcodes",
    )

    zip1_dropdown = Dropdown(label="Zipcode 1", menu=zipcodes)
    zip1_dropdown.on_event("menu_item_click", update_zip1)

    zip2_dropdown = Dropdown(label="Zipcode 2", menu=zipcodes)
    zip2_dropdown.on_event("menu_item_click", update_zip2)

    print("Adding to curdoc")
    curdoc().add_root(column(p, zip1_dropdown, zip2_dropdown))

    pass


main()
