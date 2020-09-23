import io
import pandas as pd
import requests


def extract() -> pd.DataFrame:
    r = requests.get("https://data.colorado.gov/api/views/ier5-5ms2/rows.csv?accessType=DOWNLOAD")
    df = pd.read_csv(io.StringIO(r.content.decode('utf-8')))
    return df
