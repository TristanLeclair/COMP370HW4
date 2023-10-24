from bokeh.models import ColumnDataSource, Dropdown
from bokeh.plotting import curdoc, figure
import pandas as pd

from src.utils.utils import DataHeaders, get_datafile_path


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
