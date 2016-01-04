# Copyright 2015 ClusterHQ Inc.  See LICENSE file for details.
"""
Read request load scenario for the control service benchmarks.
"""

from zope.interface import implementer

from twisted.internet.defer import succeed

from .._interfaces import IRequestScenarioSetup

from ._rate_measurer import DEFAULT_SAMPLE_SIZE

from ._request_load import RequestLoadScenario


@implementer(IRequestScenarioSetup)
class ReadRequest(object):
    """
    Implementation of the read request generator and the write.
    :ivar reactor: Reactor to use.
    :ivar cluster: `BenchmarkCluster` containing the control service.
    """
    def __init__(self, reactor, cluster):
        self.control_service = cluster.get_control_service(reactor)

    def make_request(self):
        return self.control_service.list_nodes()

    def run_setup(self):
        return succeed(None)


def read_request_load_scenario(reactor, cluster, request_rate=10,
                               sample_size=DEFAULT_SAMPLE_SIZE, timeout=45):
    """
    Factory that will initialise and return an excenario that places
    load on the cluster by performing read requests at a specified rate.

    :param reactor: Reactor to use.
    :param cluster: `BenchmarkCluster` containing the control service.
    :param request_rate: The target number of requests per second.
    :param sample_size: The number of samples to collect when measuring
        the rate.
    :param timeout: Maximum time in seconds to wait for the requested
        rate to be reached.
    """
    return RequestLoadScenario(
        reactor,
        ReadRequest(reactor, cluster),
        request_rate=request_rate,
        sample_size=sample_size,
        timeout=timeout,
    )

