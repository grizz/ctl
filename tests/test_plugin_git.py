import ctl
import subprocess
from util import instantiate_test_plugin

def init_tmp_repo(tmpdir):
    repo_path = str(tmpdir.mkdir("git_repo_src.git"))
    repo_path_clone = str(tmpdir.mkdir("git_repo_clone"))

    subprocess.call(["cd {path}; git init --bare;".format(path=repo_path)], shell=True)
    subprocess.call(["git clone {src} {path}".format(src=repo_path, path=repo_path_clone)], shell=True)

    subprocess.call(["echo empty > {path}/README.md".format(path=repo_path_clone)], shell=True)
    subprocess.call(["cd {path}; git config user.name pytest; git config user.email pytest@localhost; git add *; git commit -am initial;".format(
        path=repo_path_clone)], shell=True)
    subprocess.call(["cd {path}; git push -u origin master;".format(
        path=repo_path_clone, src=repo_path)], shell=True)

    subprocess.call(["cd {path}; git branch test;".format(
        path=repo_path_clone)], shell=True)

    return repo_path, repo_path_clone

def instantiate(tmpdir, ctlr=None, **kwargs):
    repo_path, repo_path_clone = init_tmp_repo(tmpdir)
    print(repo_path, repo_path_clone)
    config = {
        "config" : {
            "repo_url": repo_path,
            "checkout_path": str(tmpdir.mkdir("git_repo_co"))
        }
    }
    config["config"].update(**kwargs)
    plugin = instantiate_test_plugin("git", "test_git", _ctl=ctlr, **config)

    subprocess.call(["cd {path}; git config user.name pytest; git config user.email pytest@localhost".format(
        path=plugin.checkout_path)], shell=True)

    return plugin, repo_path_clone


def test_init_and_clone(tmpdir, ctlr):
    plugin, repo_path = instantiate(tmpdir, ctlr)
    assert plugin.is_cloned == True
    assert plugin.is_clean == True
    assert plugin.branch == "master"
    assert len(plugin.uuid) > 0

def test_pull(tmpdir, ctlr):
    plugin, repo_path = instantiate(tmpdir, ctlr)
    subprocess.call(
        ["echo changed > {path}/README.md; cd {path}; "\
         "git commit -am 'update'; git push -u origin master".format(path=repo_path)],
        shell=True
    )
    plugin.execute(op="pull")
    with open("{}/README.md".format(plugin.checkout_path), "r") as fh:
        assert fh.read() == "changed\n";

def test_commit_and_push(tmpdir, ctlr):
    plugin, repo_path = instantiate(tmpdir, ctlr)
    subprocess.call(
        ["echo abcdef > {path}/README.md".format(path=plugin.checkout_path)],
        shell=True
    )
    plugin.commit(files=["README.md"], message="updated", push=True)

    subprocess.call(
        ["cd {path}; git pull;".format(path=repo_path)], shell=True)

    with open("{}/README.md".format(repo_path), "r") as fh:
        assert fh.read() == "abcdef\n";

def test_tag(tmpdir, ctlr):
    plugin, repo_path = instantiate(tmpdir, ctlr)
    plugin.tag("0.0.1", "0.0.1", push=True)

    subprocess.call(
        ["cd {path}; git pull;".format(path=repo_path)], shell=True)

    out = subprocess.check_output(
        ["cd {path}; git tag;".format(path=repo_path)], shell=True)

    assert u"{}".format(out).find("0.0.1") > -1


def test_branch_and_merge(tmpdir, ctlr):
    plugin, repo_path = instantiate(tmpdir, ctlr, branch="test")

    # confirm we are starting on `test` branch
    assert plugin.branch == "test"

    # update README.md on test brach and commit
    subprocess.call(
        ["echo abcdeftest > {path}/README.md".format(path=plugin.checkout_path)],
        shell=True
    )
    plugin.commit(files=["README.md"], message="test")

    # switch back to master and check file was reverted
    plugin.checkout("master")
    with open("{}/README.md".format(plugin.checkout_path), "r") as fh:
        assert fh.read() == "empty\n";

    # merge test
    plugin.merge("test", "master")
    assert plugin.branch == "master"

    # check that master is now on the new file
    with open("{}/README.md".format(plugin.checkout_path), "r") as fh:
        assert fh.read() == "abcdeftest\n";



