import dis
import sys
from dataclasses import dataclass
from typing import Callable, Self

from .utils import GREEN, RESET
from .exceptions import ForthError


@dataclass
class Word:
    next_: Self | None
    name: str
    doc: str
    hidden: bool = False

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"


class PrimWord(Word):
    code: Callable

    def __init__(self, next_: Word, name: str, doc: str, code: Callable):
        super().__init__(next_, name, doc)
        self.code = code

    def __call__(self, st):
        self.code(st)


class ColWord(Word):
    words: list[Callable | int | str]

    def __init__(self, next_: Word, name: str, doc: str, words: list[Callable | int | str]):
        super().__init__(next_, name, doc)
        self.words = words

    def __call__(self, st):
        for w in self.words:
            st.stk.push(w)
            if isinstance(w, Word):
                st.execute()


def new_word(name=None):
    def decorator(func):
        nf = PrimWord(new_word.latest, name or func.__name__, func.__doc__, func)
        new_word.latest = nf
        return nf

    return decorator


new_word.latest = None


def new_col(name, wordlist: list[Callable | int | str], doc=""):
    nf = ColWord(new_word.latest, name, doc, wordlist)
    new_word.latest = nf
    return nf


@new_word()
def drop(st):
    """( n -- ) Drop top item."""
    st.stk.pop()


@new_word()
def rot(st):
    """( n1 n2 n3 -- n2 n3 n1 ) Left-rotate top 3 items."""

    n3 = st.stk.pop()
    n2 = st.stk.pop()
    n1 = st.stk.pop()
    st.stk.push(n2)
    st.stk.push(n3)
    st.stk.push(n1)


@new_word()
def dup(st):
    """( n -- n n ) Duplicate top item."""
    st.stk.push(st.stk.peek())


@new_word("tell")
@new_word(".")
def dot(st):
    """( n -- ) Pop and output top item."""
    print(st.stk.pop(), end=' ')


@new_word("number")
def number(st):
    """( w -- n ) Parse word as number."""
    n = st.stk.pop()
    try:
        n = int(n)
    except ValueError:
        raise ForthError(f"Not number: {n}")

    st.stk.push(n)


@new_word("+")
def add(st):
    """( n1 n2 -- sum ) Add n1 + n2."""
    st.stk.push(st.stk.pop() + st.stk.pop())


@new_word("*")
def mul(st):
    """( n1 n2 -- prod ) Multiply n1 * n2."""
    st.stk.push(st.stk.pop() * st.stk.pop())


@new_word("/mod")
def divmod_(st):
    """( n1 n2 -- rem quot ) Integer divide into remainder and quotient."""
    n1 = st.stk.pop()
    n2 = st.stk.pop()
    try:
        quot, rem = divmod(n2, n1)
    except ZeroDivisionError:
        raise ForthError(f"Cannot divide by zero")
    st.stk.push(rem)
    st.stk.push(quot)


@new_word("negate")
def negate(st):
    """( n1 -- -n1 ) Negate top number."""
    st.stk.push(-st.stk.pop())


@new_word("and")
def and_(st):
    """( n1 n2 -- n3 ) n1 AND n2 -> n3."""

    n2 = st.stk.pop()
    n1 = st.stk.pop()
    st.stk.push(n1 & n2)


@new_word("or")
def or_(st):
    """( n1 n2 -- n3 ) n1 OR n2 -> n3."""

    n2 = st.stk.pop()
    n1 = st.stk.pop()
    st.stk.push(n1 | n2)


@new_word()
def invert(st):
    """( n1 -- n2 ) Invert n1 (~n1) to n2."""

    n1 = st.stk.pop()
    st.stk.push(~n1)


@new_word("xor")
def xor(st):
    """( n1 n2 -- n3 ) n1 XOR n2 -> n3."""

    n2 = st.stk.pop()
    n1 = st.stk.pop()
    st.stk.push(n1 ^ n2)


@new_word()
def bsl(st):
    """( n1 -- n2 ) Bitshift n1 << 1 -> n3."""

    n1 = st.stk.pop()
    st.stk.push(n1 << 1)


@new_word()
def bsr(st):
    """( n1 -- n2 ) Bitshift n1 >> 1 -> n3."""

    n1 = st.stk.pop()
    st.stk.push(n1 >> 1)


@new_word("swap")
def swap(st):
    """( n1 n2 -- n2 n1 ) Swap top two items."""
    n2 = st.stk.pop()
    n1 = st.stk.pop()
    st.stk.push(n2)
    st.stk.push(n1)


@new_word("quit")
def quit_(st):
    st.ret_stack.clear()
    while st.inp_pos < len(st.inp_buffer):
        st.interpret()


@new_word("words")
def words_(st):
    """( -- ) Show all defined words."""
    cw = st.latest
    while cw:
        if not cw.hidden:
            print(cw.name, end=' ')
        cw = cw.next_
    print()


@new_word("words+")
def words_plus(st):
    """( -- ) Show all defined words and help."""
    cw = st.latest
    while cw:
        if not cw.hidden:
            print(f"{cw.name:20}{cw.doc}")
        cw = cw.next_


# noinspection PyUnusedLocal
@new_word("bye")
def bye(st):
    """( -- ) Quit program."""
    sys.exit()


@new_word('s"')
def literal_str_st(st):
    cs = ""
    while st.inp_buffer[st.inp_pos] != '"':
        cs += st.inp_buffer[st.inp_pos]
        st.inp_pos += 1
    st.inp_pos += 1
    st.stk.push(cs)


# noinspection PyUnusedLocal
@new_word('lit-string')
def literal_str(st):
    # nothing to do; it's already a string and on the stack :)
    pass


@new_word(".s")
def stack_dump(st):
    """( -- ) Show dump of stack."""
    print(
        f"{GREEN}<{len(st.stk)}>{RESET} "
        f"{' '.join(map(repr, st.stk))}"
        f"{GREEN} <- Top{RESET}"
    )


@new_word("\\")
def line_comment(st):
    """( -- ) Ignore until end of line."""
    while st.inp_pos < len(st.inp_buffer) and st.inp_buffer[st.inp_pos] != '\\':
        st.inp_pos += 1


@new_word("(")
def paren_comment(st):
    """( -- ) Ignore as comment until ')'."""
    while st.inp_pos < len(st.inp_buffer) and st.inp_buffer[st.inp_pos] != ')':
        st.inp_pos += 1
    st.inp_pos += 1


@new_word("clearstack")
def clear_stack(st):
    """( -- EMPTY ) Clear stack."""
    st.stk.clear()


@new_word()
def depth(st):
    """( -- n ) Put depth of stack on top."""
    st.stk.push(len(st.stk))


# noinspection PyUnusedLocal
@new_word()
def abort(st):
    """( -- EMPTY ) Clear stack and abort."""
    raise ForthError("Aborted")


@new_word("help")
def help_(st):
    """( w -- str ) Put help for w on top."""
    st.word()
    st.find()
    st.stk.push(st.stk.pop().doc)


@new_word("constant")
def constant(st):
    """( n -- ) Define constant like "42 constant meaning-of-life"."""

    st.word()
    name = st.stk.pop()
    new_col(name, [number, st.stk.pop()])


@new_word("char")
def char_(st):
    """( -- n ) Gets next word as literal character to stack."""

    st.word()
    if len(st.stk.peek()) != 1:
        raise ForthError("Not a single character")


@new_word("emit")
def emit(st):
    """( n -- ) Print ASCII char from code."""

    ch = st.stk.pop()
    print(chr(ch), end='')


@new_word("hide")
def hide(st):
    """( -- ) Hide next word."""

    st.word()
    st.find()
    wd = st.stk.pop()
    wd.hidden = True


@new_word("hidden?")
def hidden_q(st):
    """( -- ) Is next word hidden?"""

    # should we just modify .find to allow finding hidden-words with flag?

    st.word()
    w = st.stk.pop()
    cur = new_word.latest
    while cur:
        if w == cur.name:
            st.stk.push(-1 if cur.hidden else 0)
            return
        cur = cur.next_
    # failed to find; not hidden
    st.stk.push(0)


@new_word("unhide")
def unhide(st):
    """( -- ) Unhide next word."""

    st.word()
    w = st.stk.pop()
    cur = new_word.latest
    while cur:
        if w == cur.name:
            cur.hidden = False
            return
        cur = cur.next_

    raise ForthError("Not found.")


@new_word()
def forget(st):
    """( -- ) Forget word and all subsequent words."""
    st.word()
    st.find()
    wd = st.stk.pop()
    new_word.latest = wd.next_


@new_word()
def see(st):
    """( -- ) Print definition of next word."""

    st.word()
    st.find()
    wd = st.stk.pop()
    if isinstance(wd, PrimWord):
        print("Primitive word: Python bytecode follows")
        dis.dis(wd.code)
    elif isinstance(wd, ColWord):
        print(wd.words)
    else:
        raise ForthError("Unable to disassemble word.")


new_col("double", [dup, add], "( n -- 2n ) Double top item.")
# new_col("add5", [number, 5, add])
# new_col("greet", [literal_str, "Welcome, friend!", dot])
# new_col("greet2", ["Welcome, friend 2!", dot])
new_col("-", [negate, 0, swap, add], "( n1 n2 -- diff ) Subtract n1-n2.")
new_col("mod", [divmod_, drop], "( n -- rem ) Modulo n1 % n2.")
new_col("/", [divmod_, swap, drop], "( n1 n2 -- quot ) Integer-divide n1 / n2.")
new_col('."', [literal_str_st, dot], "( n -- ) Print top item.")
new_col("1+", [number, 1, add], "( n -- n+1 ) Increment top item.")
new_col("1-", [number, -1, add], "( n -- n-1 ) Decrement top item.")
new_col("2dup", [swap, dup, rot, dup], "( n1 n2 -- n1 n1 n2 n2 ) Duplicate top 2 items.")
new_col("-rot", [rot, rot], "( n1 n2 n3 -- n3 n1 n2 ) Rotate right")
new_col("help?", [help_, dot], "( -- ) Parse word and show help for it.")
new_col("over", [swap, dup, rot, swap], "( n1 n2 -- n1 n2 n1 ) Put copy of 2nd item on top.")
new_col("false", [0], "( -- 0 ) Puts FALSE on top.")
new_col("true", [-1], "( -- -1 ) Puts TRUE on top.")
new_col("nand", [and_, invert], "( n1 n2 -- n3 ) n1 NAND n2 -> n3.")
new_col("nor", [or_, invert], "( n1 n2 -- n3 ) n1 NOR n2 -> n3.")
new_col("bl", [32], "( -- 32 ) Add space char to stack.")
new_col("space", [32, emit], "( -- ) Print space character.")
new_col("cr", [10, emit], "( -- ) Print newline.")
new_col("2drop", [drop, drop], "( n1 n2 -- ) Drop two top items.")
new_col("nip", [swap, drop], "( n1 n2 -- n2 ) Drop 2nd item.")
new_col("tuck", [dup, rot, rot], "( n1 n2 -- n2 n1 n2 ) Copy top item below 2nd.")
# 2swap
