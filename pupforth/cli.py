import click
from prompt_toolkit import prompt, HTML
from prompt_toolkit.history import FileHistory

from .exceptions import ForthError
from .main import process, State
from .utils import RED, RESET


@click.command("Pupforth")
@click.argument("file_input", type=click.File("rb"), nargs=-1)
def cli(file_input):
    st = State()
    try:
        for f in file_input:
            for line in f:
                process(st, line.decode("utf-8"))

        while True:
            line = prompt(
                HTML("<ansiyellow><b>> </b></ansiyellow>"),
                history=FileHistory(".pupforth-history.txt"),
            )
            try:
                process(st, line)
            except ForthError as e:
                print(f"{RED}{e}{RESET}")

    except (EOFError, KeyboardInterrupt):
        pass


cli.main()
