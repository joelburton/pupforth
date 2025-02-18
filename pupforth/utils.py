"""General utilities."""
import re

# ANSI color codes
RESET = "\u001b[0m"
RED = "\u001b[31m"
GREEN = "\u001b[32m"
YELLOW = "\u001b[33m"
BLUE = "\u001b[34m"

def parse_docstring(s, width=25):
    """Parse out the stack effect, if present.

    >>> parse_docstring("( n -- n ) Foo foo", 12)
    '( n -- n )   Foo foo'

    >>> parse_docstring("( n -- n ) Foo foo", 2)
    '( n -- n ) Foo foo'

    >>> parse_docstring("Foo foo", 12)
    '             Foo foo'

    >>> parse_docstring("( n -- n )      Foo foo", 12)
    '( n -- n )   Foo foo'
    """

    RE = re.compile(r"^(\([^)]+\))?(.*)$")
    mo = RE.match(s)
    se, text = mo.groups()
    se = se or ""
    text = text.strip()
    return f"""{se:{width}s} {text}"""


def to_base_n(decimal_number, base):
    if decimal_number == 0:
        return "0"

    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
    while decimal_number > 0:
        remainder = decimal_number % base
        result = digits[remainder] + result
        decimal_number //= base
    return result


# decimal_number = 100
# base_16_number = to_base_n(decimal_number, 2)
# print(base_16_number)