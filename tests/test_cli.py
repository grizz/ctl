import os
import subprocess

import pytest

import ctl


def test_cli(config_dir):
    output = subprocess.check_output(
        ["ctl ls --home {}".format(os.path.join(config_dir, "standard"))], shell=True
    )

    output = f"{output}"
    assert output.find("[usage] ran command: `ls --home") > -1
