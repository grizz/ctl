
import ctl


def test_ctr_config_reset():
    ctlr0 = ctl.Ctl()
    git0 = ctlr0.get_plugin("ls")
    git0.config["command"] = "changed"

    ctlr1 = ctl.Ctl()
    git1 = ctlr1.get_plugin("ls")
    assert git0.config != git1.config

def test_plugin_config_default():
    pass
