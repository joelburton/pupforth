"""CLI for Pupforth.

Run like:

    $ pupforth                     # if pip-installed
    $ python3 -m pupforth          # if pip-installed

Run with "--help" to see the available options.
"""

import sys
from pathlib import Path
from pupforth import __version__

import click
from prompt_toolkit import prompt, HTML
from prompt_toolkit.history import FileHistory

from .exceptions import ForthError, ForthBye
from .main import process, State
from .utils import RED, RESET, YELLOW, BLUE


@click.command("Pupforth")
@click.version_option(__version__)
@click.option("--quiet", "-q", is_flag=True, default=False, help="Omit greet/exit text.")
@click.option("--no-stdlib", help="Don't load standard library",  is_flag=True, default=False)
@click.argument("forth_files", type=click.File("r"), nargs=-1)
def cli(forth_files, no_stdlib, quiet):
    if not quiet:
        print(f"{YELLOW}PupForth {__version__}{RESET}")
        print(f"See list of words with `words` or `words+`.")
        print(f"Get help on individual word like `help dup`\n")

    st = State()
    if not no_stdlib:
        std_lib = Path(__file__).parent / "lib.f"
        forth_files = (open(std_lib), *forth_files)
    try:
        for f in forth_files:
            try:
                for line in f:
                    process(st, line)
            except ForthError as e:
                print(f"{RED}{e} --- rest of file ignored{RESET}")

        # if a file is piped in via stdin
        if not sys.stdin.isatty():
            for line in sys.stdin.readlines():
                try:
                    process(st, line)
                except ForthError as e:
                    print(str(e))
            raise ForthBye

        # else a real live human at a terminal!
        else:
            while True:
                line = prompt(
                    HTML("<ansiyellow><b>> </b></ansiyellow>"),
                    history=FileHistory(".pupforth-history.txt"),
                )
                try:
                    process(st, line)
                except ForthError as e:
                    print(f"{RED}{e}{RESET}")

    except (EOFError, KeyboardInterrupt, ForthBye):
        if not quiet:
            print(f"{BLUE}Goodbye!{RESET}")


if __name__ == "__main__":
    cli.main()
