import argparse
import datetime
from enum import Enum
from pathlib import Path


def get_datafile_path(relativeDir: str, fname: str) -> Path:
    return Path(relativeDir).parent / fname


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


class DataHeaders(Enum):
    Borough = "Borough"
    ComplaintType = "Complaint Type"
    IncidentZip = "Incident Zip"
    OpenedDate = "Created Date"
    ClosedDate = "Closed Date"
    Status = "Status"
