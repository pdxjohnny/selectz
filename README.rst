selectz
=======

-----

.. contents:: **Table of Contents**
    :backlinks: none

Installation
------------

selectz is distributed on PyPI_ as a universal wheel and is available on
Linux/macOS and Windows and supports Python 2.7/3.5+ and PyPy.

.. code-block:: bash

    $ pip install selectz

Usage
-----

Modified Python 3 selectors example_ using `selectz`.

.. code-block:: python

    import selectz
    import socket

    sel = selectz.Selector()

    def accept(sock):
        conn, addr = sock.accept()  # Should be ready
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        sel.register('read', conn, read)

    def read(conn):
        data = conn.recv(1000)  # Should be ready
        if data:
            print('echoing', repr(data), 'to', conn)
            conn.send(data)  # Hope it won't block
        else:
            print('closing', conn)
            sel.remove(conn)
            conn.close()

    sock = socket.socket()
    sock.bind(('localhost', 1234))
    sock.listen(100)
    sock.setblocking(False)
    sel.register('read', sock, accept)

    while True:
        sel.select()

License
-------

selectz is distributed under the terms of both

- MIT_ License
- Apache_ License, Version 2.0

at your option.

.. _PYPI: https://pypi.org
.. _example: https://docs.python.org/3/library/selectors.html
.. _MIT: https://choosealicense.com/licenses/mit
.. _Apache: https://choosealicense.com/licenses/apache-2.0
