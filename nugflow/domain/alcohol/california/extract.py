from pathlib import Path
import requests


def extract(dst_path: Path) -> None:
    out_file = dst_path.joinpath(f"data.csv.zip")
    r = requests.get("https://www.abc.ca.gov/wp-content/uploads/WeeklyExport_CSV.zip")
    with open(str(out_file), "wb") as f:
        f.write(r.content)


if __name__ == "__main__":
    extract(Path("/home/alexanderldixon/downloads/"))
