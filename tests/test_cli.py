
import os
import pytest
import subprocess

import ctl



def test_cli():
    output = subprocess.check_output(
        ["ctl ls"], shell=True)

    output = u"{}".format(output)
    assert output.find(u"[usage] ran command: `ls`") > -1
