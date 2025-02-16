from .exceptions import StackUnderflow


class Stack(list):
    """Simple stack for Forth. Raises specific errors on underflow."""

    push = list.append

    def peek(self):
        try:
            return self[-1]
        except IndexError as e:
            raise StackUnderflow(e)

    def pop(self, index=-1):
        assert index == -1, "Why pop anywhere but top?"
        try:
            return super().pop(index)
        except IndexError:
            raise StackUnderflow("Stack underflow")
