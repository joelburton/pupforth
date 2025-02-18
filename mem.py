import array

mem = array.array('q', [0] * 4096)
mem_mv = memoryview(mem)

class MStack():

    # TODO: sp is beyond top item; is this right? or should it be at top item?

    s0 = 1023
    _sp = 1023
    mv: memoryview = None

    def __init__(self, mem=1024):
        assert mem % 8 == 0, "Mem must be multiple of 8"
        self.mv = mem_mv[:mem // 8]
        self.raw_mv = self.mv.cast('b')

    @property
    def sp(self):
        return self._sp

    @sp.setter
    def sp(self, new_sp):
        assert 0 <= new_sp < len(self.mv), f"New sp must be between 0 and {len(self.mv)}"
        self._sp = new_sp

    def mem(self):
        return len(self.mv)

    @property
    def depth(self):
        return 8 * self.nitems

    @property
    def nitems(self):
        return self.sp - self.so

    def push(self, val):
        self.mv[self.sp] = val
        assert 0 <=self.sp < len(self.mv), "SP out of range"
        self.sp += 1

    def pop(self):
        assert 1 <= self.sp < len(self.mv), "SP out of range"
        v = self.mv[self.sp - 1]
        self.sp -= 1
        return v

    def peek(self):
        assert 1 <= self.sp < len(self.mv), "SP out of range"
        return self.mv[self.sp - 1]


s = MStack()
s.push(127)
print(s.peek())
print(s.pop())


def dump(start, num):
    for adr in range(start, start + num + 1):
        assert 0 <= adr <= 4096, "Mem access out of range"
        print(f"{adr:8x} {bytearray(mem[adr:adr+1]).hex()}")
