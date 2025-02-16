"""Infrastructure for Forth words and colon words."""

from dataclasses import dataclass
from typing import Callable, Self

from .utils import parse_docstring


@dataclass
class Word:
    next_: Self | None
    name: str
    doc: str
    hidden: bool = False
    compilation: bool = False
    immediate: bool = True  # not used right now

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"


class PrimWord(Word):
    code: Callable

    def __init__(self,
                 next_: Word,
                 name: str,
                 doc: str,
                 code: Callable,
                 compilation: bool,
                 immediate: bool):
        super().__init__(next_, name, doc, False, compilation, immediate)
        self.code = code

    def __call__(self, st, *args, **kwargs):
        self.code(st, *args, **kwargs)


class ColWord(Word):
    words: list[Callable | int | str]

    def __init__(self,
                 next_: Word,
                 name: str,
                 doc: str,
                 words: list[Callable | int | str],
                 compilation: bool,
                 immediate: bool):
        super().__init__(next_, name, doc, False, compilation, immediate)
        self.words = words

    def __call__(self, st):
        for w in self.words:
            st.stk.push(w)
            if isinstance(w, Word):
                st.stk.pop()(st)


def new_word(name=None, compilation=False, immediate=True):
    def decorator(func):
        nf = PrimWord(
            next_=new_word.latest,
            name=name or func.__name__,
            doc=parse_docstring(func.__doc__ or ""),
            compilation=compilation,
            immediate=immediate,
            code=func,
        )
        new_word.latest = nf
        return nf

    return decorator


new_word.latest = None


def new_col(name, wordlist: list[Callable | int | str], doc="", compilation=False, immediate=True):
    nf = ColWord(
        next_=new_word.latest,
        name=name,
        doc=parse_docstring(doc),
        words=wordlist,
        compilation=compilation,
        immediate=immediate,
    )
    new_word.latest = nf
    return nf
