import sys

import click
from prompt_toolkit import prompt, HTML
from prompt_toolkit.history import FileHistory

from .exceptions import ForthError
from .main import process, State
from .utils import RED, RESET, YELLOW


@click.command("Pupforth")
@click.argument("file_input", type=click.File("rb"), nargs=-1)
def cli(file_input):
    print(f"{YELLOW}PupForth 1.0{RESET}")
    print(f"See list of words with `words` or `words+`.")
    print(f"Get help on individual word like `help dup`\n")
    st = State()
    try:
        for f in file_input:
            try:
                for line in f:
                    process(st, line.decode("utf-8"))
            except ForthError as e:
                print(f"{RED}{e} --- rest of file ignored{RESET}")
        while True:
            if sys.stdin.isatty():
                line = prompt(
                    HTML("<ansiyellow><b>> </b></ansiyellow>"),
                    history=FileHistory(".pupforth-history.txt"),
                )
            else:
                line = sys.stdin.readline()
            try:
                process(st, line)
            except ForthError as e:
                print(f"{RED}{e}{RESET}")

    except (EOFError, KeyboardInterrupt):
        pass


if __name__ == "__main__":
    cli.main()