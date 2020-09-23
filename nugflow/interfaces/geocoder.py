import csv
import os
from pathlib import Path
import subprocess as sp
import typing
import pandas as pd


def geocode(input_path: str, output_path: str) -> None:
    p = sp.check_call(
        [
            "curl",
            "--form",
            f"addressFile=@{input_path}",
            "--form",
            "benchmark=Public_AR_Current",
            "--form",
            "vintage=Current",
            "https://geocoding.geo.census.gov/geocoder/locations/addressbatch",
            "--output",
            output_path,
        ]
    )
    print("Successfully produced", output_path)


def process(
    df: pd.DataFrame, work_dir: Path, chunk_size: int = 1000, chunk: int = 1
) -> typing.Generator[str, None, None]:
    """"""
    print("Begin processing chunk", chunk)
    lower_bound = chunk_size * (chunk - 1)
    if chunk > 1:
        lower_bound += 1
    upper_bound = chunk_size * chunk

    upload_file = str(work_dir.joinpath("data.csv"))
    df[lower_bound:upper_bound].to_csv(
        upload_file, index=None, header=False, quoting=csv.QUOTE_ALL
    )

    geocode_extract_file = str(work_dir.joinpath(f"geocode_{chunk}.csv"))
    geocode(upload_file, geocode_extract_file)
    yield geocode_extract_file

    if upper_bound <= len(df):
        yield from process(df, work_dir, chunk_size, chunk + 1)
    else:
        print(f"Done processing {len(df)} records.")
        os.remove(upload_file)
