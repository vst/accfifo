accfifo: A FIFO accounting calculator
=====================================

.. image:: https://travis-ci.org/vst/accfifo.svg?branch=develop

``TODO: Provide a complete README file``

Usage
-----

Check tests to see examples.

Development
-----------

Nix shell is provided::

    nix-shell

You can choose between different Python versions::

    nix-shell --arg python "\"python39\""
    nix-shell --arg python "\"python310\""

Once you are inside the Nix shell, you can then run Visual Studio Code::

    code .

Testing
-------

If you are inside the Nix shell::

    python test_accfifo.py

Without entering the Nix shell, for Python 3.9::

    nix-shell --arg python "\"python39\"" --command "python test_accfifo.py"

\... and for Python 3.10::

    nix-shell --arg python "\"python310\"" --command "python test_accfifo.py"


License
-------

This library is licensed under `BSD 2-Clause <http://opensource.org/licenses/BSD-2-Clause>`_.
