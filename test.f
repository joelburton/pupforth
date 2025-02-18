\ Just some simple tests:

s" test.f running ===============" tell cr

: consty create , ;
42 consty life

: postpone immediate word find , ;
: ['] postpone ' ;

\ create : made in forth, so we don't need the primitive

create : -1 compiling! create -1 compiling! ;
: aa 1 2 + . ;
aa

\ create : -1 , compiling!

\ abort

42 constant meaning-of-life
s" the meaning of life is" tell meaning-of-life . cr

variable foo
s" foo =" tell
7 foo !
foo ?
8 foo !
s" and then =" tell
foo ?
cr

1 dup .s cr
hide dup
hidden? dup . cr
unhide dup

: msg s" my message!" ;
: times3 [[ ( n1 -- n2 ) Multiply by 3. ]] [ msg tell ] 3 * ; cr
help times3
9 times3 .
cr
s" SEE for times3:" tell cr
see times3

cr
s" test.f done ==================" tell cr cr

