"""
Plugin that allows you to handle repository versioning
"""

import argparse
import os

import toml

import confu.schema

import ctl
from ctl.auth import expose
from ctl.docs import pymdgen_confu_types
from ctl.exceptions import OperationNotExposed, PluginOperationStopped, UsageError
from ctl.plugins import ExecutablePlugin
from ctl.plugins.changelog import ChangelogVersionMissing
from ctl.plugins.changelog import temporary_plugin as temporary_changelog_plugin
from ctl.plugins.repository import RepositoryPlugin
from ctl.plugins.version_base import VersionBasePlugin, VersionBasePluginConfig
from ctl.util.versioning import bump_semantic, version_string


@ctl.plugin.register("semver2")
class Semver2Plugin(VersionBasePlugin):
    """
    manage repository versioning
    """

    class ConfigSchema(VersionBasePlugin.ConfigSchema):
        config = VersionBasePluginConfig()

    @classmethod
    def add_arguments(cls, parser, plugin_config, confu_cli_args):

        shared_parser = argparse.ArgumentParser(add_help=False)

        release_parser = argparse.ArgumentParser(add_help=False)
        group = release_parser.add_mutually_exclusive_group(required=False)
        group.add_argument(
            "--release",
            action="store_true",
            help="if set will also "
            "perform `merge_release` operation and tag in the specified "
            "release branch instead of the currently active branch",
        )

        group.add_argument(
            "--init",
            action="store_true",
            help="automatically create " "Ctl/VERSION file if it does not exist",
        )

        # subparser that routes operation
        sub = parser.add_subparsers(title="Operation", dest="op")

        # operation `tag`
        op_tag_parser = sub.add_parser(
            "tag",
            help="tag with a specified version",
            parents=[shared_parser, release_parser],
        )
        op_tag_parser.add_argument(
            "version", nargs=1, type=str, help="version string to tag with"
        )

        cls.add_repo_argument(op_tag_parser, plugin_config)

        # operation `bump`
        op_bump_parser = sub.add_parser(
            "bump",
            help="bump semantic version",
            parents=[shared_parser, release_parser],
        )
        op_bump_parser.add_argument(
            "version",
            nargs=1,
            type=str,
            choices=["major", "minor", "patch", "dev"],
            help="bumps the specified version segment by 1",
        )

        op_bump_parser.add_argument(
            "--no-auto-dev",
            help="disable automatic bumping of dev "
            "version after bumping `major`, `minor` or `patch`",
            action="store_true",
        )

        confu_cli_args.add(op_bump_parser, "changelog_validate")

        cls.add_repo_argument(op_bump_parser, plugin_config)

        # operations `merge_release`
        op_mr_parser = sub.add_parser(
            "merge_release",
            help="merge dev branch into release branch " "(branches defined in config)",
            parents=[shared_parser],
        )

        cls.add_repo_argument(op_mr_parser, plugin_config)

    def execute(self, **kwargs):

        super().execute(**kwargs)

        if "version" in kwargs and isinstance(kwargs["version"], list):
            kwargs["version"] = kwargs["version"][0]

        kwargs["repo"] = self.get_config("repository")

        op = kwargs.get("op")
        fn = self.get_op(op)

        if not getattr(fn, "exposed", False):
            raise OperationNotExposed(op)

        fn(**kwargs)

    @expose("ctl.{plugin_name}.tag")
    def tag(self, version, repo, **kwargs):
        """
        tag a version according to version specified

        **Arguments**

        - version (`str`): tag version (eg. 1.0.0)
        - repo (`str`): name of existing repository type plugin instance

        **Keyword Arguments**

        - release (`bool`): if `True` also run `merge_release`
        """
        repo_plugin = self.repository(repo)
        repo_plugin.pull()

        if not repo_plugin.is_clean:
            raise UsageError("Currently checked out branch is not clean")

        if kwargs.get("release"):
            self.merge_release(repo=repo)
            repo_plugin.checkout(self.get_config("branch_release") or "master")

        self.log.info(f"Preparing to tag {repo_plugin.checkout_path} as {version}")
        if not os.path.exists(repo_plugin.repo_ctl_dir):
            os.makedirs(repo_plugin.repo_ctl_dir)

        files = []

        self.update_version_files(repo_plugin, version, files)

        repo_plugin.commit(files=files, message=f"Version {version}", push=True)
        repo_plugin.tag(version, message=version, push=True)

    @expose("ctl.{plugin_name}.bump")
    def bump(self, version, repo, **kwargs):
        """
        bump a version according to semantic version

        **Arguments**

        - version (`str`): major, minor, patch or dev
        - repo (`str`): name of existing repository type plugin instance
        """

        repo_plugin = self.repository(repo)
        repo_plugin.pull()

        if version not in ["major", "minor", "patch", "prerelease"]:
            raise ValueError(f"Invalid semantic version: {version}")

        current = repo_plugin.version
        version = bump_semantic(current, version)

        self.log.info(
            "Bumping semantic version: {} to {}".format(
                version_string(current), version_string(version)
            )
        )

        if self.get_config("changelog_validate"):
            self.validate_changelog(repo, version)

        self.tag(version=version_string(version), repo=repo, **kwargs)
