falcon-sslify
=============

Release v\ |version|

A simple falcon middleware that configures your app to redirect all incoming requests to HTTPS.
This is a port of `flask-sslify <https://github.com/kennethreitz/flask-sslify>`__ by
`Kenneth Reitz <https://github.com/kennethreitz>`__ from flask to
falcon

Installation
------------

Install the extension with using pip, or easy\_install.

.. code:: bash

    $ pip install -U flask-cors

Usage
-----
This package exposes a falcon middleware which by default forces SSL on all
routes and also enables `HSTS <https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security>`__

.. code:: python

    import falcon
    from falcon_sslify import FalconSSLify

    sslify = FalconSSLify()
    api = falcon.API(middleware=[sslify])


HTTP Strict Transport Security
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
flask-sslify also enables HSTS policy for your application by default. By default,
HSTS is set for 1 year ie ``31536000 seconds``.
You can change the duration  by passing the ``age`` parameter:

.. code:: python

    sslify = FalconSSlify(age=30000)

By default, HSTS is also enabled for subdomains, you can disable it by
setting the ``subdomains`` parameter to ``False``

.. code:: python

    sslify = FalconSSlify(subdomains=False)


HTTP 301 Redirects
^^^^^^^^^^^^^^^^^^
By default, the redirect is issued with a `HTTP 302` response. You can change
that to a `HTTP 301` response by setting ``permanent`` parameter to ``False``

.. code:: python

    sslify = FalconSSlify(permanent=False)


Skip Redirection on Certain Endpoints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
It is also possible to support HTTP and disable redirection on certain endpoints
by passing a list of such paths to ``skips`` parameter.

.. code:: python

    sslify = FalconSSlify(skips=['http_only',  'anotherpath'])


Notes
^^^^^
When using basic auth, this middelware must be placed before any
other authentication middleware so that credentials are always propmted on a
ssl connection and not on http ones.

API
---
.. autoclass:: falcon_sslify.FalconSSLify
    :members: