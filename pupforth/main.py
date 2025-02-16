from .exceptions import ForthError
from .stack import Stack
from .words import new_word, number, quit_, clear_stack


class State:
    stk: Stack = Stack()
    ret_stack: Stack = Stack()
    inp_buffer: str = ""
    inp_pos: int = 0

    @property
    def latest(self):
        # noinspection PyUnresolvedReferences
        return new_word.latest

    def interpret(self):
        try:
            self.word()
        except IndexError:
            return
        self.find()
        self.execute()

    def word(self):
        nw = ""
        while self.inp_buffer[self.inp_pos].isspace():
            self.inp_pos += 1
        while not self.inp_buffer[self.inp_pos].isspace():
            nw += self.inp_buffer[self.inp_pos]
            self.inp_pos += 1
        self.inp_pos += 1
        self.stk.push(nw)

    def find(self):
        w = self.stk.pop()
        cur = self.latest
        while cur:
            if w == cur.name and not cur.hidden:
                self.stk.push(cur)
                return None
            cur = cur.next_
        # failed to find; try it as a number, emit token & number word
        self.stk.push(w)
        self.stk.push(number)

    def execute(self):
        self.stk.pop()(self)


def process(st, inp):
    st.inp_buffer = inp + " "
    st.inp_pos = 0
    try:
        quit_(st)
    except ForthError as e:
        clear_stack(st)
        raise e
