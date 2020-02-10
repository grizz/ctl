# Changelog


## Unreleased


## 0.3.1
### Changed
- switch to confu package, away from cfu (same version and codebase, different package name)
- update test requirements for pyaml according to python version


## 0.3.0
### Added
- `venv` plugin: `sync_setup` operation added
- `confuargparserouter`: better way to route confu generated cli parameters to sub parsers
- `changelog` plugin`
- `version` plugin: changelog validation
### Fixed
- fix #13: plugin.expose_vars: don't raise on io error
- fix #5: fix config error handling for errors that happen outside of plugin config
- fix #6: fix semantic version bumping when the current version is truncated


## 0.2.0
### Changed
- pypi plugin: config `repository` changed to `pypi_repository` (#2)
- pypi plugin: config `target` changed to `repository` (#2)