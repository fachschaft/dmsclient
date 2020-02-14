=================================================
Readme Drink Management System Client (dmsclient)
=================================================

Python3 library with command line interface to interact with the Drink Management System (DMS) of the `student council TF Uni Freiburg <https://fachschaft.tf.uni-freiburg.de>`_.

Example use case: Order product from the command line.

.. code:: bash

    $ dms order spezi -u johann
    (1) Johannes Mustermann
    (2) Johanna  Musterfrau
    (3) Johann   Mustermensch
    Please enter a number between 1 and 3: 1
    Order 1 NetteMarke Spezi (0.70€) for Johannes Mustermann? [YES/no] y 
    Order successful.

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
Usually the token is stored in an RC file readable with ``DmsConfig``.

.. code:: python

    import os
    from random import sample

    from dmsclient import DmsClient, DmsConfig


    rcfile = os.path.expanduser('~/.dmsrc')
    cfg = DmsConfig()
    cfg.read(rcfile)


API functions of ``DmsClient`` usually return coroutines for asynchronous access.

.. code:: python

    import asyncio


    async def async_order_random_stuff_for_last_customer(loop, cfg):
        async with DmsClient(cfg.token, cfg.api) as dms:
           # register tasks which can run in parallel
           products_task = loop.create_task(dms.products)
           sales_task = loop.create_task(dms.sale_history(num_days=1))

           # execute tasks to fetch data in parallel
           available_products = [p for p in await products_task
                                 if p.quantity > 0]
           random_product = sample(available_products, 1)[0]
           last_sale = (await sales_task)[0]

           # order random product
           await dms.add_order(random_product.id, last_sale['profile'])

    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_order_random_stuff_for_last_customer(loop, cfg))


Still, you can use the library also in a synchronous fashion

.. code:: python

   from syncer import sync


   @sync
   async def order_random_stuff_for_last_customer(cfg):
       async with DmsClient(cfg.token, cfg.api) as dms:
           # synchronous fetch data
           products = await dms.products
           sales = await dms.sale_history(num_days=1)

           available_products = [p for p in products
                                 if p.quantity > 0]
           random_product = sample(available_products, 1)[0]
           last_sale = sales[0]

           # order random product
           await dms.add_order(random_product.id, last_sale['profile'])


   order_random_stuff_for_last_customer(cfg)

Alternative:

.. code:: python

    loop = asyncio.get_event_loop()

    # Connect synchronously
    client = dms.DmsClient(cfg.token, cfg.api)
    client.connect()

    # Read products
    products = loop.run_until_complete(client.products)


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
