Sift Log - JSON logging adapter for Python (now in color)
=========================================================

Features
--------

-  Tag log statements with arbitrary values for easier grouping and
   analysis
-  Add keyword arguments that are converted to JSON values
-  Variable substitution
-  Specifies where log calls are made from
-  Meant to be used with core Python logging (formatters, handlers, etc)
-  Colorized logs on a console (POSIX only)
-  ``TRACE`` log level built-in

Examples
--------

A simple log message
^^^^^^^^^^^^^^^^^^^^

.. code:: python

    log.info('Hello')

``{"msg": "Hello", "time": "12-12-14 10:12:01 EST", "level": "INFO", "loc": "test:log_test:20"}``

Logging with tags
^^^^^^^^^^^^^^^^^

.. code:: python

    log.debug('Creating new user', 'MONGO', 'STORAGE')

``{"msg": "Creating new user", "time": "12-12-14 10:12:09 EST", "tags": ["MONGO", "STORAGE"], "level": "DEBUG", "loc": "test:log_test:20"}``

Appending more data
^^^^^^^^^^^^^^^^^^^

.. code:: python

    log.debug('Some key', is_admin=True, username='papito')

``{"msg": "Some key", "is_admin": true, "username": "papito", "time": "12-12-14 10:12:04 EST", "level": "DEBUG", "loc": "test:log_test:20"}``

String substitution
^^^^^^^^^^^^^^^^^^^

.. code:: python

    log.debug('User "$username" admin? $is_admin', is_admin=False, username='fez')

``{"msg": "User \"fez\" admin? False",  "username": "fez", "is_admin": false, "time": "12-12-14 10:12:18 EST", "level": "DEBUG", "loc": "test:log_test:20"}``

Setup
-----

Logging to console
^^^^^^^^^^^^^^^^^^

.. code:: python

    import sys
    import logging
    from siftlog import SiftLog

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)

    log = SiftLog(logger)

In this fashion, you can direct the JSON logs to `any logging
handler <https://docs.python.org/2/library/logging.handlers.html>`__

Color
^^^^^

For enhanced flamboyancy, attach the ``ColorStreamHandler`` to your
logger. The output will not have color if the logs are being output to a
file, or on systems that are not POSIX (will not work on Windows for
now).

.. code:: python

    from siftlog import SiftLog, ColorStreamHandler

    logger = logging.getLogger()
    handler = ColorStreamHandler(sys.stdout)
    logger.addHandler(handler)

    log = SiftLog(logger)

Different colors
''''''''''''''''

You can change font background, text color, and boldness:

.. code:: python

    from siftlog import ColorStreamHandler

    handler = ColorStreamHandler(sys.stdout)
    handler.set_color(
        logging.DEBUG, bg=handler.WHITE, fg=handler.BLUE, bold=True
    )

Supported colors
''''''''''''''''

-  ColorStreamHandler.BLACK
-  ColorStreamHandler.RED
-  ColorStreamHandler.GREEN
-  ColorStreamHandler.YELLOW
-  ColorStreamHandler.BLUE
-  ColorStreamHandler.MAGENTA
-  ColorStreamHandler.CYAN
-  ColorStreamHandler.WHITE

Constants (re-occuring values)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can define constants that will appear in every single log message.
This is useful, for example, if you'd like to log process PID and
hostname with every log message (recommended). This is done upon log
adapter initialization:

.. code:: python

    import os
    from siftlog import SiftLog
    log = SiftLog(logger, pid=os.getpid(), env='INTEGRATION')

``{"msg": "And here I am", "time": "12-12-14 11:12:24 EST", "pid": 37463, "env": "INTEGRATION", "level": "INFO"}``

Custom time format
^^^^^^^^^^^^^^^^^^

.. code:: python

    log = SiftLog(logger)
    SiftLog.TIME_FORMAT = '%d-%m-%y %H:%m:%S %Z'

Define the format as accepted by
`time.strftime() <https://docs.python.org/2/library/time.html#time.strftime>`__

Custom location format
^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    log = SiftLog(logger)
    SiftLog.LOCATION_FORMAT = '$module:$method:$line_no'

The format should be a string containing any of the following variables:

-  ``$file``
-  ``$line_no``
-  ``$method``
-  ``$module``

Custom core key names
^^^^^^^^^^^^^^^^^^^^^

Core keys, such as ``msg`` and ``level`` can be overridden, if they
clash with common keys you might be using.

The following can be redefined:

-  SiftLog.MESSAGE (default ``msg``)
-  SiftLog.LEVEL (default ``level``)
-  SiftLog.LOCATION (default ``loc``)
-  SiftLog.TAGS (default ``tags``)
-  SiftLog.TIME (default ``time``)

As in:

.. code:: python

    log = SiftLog(logger)
    SiftLog.log.MESSAGE = "MESSAGE"

