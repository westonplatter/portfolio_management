import glob
import os
from shutil import copyfile

import click


@click.group()
def core():
    pass


@core.command()
@click.option("--all", default="0", help="Import ALL trades?")
def upload(all):
    from upload_to_portfolio_manager import execute

    import_all: bool = all != "0"
    execute(import_all)


@core.command()
def copy():
    csv_files = []
    for file in glob.glob("*.csv"):
        csv_files.append(file)

    for file in csv_files:
        print(f"Deleting = {file}")
        os.remove(file)

    lsc_data_path = "/Users/vifo/work/lsc/loganstreetcap/data/*closed_trades*"

    for file in glob.glob(lsc_data_path):
        print(f"Copying {file}")
        fn = file.split("/")[-1]
        dest = f"/Users/vifo/work/lsc/portfolio_management/data/{fn}"
        copyfile(file, dest)


if __name__ == "__main__":
    core()
