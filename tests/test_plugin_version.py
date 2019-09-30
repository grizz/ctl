import os
import pytest

import ctl

from ctl.plugins.repository import RepositoryPlugin
from ctl.plugins.version import VersionPlugin
from ctl.exceptions import PermissionDenied

from util import instantiate_test_plugin

class DummyRepositoryPlugin(RepositoryPlugin):

    """
    In order to test the versioning plugin we need a dummy
    repository plugin - so we can test that actions are properly
    propagated to a repository managed by the version plugin.

    This plugin serves that purpose
    """

    def init(self):
        self.repo_url = self.config.get("repo_url")
        self.checkout_path = self.config.get("checkout_path")
        self._clean = True
        self._cloned = False
        self._committed = False
        self._pulled = False
        self._pushed = False
        self._merged = None
        self._tag = None
        self._branch = "master"

    @property
    def uuid(self):
        return "deadbeef"

    @property
    def is_cloned(self):
        return self._cloned

    @property
    def is_clean(self):
        return self._clean

    @property
    def branch(self):
        return self._branch

    def commit(self, **kwargs):
        self._committed = True

    def clone(self, **kwargs):
        self._is_cloned = True

    def pull(self, **kwargs):
        self._pulled = True

    def push(self, **kwargs):
        self._committed = False
        self._pushed = True

    def tag(self, version, **kwargs):
        self._tag = version

    def checkout(self, branch, **kwargs):
        print("SETTING BRANCH", branch)
        self._branch = branch

    def merge(self, a, b, **kwargs):
        self.checkout(b)
        self._merged = b


def instantiate(tmpdir, ctlr=None):
    """
    shortcut to instantiate a version plugin as well as a dummy repository
    """
    dummy_repo = ctl.plugin._instance["dummy_repo"] = DummyRepositoryPlugin(
        {"config":{"checkout_path":str(tmpdir.mkdir("repo"))}}, ctlr)
    config = {"config":{"branch_dev":"master", "branch_release":"release"}}
    plugin = instantiate_test_plugin("version", "test_version", _ctl=ctlr, **config)
    plugin.init_version = True
    plugin.no_auto_dev = True
    return (plugin, dummy_repo)



def test_init():
    ctl.plugin.get_plugin_class('version')


def test_repository(tmpdir, ctlr):
    plugin, dummy_repo = instantiate(tmpdir, ctlr)
    assert plugin.repository("dummy_repo") == dummy_repo

def test_tag(tmpdir, ctlr):
    plugin, dummy_repo = instantiate(tmpdir, ctlr)
    plugin.tag(version="1.0.0", repo="dummy_repo")
    assert os.path.exists(dummy_repo.version_file)
    assert dummy_repo.version == ('1','0','0')
    assert dummy_repo._tag == "1.0.0"

    plugin.tag(version="1.0.1", repo="dummy_repo")
    assert dummy_repo.version == ('1','0','1')
    assert dummy_repo._tag == "1.0.1"

    plugin.tag(version="1.0.2", repo="dummy_repo", release=True)
    assert dummy_repo.version == ('1','0','2')
    assert dummy_repo._tag == "1.0.2"
    assert dummy_repo._merged == "release"
    assert dummy_repo.branch == "release"


def test_bump(tmpdir, ctlr):
    plugin, dummy_repo = instantiate(tmpdir, ctlr)
    plugin.tag(version="1.0.0", repo="dummy_repo")

    plugin.bump(version="dev", repo="dummy_repo")
    assert dummy_repo.version == ('1','0','0','1')
    assert dummy_repo._tag == "1.0.0.1"

    plugin.bump(version="patch", repo="dummy_repo")
    assert dummy_repo.version == ('1','0','1')
    assert dummy_repo._tag == "1.0.1"

    plugin.bump(version="minor", repo="dummy_repo")
    assert dummy_repo.version == ('1','1','0')
    assert dummy_repo._tag == "1.1.0"

    plugin.bump(version="major", repo="dummy_repo")
    assert dummy_repo.version == ('2','0','0')
    assert dummy_repo._tag == "2.0.0"

    with pytest.raises(ValueError):
        plugin.bump(version="invalid", repo="dummy_repo")


def test_execute(tmpdir, ctlr):
    plugin, dummy_repo = instantiate(tmpdir, ctlr)
    plugin.execute(op="tag", version="1.0.0", repository="dummy_repo", init=True)
    assert dummy_repo._tag == "1.0.0"

    plugin.execute(op="bump", version="patch", repository="dummy_repo", init=True,
                   no_auto_dev=True)
    assert dummy_repo._tag == "1.0.1"

    with pytest.raises(ValueError, match="operation not defined"):
        plugin.execute(op=None)

    with pytest.raises(ValueError, match="invalid operation"):
        plugin.execute(op="invalid")



def test_execute_permissions(tmpdir, ctldeny):
    plugin, dummy_repo = instantiate(tmpdir, ctldeny)
    with pytest.raises(PermissionDenied):
        plugin.execute(op="tag", version="1.0.0", repo="dummy_repo", init=True)

    with pytest.raises(PermissionDenied):
        plugin.execute(op="bump", version="patch", repo="dummy_repo", init=True)

