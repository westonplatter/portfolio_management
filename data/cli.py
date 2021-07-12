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


if __name__ == "__main__":
    core()
