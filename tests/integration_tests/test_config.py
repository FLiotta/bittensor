from argparse import ArgumentParser

import pytest

from bittensor.core.config import Config
from bittensor.core.settings import DEFAULTS
from bittensor.core.axon import Axon
from bittensor.utils import networking


def test_axon():
    og_axon = Axon()
    assert og_axon.ip == DEFAULTS.axon.ip
    assert og_axon.port == DEFAULTS.axon.port
    assert og_axon.external_ip == networking.get_external_ip()
    assert og_axon.external_port == DEFAULTS.axon.port
    assert og_axon.config.axon.max_workers == DEFAULTS.axon.max_workers  # type: ignore

    parser = ArgumentParser()
    parser.add_argument("--axon.ip", default="127.0.0.2")
    parser.add_argument("--axon.port", default=8081)
    parser.add_argument("--axon.external_ip", default="93.23.25.92")
    parser.add_argument("--axon.external_port", default=8053)
    parser.add_argument("--axon.max_workers", default=3)
    config = Config(parser)
    axon = Axon(config=config)
    assert axon.ip == "127.0.0.2"
    assert axon.port == 8081
    assert axon.external_ip == "93.23.25.92"
    assert axon.external_port == 8053
    assert axon.config.axon.max_workers == 3  # type: ignore



# subtensor
# subtensor.chain_endpoint
# subtensor.network



# threadpool
# i think this is all used in neurons templates, but it's hard to say
# that whole repo needs redone
# functions with `self` args, no type annotation

# logging machine


# neurons...
# miner


# neuron


