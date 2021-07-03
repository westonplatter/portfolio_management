import click


@click.group()
def core():
    pass


# @core.command()
# @click.option("--time-period", default="weekly", help="weekly or annual.")
# @click.option("--account-type", default="real", help="real or paper")
# def download(time_period: str, account_type: str):
#     print(f"downloading: time_period={time_period}, account_type={account_type}")
#     from download_trades import execute

#     execute(time_period, account_type)


# @core.command()
# def tws_download_trades():
#     # @TODO(weston) download trades from TWS api
#     print(f"TODO tws_download")
#     from tws_client import download_trades

#     download_trades()


@core.command()
@click.option("--all", default="0", help="Import ALL trades?")
def upload(all):
    from upload_to_portfolio_manager import execute

    import_all: bool = all != "0"
    execute(import_all)


if __name__ == "__main__":
    core()
