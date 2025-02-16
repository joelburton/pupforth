"""Primitive Forth words implemented in Python.

Many more words are implemented in Forth; see lib.f.
"""

import dis
import ctypes

from .exceptions import ForthError, ParseError, ForthBye
from .utils import RESET, GREEN
from .words import new_word, new_col, PrimWord, ColWord


@new_word()
def word(self):
    """( -- tok ) Get next token to stack."""
    nw = ""

    try:
        while self.inp_buffer[self.inp_pos].isspace():
            self.inp_pos += 1
        while not self.inp_buffer[self.inp_pos].isspace():
            nw += self.inp_buffer[self.inp_pos]
            self.inp_pos += 1
        self.inp_pos += 1
        self.stk.push(nw)
    except IndexError:
        raise ParseError("Couldn't find next token.")

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


@new_word("number", compilation=True)
def number(st):
    """( w -- n ) Parse word as number."""
    n = st.stk.pop()
    try:
        n = int(n)
    except ValueError:
        raise ForthError(f"Not number: {n}")

    if st.compiling:
        st.col_stk.push(n)
    else:
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
    """( n1 n2 -- rem quot ) Int divide into remainder and quotient."""
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
    raise ForthBye()


@new_word('s"', compilation=True)
def literal_str_st(st):
    cs = ""
    while st.inp_buffer[st.inp_pos] != '"':
        cs += st.inp_buffer[st.inp_pos]
        st.inp_pos += 1
    st.inp_pos += 1

    if st.compiling:
        st.col_stk.push(cs)
    else:
        st.stk.push(cs)

# @new_word('ss"')
# def literal_str_st(st):
#     cs = ""
#     while st.inp_buffer[st.inp_pos] != '"':
#         cs += st.inp_buffer[st.inp_pos]
#         st.inp_pos += 1
#     st.inp_pos += 1
#
#     if st.compiling:
#         st.col_stk.push(cs)
#     else:
#         st.stk.push(cs)


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


@new_word("(", compilation=True)
def paren_comment(st):
    """( -- ) Ignore as comment until ')'."""

    # FIXME: works when shouldn't for ( foo bar), ( foo bar)., etc
    # change imp to getting words and looking for ) token ?

    while True:
        word(st)
        wd = st.stk.pop()
        if wd == ")":
            break


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


@new_word("help@")
def help_at(st):
    """( w -- str ) Put help for w on top."""
    word(st)
    find(st)
    st.stk.push(st.stk.pop().doc)


@new_word("constant")
def constant(st):
    """( n -- ) Def const: `42 constant wtf-life`."""

    word(st)
    name = st.stk.pop()
    new_col(name, [st.stk.pop(), number])


@new_word("char")
def char_(st):
    """( -- n ) Push next word as literal char."""

    word(st)
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

    word(st)
    find(st)
    wd = st.stk.pop()
    wd.hidden = True


@new_word("hidden?")
def hidden_q(st):
    """( -- ) Is next word hidden?"""

    word(st)
    find(st, find_hidden=True)
    wd = st.stk.pop()
    st.stk.push(-1 if wd.hidden else 0)


@new_word("unhide")
def unhide(st):
    """( -- ) Unhide next word."""

    word(st)
    find(st, find_hidden=True)
    w = st.stk.pop()
    w.hidden = False


@new_word()
def forget(st):
    """( -- ) Forget word and all subsequent words."""
    word(st)
    find(st)
    wd = st.stk.pop()
    new_word.latest = wd.next_


@new_word()
def see(st):
    """( -- ) Print definition of next word."""

    word(st)
    find(st)
    wd = st.stk.pop()
    if isinstance(wd, PrimWord):
        print("Primitive word: Python bytecode follows")
        dis.dis(wd.code)
    elif isinstance(wd, ColWord):
        print(wd.words)
    else:
        raise ForthError("Unable to disassemble word.")
    print(f"{'(hidden) ' if wd.hidden else ''}", end="")
    print(f"{'(compilation) ' if wd.compilation else ''}", end="")
    print(f"{'(immediate) ' if wd.immediate else ''}")


@new_word()
def find(st, find_hidden=False):
    """( s -- w ) Finds word by string name."""

    rez = st.find(find_hidden)
    if rez:
        raise ForthError(f"Not word: {rez}")


@new_word()
def execute(st):
    """( w -- ) Execute word."""

    st.stk.pop()(st)


@new_word(":")
def colon(st):
    """( -- ) Define new word."""

    word(st)
    name = st.stk.pop()
    st.compiling = name
    st.docstring = ""
    st.colon_start = len(st.stk)


@new_word(";", compilation=True, immediate=False)
def semicolon(st):
    """( -- ) End new word definition."""

    new_col(st.compiling, st.col_stk[:], st.docstring)
    st.compiling = None
    st.col_stk.clear()


@new_word("[[", compilation=True, immediate=False)
def docstring_start(st):
    """( -- ) Start docstring, like: `: 2drop [[ n1 n2 -- ) ]] drop drop ;`"""

    start_i = st.inp_pos
    while True:
        word(st)
        wd = st.stk.pop()
        if wd == "]]":
            break

    st.docstring = st.inp_buffer[start_i:st.inp_pos].strip().removesuffix("]]").strip()


@new_word("dsp@")
def dsp_r(st):
    """( -- n ) Get location of stack pointer."""

    return len(st.stk) - 1


@new_word("dsp!")
def dsp_w(st):
    """( m -- ) Write location of stack pointer."""

    raise NotImplementedError


@new_word("[", compilation=True, immediate=False)
def imm_start(st):
    """( -- ) Start immediate mode."""

    st.force_immediate = True


@new_word("]", immediate=True)
def imm_end(st):
    """( -- ) End immediate mode."""

    st.force_immediate = False


@new_word("@")
def at(st):
    """( addr -- v ) Get value at address (variables only!)."""

    val = st.memory[st.stk.pop()]
    st.stk.push(val)


@new_word("!")
def bang(st):
    """( v addr -- ) Set value at address."""

    addr = st.stk.pop()
    v = st.stk.pop()
    st.memory[addr] = v


@new_word("variable")
def variable(st):
    """( -- ) Create variable from next word."""

    word(st)
    name = st.stk.pop()
    st.memory.append(None)
    addr = len(st.memory) - 1
    new_col(name, [addr])


@new_word("'")
def tick(st):
    """( -- addr ) Kinda worthless right now. FIXME."""
    word(st)
    find(st)
    st.stk.push(id(st.stk.pop()))
