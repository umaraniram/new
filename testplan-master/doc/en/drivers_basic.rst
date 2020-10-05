Drivers
*******

MultiTest provides a dynamic driver configuration system, around the two
following properties:

    * Drivers can depend on other drivers.
    * Driver configuration is not required to exist until the driver starts.

Dependencies between drivers are expressed very simply: any driver in the
environment list passed to MultiTest is allowed to depend on any other driver
appearing earlier than itself in the list.

Specifying dependencies this way is sufficiently flexible to cover all cases
while remaining simple enough to understand and easily express.

Dependent values can be created either through the
:py:func:`context() <testplan.common.utils.context.context>` call, or using
pairs of double curly brackets in configuration files (MultiTest is using the
`Tempita <http://pythonpaste.org/tempita/>`_ templating library).

.. code-block:: python

    # Example environment of three dynamically connecting drivers.
    #  --------------         -----------------         ---------------
    #  |            | ------> |               | ------> |             |
    #  |   Client   |         |  Application  |         |   Service   |
    #  |            | <------ |               | <------ |             |
    #  --------------         -----------------         ---------------

    environment=[
        Service(name='service'),
        Application(name='app',
                    host=context('service', '{{host}}')
                    port=context('service', '{{port}}'))
        Client(name='client',
               host=context('app', '{{host}}')
               port=context('app', '{{port}}'))
    ]


Configuration
=============

Context
=======
Context at any point during the MultiTest startup is defined as the state of the
set of drivers that have already started. As soon as a driver has completed its
start step successfully, all of its attributes become part of the context and
are thus made available to all drivers that will start after it.

In practice the context is often used to communicate hostnames, port values,
file paths, and other such values dynamically generated at runtime to avoid
collisions between setups that must be shared between the various drivers to
communicate meaningfully.

Any context value from any process can be accessed by the
:py:func:`context() <testplan.common.utils.context.context>` call, taking a
driver name and a tempita expression that must be valid on that driver name.
This call effectively creates a late-bound value that drivers will resolve at
startup, against the current context.

Those expressions can also be used in the configuration of the drivers that
support them, for example
:py:class:`App <testplan.testing.multitest.driver.app.App>`. In the case of
configurations, the values of the driver that is being configured are available
in the global scope, and other drivers can be accessed through the special
'context' object.

Network dependencies
====================
Probably one of the most common use-cases of the context is the passing of
network addresses between processes. For robustness reasons, it is much
preferable to neither hardcode hosts nor ports in test setups. Ports can
typically be assigned by the operating system in such a way that collisions
between instances are avoided.

This is a simple example of a server and a client, where the server is binding
to ``localhost:0`` and communicating at runtime to the client where it is in
fact listening. As long as there are dynamic ports available on the host, this
setup will start reliably and will not collide with other already running
applications.

.. code-block:: python

    # Example environment of a Server and 2 Clients.
    #
    #      +--------- client1
    #      |
    #   server
    #      |
    #      +--------- client2
    #
    # Client will have access to the server host, port
    # after server starts.

    [
        TCPServer('server'),
        TCPClient(
            'client1',
            context('server', '{{host}}'),
            context('server', '{{port}}')
        )
        TCPClient(
            'client2',
            context('server', '{{host}}'),
            context('server', '{{port}}')
        )
    ]

Users are strongly encouraged to follow this practice rather than hardcode host
names and port numbers in their test setups.

Work with unit test
===================

Drivers can also be useful while working with other unit testing frameworks like
like GTest or Hobbes Test. Testplan will export environment variables for newly
started test process. Have a look at the following code:

.. code-block:: python

    plan.add(GTest(
        name='My GTest',
        binary=BINARY_PATH,
        environment=[
            TCPServer(name='my server'),
            TCPClient(name='client-101',
                host=context('server', '{{host}}'),
                port=context('server', '{{port}}')
            )
        ]
    )

In your unit test process, you can find an environment variable named
'DRIVER_MY_SERVER_ATTR_HOST', likewise, 'DRIVER_CLIENT_101_ATTR_PORT' is also
available. It is easy to understand that the string is formatted in uppercase,
like 'DRIVER_<uid of driver>_ATTR_<attribute name>', while hyphens and spaces
are replaced by underscores.
