class ForthError(Exception):
    """Generic class for problem in Forth code."""


class StackUnderflow(ForthError):
    """Attempted to pop from empty stack."""


class ParseError(ForthError):
    """Parsing problem."""


class ForthBye(Exception):  # <-- not a subclass!
    """Exit program."""
