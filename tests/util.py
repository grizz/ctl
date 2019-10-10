import ctl


def instantiate_test_plugin(typ, name, _ctl=None, **extra):
    config = {"type": typ, "name": name}
    config.update(**extra)
    ctl.plugin.instantiate([config], _ctl)
    return ctl.plugin.get_instance(name)
