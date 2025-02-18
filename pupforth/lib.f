\ PUPFORTH STANDARD LIBRARY -- read this on startup, like "pupforth path-to/lib.f"

\ Core

\ IO

: cr       [[ ( -- )                       Print newline.                 ]]    10 emit ;
: bl       [[ ( -- 32 )                    Push space ASCII code.         ]]    32 ;
: space    [[ ( -- )                       Print space.                   ]]    bl emit ;
\ : ."       [[ ( n -- )                     Print top item.                ]]    s" . ;              \ BUGGY

\ Math

: double   [[ ( n -- 2n )                  Double top item.               ]]    dup + ;
: -        [[ ( n1 n2 -- diff )            Subtract n1-n2.                ]]    negate + ;
: mod      [[ ( n1 n2 -- rem )             Modulo n1 % n2.                ]]    /mod drop ;
: /        [[ ( n1 n2 -- quot )            Int-divide n1//n2.             ]]    /mod swap drop ;
: 1+       [[ ( n -- n+1 )                 Increment top item.            ]]    1 + ;
: 1-       [[ ( n -- n-1 )                 Decrement top item.            ]]    1 - ;
: 2+       [[ ( n -- n+2 )                 +2 to top item.                ]]    1+ 1+ ;
: 2-       [[ ( n -- n-2 )                 -2 to top item.                ]]    1- 1- ;

\ Logic

: false    [[ ( -- 0 )                     Push FALSE.                    ]]    0 ;
: true     [[ ( -- -1 )                    Push TRUE.                     ]]    -1 ;
: nand     [[ ( n1 n2 -- n3 )              n1 NAND n2 -> n3               ]]    and invert ;
: nor      [[ ( n1 n2 -- n3 )              n1 NOR n2 -> n3                ]]    or invert ;

\ Stack

: over     [[ ( n1 n2 -- n1 n2 n1 )        Put copy of 2nd items on top.  ]]    swap dup rot swap ;
: nip      [[ ( n1 n2 -- n2 )              Drop 2nd item.                 ]]    swap drop ;
: tuck     [[ ( n1 n2 -- n2 n1 n2 )        Copy top item below 2nd.       ]]    dup rot rot ;
: -rot     [[ ( n1 n2 n3 -- n3 n1 n2 )     Rotate right.                  ]]    rot rot ;
: 2dup     [[ ( n1 n2 -- n1 n1 n2 n2 )     Duplicate top 2 items.         ]]    swap dup rot dup ;
: 2drop    [[ ( n1 n2 -- )                 Drop two top items.            ]]    drop drop ;

\ Misc

: cs       [[ ( -- )                       Alias for `clearstack`         ]]    clearstack ;
: help     [[ ( -- )                       Parse word & show its help.    ]]    help@ . cr ;
: ?        [[ ( addr -- )                  Print value of variable.       ]]    @ . ;
