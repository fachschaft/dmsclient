=================================================
Readme Drink Management System Client (dmsclient)
=================================================

Python3 library with command line interface to interact with the Drink Management System (DMS) of the `student council TF Uni Freiburg <https://fachschaft.tf.uni-freiburg.de>`_.

Getting Started
===============

Prerequisites
-------------

You need ``python 3.5`` or newer and ``pip``.
For development you also need git installed on your machine.

Installation
------------

Install the dmsclient library and command line interface simply from *PyPi*:

.. code:: bash

    pip3 install dmsclient

For developers it's recommended to install from source vie *develop*.
Then all changes in code are automatically available in the library and command line without reinstallation.

.. code:: bash

    git clone git@<git url>:<user>/dmsclient.git
    cd dmsclient

    python3 setup.py develop

Command Line
------------

The installation of ``dmsclient`` provides a command line interface ``dms``.
For authentication you have to generate a token key in your dms profile settings.
Add your token to a ``.dmsrc`` file in your home folder.

.. code::

   [DEFAULT]
   Token = XxxxxXXXxxxxxXXXXxxxxxxxXXX

Then you can start using ``dms``. You'll find all available commands via

.. code:: bash

   dms --help

User and product names don't have to be added exactly, but are estimated from what you type. E.g.:

.. code:: bash

   $ dms buy apfel -u must
   Buy Apfelschorle (0.70€) for Max Mustermann? [Y/n]

Library
-------

For communication with the DMS via REST you can use the ``DmsClient`` class provided by this library.
Authentication is provided via a token key which you can generate in the DMS profile settings.
The ``DmsClient`` usually returns deep objects where ids were replaced by the corresponding object.

Example code:

.. code:: python

   from random import sample
   from dmsclient import DmsClient


   def order_random_stuff_for_last_customer(dms):
       available_products = (p for p in dms.products if p.quantity > 0)
       random_product = sample(available_products, 1)[0]
       last_sale = dms.sale_history(num_days=1)[0]

       dms.add_order(random_product.id, last_sale.profile.id)


   token = 'XxxxxXXXxxxxxXXXXxxxxxxxXXX'
   api_endpoint = 'https://dms.fachschaft.tf/api'
   dms = DmsClient(token, api_endpoint)
   order_random_stuff_for_last_customer(dms)

Authors
=======

Initiated by *David-Elias Künstle* <kuenstld[at]tf.uni-freiburg> / `Github <https://github.com/dekuenstle>`_
but see `contributors <https://github.com/fachschaft/dmsclient/graphs/contributors>`_ for a full list of contributions.

License
=======

dmsclient is available under the `MIT License <https://opensource.org/licenses/MIT>`_

Acknowledgements
================

Big thanks to the DMS and DMS-API developers!
