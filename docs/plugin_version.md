# Version Release

This plugin allows tagging and pushing of version to repositories

It will automatically tag, merge branches and maintain a Ctl/VERSION file in the targeted repository

## Config Example

The plugin can use one ore more repository type plugins to version

```yaml
ctl:
  plugins:
    # we will use a git plugin instane to manage the repo
    - type: git
      name: my_repo
      config:
        repo_url: git@github.com:path/to/repo

    - type: version
      name: version
      config:
        # branches used during `merge_release` operation
        branch_dev: master
        branch_release: release
        repository: my_repo
```

## Version the repo specified in the `repostory` config field

```
# update Ctl/VERSION to 1.0.0
# tag 1.0.0
# push tag
ctl version tag 1.0.0
```

```
# update Ctl/VERSION from 1.0.0 to 1.1.0
# tag 1.1.0
# push tag
ctl version bump minor
```

## Use existing repository checkout

Instead of configuring and specifying a git type plugin to use 
you can also set `repository` to a directory path. It still needs
to be valid git repository


```yaml
ctl:
  plugins:
    - type: version
      name: version
      config:
        repository: /path/to/my/repository/checkout 
```

## Specifying repository in the command line

```
ctl version tag 1.0.0 /path/to/my/repository
ctl version tag 1.0.0 .
ctl version tag 1.0.0 [plugin_name]
```


## Usage

```
usage: ctl version [-h] [--branch-dev BRANCH_DEV]
                   [--branch-release BRANCH_RELEASE]
                   {tag,bump,merge_release} ...

optional arguments:
  -h, --help            show this help message and exit
  --branch-dev BRANCH_DEV
                        the branch to merge from when the --merge-release flag
                        is present (dev)
  --branch-release BRANCH_RELEASE
                        the breanch to merge to when the --merge-release flag
                        is present (master)

Operation:
  {tag,bump,merge_release}
    tag                 tag with a specified version
    bump                bump semantic version
    merge_release       merge dev branch into release branch (branches defined
                        in config)
```

### Tag

```
usage: ctl version tag [-h] [--release | --init] version [repository]

positional arguments:
  version     version string to tag with
  repository  name of repository type plugin or path to a repository checkout

optional arguments:
  -h, --help  show this help message and exit
  --release   if set will also perform `merge_release` operation and tag in
              the specified release branch instead of the currently active
              branch
  --init      automatically create Ctl/VERSION file if it does not exist
```

### Bump

```
usage: ctl version bump [-h] [--release | --init] [--no-auto-dev]
                        {major,minor,patch,dev} [repository]

positional arguments:
  {major,minor,patch,dev}
                        bumps the specified version segment by 1
  repository            name of repository type plugin or path to a repository
                        checkout

optional arguments:
  -h, --help            show this help message and exit
  --release             if set will also perform `merge_release` operation and
                        tag in the specified release branch instead of the
                        currently active branch
  --init                automatically create Ctl/VERSION file if it does not
                        exist
  --no-auto-dev         disable automatic bumping of dev version after bumping
                        `major`, `minor` or `patch`
```

### Merge_Release

```
usage: ctl version merge_release [-h] [repository]

positional arguments:
  repository  name of repository type plugin or path to a repository checkout

optional arguments:
  -h, --help  show this help message and exit
```

