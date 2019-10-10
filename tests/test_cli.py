import os
import pytest
import subprocess

import ctl


def test_cli(config_dir):
    output = subprocess.check_output(
        ["ctl ls --home {}".format(os.path.join(config_dir, "standard"))], shell=True
    )

    output = u"{}".format(output)
    assert output.find(u"[usage] ran command: `ls --home") > -1
