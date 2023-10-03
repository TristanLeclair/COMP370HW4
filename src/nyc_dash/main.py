from pathlib import Path
import pandas as pd

from bokeh.plotting import curdoc, figure
from bokeh.models import Dropdown, ColumnDataSource


def get_datafile_path(fname):
    return Path(__file__).parent / fname


def import_data():
    try:
        csv_path = get_datafile_path("trimmed.tiny.csv")
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print("File not found!")
        return None

    return df


def main():
    df = import_data()
    # print(df.head)
    dropdown1 = Dropdown(label="Zipcode 1")
    dropdown2 = Dropdown(label="Zipcode 2")
    curdoc().add_root(dropdown1)
    curdoc().add_root(dropdown2)

    pass


main()
