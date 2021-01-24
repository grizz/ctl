import ctl


def plugin_instance():
    ctl.plugin.instantiate([{"type": "email", "name": "email_test"}], None)
    return ctl.plugin.get_instance("email_test")


def test_init():
    plugin = plugin_instance()
    assert plugin


def test_send():
    plugin = plugin_instance()
    msg = plugin._send(
        body="this is a test",
        subject="test subject",
        recipient="to@localhost",
        sender="from@localhost",
        test_mode=True,
    )
    assert msg["Subject"] == "test subject"
    assert msg["From"] == "from@localhost"
    assert msg["To"] == "to@localhost"
