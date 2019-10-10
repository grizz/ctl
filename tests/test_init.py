import os
import pytest

import ctl


def test_init(config_dir):
    ctlr = ctl.Ctl(config_dir=os.path.join(config_dir, "standard"))
    assert ctlr.home == os.path.join(config_dir, "standard")
