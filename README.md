# mkdocs-versions-menu

This MkDocs plugin generates a versions menu from the branches of a git repository. It is intended to be used with the [mkdocs-material](https://github.com/squidfunk/mkdocs-material) theme.

It does the following when enabled in a docs repo:

* It injects the required [theme](mkdocs_versions_menu/theme) files, but allows customization if these are provided by the docs
* For the latest branch, it copies the docs to site/x.y
* For other branches, it moves the docs to site/x.y
* It generates supporting Javascript glue for tying it all together

Inspired by: https://github.com/containous/structor

## Requirements

* The [mkdocs-material](https://github.com/squidfunk/mkdocs-material) theme
* A git docs repository

## Setup

Install the plugin using pip:

`pip install git+https://github.com/RedisLabs/mkdocs-versions-menu.git`

Activate the plugin in `mkdocs.yml`:
```yaml
plugins:
  - search
  - versions-menu:
      exclude-regexes:
        - '(?!.*)'
      include-regex: '([0-9]+)\.([0-9]+)'
      master-branch: 'master'
      master-text: 'Master'
      css-path: 'css'
      javascript-path: 'javascript'
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

More information about plugins in the [MkDocs documentation][mkdocs-plugins].

## Config

* `exclude-regexes` - a list of branch regexes to exclude (default: ['(?!.*)'], i.e. nothing)
* `include-regexes` - a string regex of branches to include, where `\$1` is the major version and `\$2` is the minor (default: '([0-9]+)\.([0-9]+)')
* `master-branch` - a string name of the master branch, if set to '' then no master (default: 'master')
* `master-text` - a string text to display for master branch (defaults to capitalized form of `master-branch`)
* `css-path` - the site's css relative path (default: 'css')
* `javascript-path` - the site's Javascript relative path (default: 'javascript')

## Usage
