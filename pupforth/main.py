from .exceptions import ForthError
from .stack import Stack
from .words import new_word
from .primitives import quit_, clear_stack, word, execute, number


class State:
    """State machine for the overall Forth environment."""

    stk: Stack = Stack()
    col_stk: Stack = Stack()
    ret_stack: Stack = Stack()
    inp_buffer: str = ""
    inp_pos: int = 0
    compiling: str = None
    # colon_start: int = 0

    @property
    def latest(self):
        """Head of stack of added-words."""
        # noinspection PyUnresolvedReferences
        return new_word.latest

    def interpret(self):
        """Main interp: parse word, find it (or find ok number), exec it."""
        try:
            word(self)
        except ForthError:
            return
        fail_w = self.find()
        if fail_w:
            # failed to find; try it as a number, emit token & number word
            self.stk.push(fail_w)
            self.stk.push(number)

        op = self.stk.peek()
        if self.compiling:
            if op.compilation:
                execute(self)
            else:
                self.col_stk.push(self.stk.pop())
        else:
            if not op.immediate:
                raise ForthError("Cannot use in immediate mode")
            else:
                execute(self)

    def find(self, find_hidden=False):
        """Find word in dict.

        Put found word on stack.
        Finds hidden words with is_hidden.
        If not found, returns token searched for.
        """
        w = self.stk.pop()
        cur = self.latest
        while cur:
            if w == cur.name and (find_hidden or not cur.hidden):
                self.stk.push(cur)
                return
            cur = cur.next_
        # on failure, return the searched-for word; this won't be
        # accessible to forth code, but will to the interp loop
        return w


def process(st, inp):
    """Process line of Forth."""
    st.inp_buffer = inp + " "
    st.inp_pos = 0
    try:
        quit_(st)
    except ForthError as e:
        clear_stack(st)
        st.compiling = None
        raise e
