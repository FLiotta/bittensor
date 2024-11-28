from argparse import ArgumentParser
from unittest import mock

import pytest

from bittensor.core.config import Config
from bittensor.core.settings import DEFAULTS
from bittensor.core.axon import Axon
from bittensor.core.subtensor import Subtensor
from bittensor.utils import networking


def test_axon():
    og_axon = Axon()

    # defaults
    assert og_axon.ip == DEFAULTS.axon.ip
    assert og_axon.port == DEFAULTS.axon.port
    assert og_axon.external_ip == networking.get_external_ip()
    assert og_axon.external_port == DEFAULTS.axon.port
    assert og_axon.config.axon.max_workers == DEFAULTS.axon.max_workers  # type: ignore

    # config values
    ip = "127.0.0.2"
    port = 8081
    external_ip = "93.23.25.92"
    external_port = 8053
    max_workers = 3

    parser = ArgumentParser()
    parser.add_argument("--axon.ip", default=ip)
    parser.add_argument("--axon.port", default=port)
    parser.add_argument("--axon.external_ip", default=external_ip)
    parser.add_argument("--axon.external_port", default=external_port)
    parser.add_argument("--axon.max_workers", default=max_workers)
    config = Config(parser)
    axon = Axon(config=config)
    assert axon.ip == ip
    assert axon.port == port
    assert axon.external_ip == external_ip
    assert axon.external_port == external_port
    assert axon.config.axon.max_workers == max_workers  # type: ignore


# subtensor
def test_subtensor():
    with mock.patch.object(Subtensor, "_get_substrate", return_value=None):
        og_subtensor = Subtensor()
        assert og_subtensor.chain_endpoint == DEFAULTS.subtensor.chain_endpoint
        assert og_subtensor.network == DEFAULTS.subtensor.network

        network = "this-should-fail"
        chain_endpoint = "ws://pytest"
        parser = ArgumentParser()
        parser.add_argument("--subtensor.chain_endpoint", default=chain_endpoint)
        parser.add_argument("--subtensor.network", default=network)

        subtensor = Subtensor(config=Config(parser))
        assert subtensor.chain_endpoint == chain_endpoint
        assert subtensor.network != network
        assert subtensor.network == "unknown"


# threadpool
# i think this is all used in neurons templates, but it's hard to say
# that whole repo needs redone
# functions with `self` args, no type annotation

# logging machine


# neurons...
# miner


# neuron
