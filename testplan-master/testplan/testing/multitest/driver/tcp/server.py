"""
TCPServer driver classes.
"""

import socket

from schema import Use

from testplan.common.config import ConfigOption
from testplan.common.utils.timing import TimeoutException, TimeoutExceptionInfo
from testplan.common.utils.sockets import Server

from ..base import Driver, DriverConfig


class TCPServerConfig(DriverConfig):
    """
    Configuration object for
    :py:class:`~testplan.testing.multitest.driver.tcp.server.TCPServer` driver.
    """

    @classmethod
    def get_options(cls):
        """
        Schema for options validation and assignment of default values.
        """
        return {
            ConfigOption("host", default="localhost"): str,
            ConfigOption("port", default=0): Use(int),
        }


class TCPServer(Driver):
    """
    Driver for a server that can send and receive messages over TCP.
    Supports multiple connections.

    This is built on top of the
    :py:class:`testplan.common.utils.sockets.server.Server` class, which
    provides equivalent functionality and may be used outside of MultiTest.

    :param name: Name of TCPServer.
    :type name: ``str``
    :param host: Host name to bind to. Default: 'localhost'
    :type host: ``str``
    :param port: Port number to bind to. Default: 0 (Random port)
    :type port: ``int``

    Also inherits all
    :py:class:`~testplan.testing.multitest.driver.base.Driver`` options.
    """

    CONFIG = TCPServerConfig

    def __init__(self, name, host="localhost", port=0, **options):
        options.update(self.filter_locals(locals()))
        super(TCPServer, self).__init__(**options)
        self._host = None
        self._port = None
        self._server = None

    @property
    def host(self):
        """Target host name."""
        return self._host

    @property
    def port(self):
        """Port number assigned."""
        return self._port

    @property
    def socket(self):
        """
        Returns the underlying ``socket`` object
        """
        return self._server.socket

    def accept_connection(self, timeout=10):
        """Doc from Server."""
        return self._server.accept_connection(timeout=timeout)

    accept_connection.__doc__ = Server.accept_connection.__doc__

    def send_text(self, msg, standard="utf-8", **kwargs):
        """
        Encodes to bytes and calls
        :py:meth:`TCPServer.send
        <testplan.testing.multitest.driver.tcp.server.TCPServer.send>`.
        """
        return self.send(bytes(msg.encode(standard)), **kwargs)

    def send(self, msg, conn_idx=None, timeout=30):
        """Doc from Server."""
        return self._server.send(msg=msg, conn_idx=conn_idx, timeout=timeout)

    send.__doc__ = Server.send.__doc__

    def receive_text(self, standard="utf-8", **kwargs):
        """
        Calls
        :py:meth:`TCPServer.receive
        <testplan.testing.multitest.driver.tcp.server.TCPServer.receive>`
        and decodes received bytes.
        """
        return self.receive(**kwargs).decode(standard)

    def receive(self, size=None, conn_idx=None, timeout=30):
        """Receive bytes from the given connection."""
        received = None
        timeout_info = TimeoutExceptionInfo()
        try:
            receive_kwargs = dict(conn_idx=conn_idx, timeout=timeout or 0)
            if size is None:
                receive_kwargs["size"] = 1024
                receive_kwargs["wait_full_size"] = False
            else:
                receive_kwargs["size"] = size
                receive_kwargs["wait_full_size"] = True

            received = self._server.receive(**receive_kwargs)
        except socket.timeout:
            if timeout is not None:
                raise TimeoutException(
                    "Timed out waiting for message on {0}. {1}".format(
                        self.cfg.name, timeout_info.msg()
                    )
                )
        return received

    def starting(self):
        """Starts the TCP server."""
        super(TCPServer, self).starting()
        self._server = Server(host=self.cfg.host, port=self.cfg.port)
        self._server.bind()
        self._server.serve()
        self._host = self.cfg.host
        self._port = self._server.port

    def _stop_logic(self):
        if self._server:
            self._server.close()

    def stopping(self):
        """Stops the TCP server."""
        super(TCPServer, self).stopping()
        self._stop_logic()

    def aborting(self):
        """Abort logic that stops the server."""
        self._stop_logic()
