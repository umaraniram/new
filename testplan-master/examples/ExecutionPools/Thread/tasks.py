"""TCP connections tests to be executed in parallel in a thread pool."""

import threading
import time

from testplan.testing.multitest import MultiTest, testsuite, testcase

from testplan.common.utils.context import context
from testplan.testing.multitest.driver.tcp import TCPServer, TCPClient


def after_start(env):
    """
    Called right after MultiTest starts.
    """
    # Server accepts connection request made by client.
    env.server.accept_connection()


@testsuite
class TCPTestsuite(object):
    """TCP communication tests."""

    def __init__(self):
        self._thread_id = threading.current_thread().name

    @testcase
    def send_and_receive_msg(self, env, result):
        """
        Server client communication with a sleep in the middle that
        represents processing time by the server before respond.
        """
        # Client sends a message.
        msg = env.client.cfg.name
        result.log(
            "Client on thread {} is sending: {}".format(self._thread_id, msg)
        )
        bytes_sent = env.client.send_text(msg)
        received = env.server.receive_text(size=bytes_sent)
        result.equal(received, msg, "Server received")

        start_time = time.time()
        # Sleeping here to represent a time consuming processing
        # of the message received by the server before replying back.
        time.sleep(1)
        result.log(
            "Server was processing message for {}s".format(
                round(time.time() - start_time, 1)
            )
        )
        response = "Hello {}".format(received)

        result.log(
            "Server on thread {} is responding: {}".format(
                self._thread_id, response
            )
        )
        # Server sends the reply.
        bytes_sent = env.server.send_text(response)
        received = env.client.receive_text(size=bytes_sent)
        result.equal(received, response, "Client received")


def make_multitest(index=0):
    """
    Creates a new MultiTest that runs TCP connection tests.
    This will be created inside a thread worker.
    """
    print(
        "Creating a MultiTest on {}.".format(threading.current_thread().name)
    )
    test = MultiTest(
        name="TCPMultiTest_{}".format(index),
        suites=[TCPTestsuite()],
        environment=[
            TCPServer(name="server"),
            TCPClient(
                name="client",
                host=context("server", "{{host}}"),
                port=context("server", "{{port}}"),
            ),
        ],
        after_start=after_start,
    )
    return test
