Pupforth
========

A minimal Forth interpreter.

While there are lots of standard functionality missing,
what is here is reasonably compliant: lots of other
Python forth interpreters don't expose the internals or
handle compilation right.

This is mostly a personal project, to force me to play
with Forth --- but if you stumble across this and
are interested, feel free to reach out!

Installation & Running
----------------------

Installing in a venv:

::

    python3 -m venv venv
    source venv/bin/activate
    pip install git+https://github.com/joelburton/pupforth.git

Running:

::

    pupforth
    pupforth --help
    echo "1 2 + ." | pupforth -q
