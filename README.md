# mkdocs-versions-menu

This MkDocs plugin generates a versions menu for the mkdocs-material theme.

It does the following when enabled on a git-back docs repo:

* It stores the branch's name
* It generates a list of all version branches (i.e. origin/x.y)
* (TODO) It injects the required css and js files
* For the latest branch, it copies the docs to site/x.y
* For other branches, it moves the docs to site/x.y

Inspired from: https://github.com/containous/structor

## Setup

Install the plugin using pip:

`pip install git+https://github.com/RedisLabs/mkdocs-versions-menu.git`

Assuming your docs are at `docs/`, extend the mkdocs-material theme by:

1. `mkdir -p docs/theme/css`
1. Copy the contents of [/theme/css/versions-menu.css] to `docs//theme/css/versions-menu.css`
1. `mkdir -p docs/theme/javascript`
1. Copy the contents of [/theme/javascript/versions-menu.js] to `docs//theme/javascript/versions-menu.js`
1. Copy the contents of [/theme/main.html] to `docs/theme/main.html`
1. Feel free to customizer these

Add the custom theme directory in `mkdocs.yml`:
```yaml
theme:
  name: 'material'
  custom_dir: 'docs/theme/'
```

Activate the plugin in `mkdocs.yml`:
```yaml
plugins:
  - search
  - versions-menu:
      exclude-regexes:
        - '0\.1'
      include-regex: '([0-9]+)\.([0-9]+)'
      master-branch: master
      master-text: Master
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

More information about plugins in the [MkDocs documentation][mkdocs-plugins].

## Config

* `exclude-regexes` - a list of branch regexes to exclude (default: [])
* `include-regexes` - a string regex of branches to include, where `\$1` is the major version and `\$2` is the minor (default: ''([0-9]+)\.([0-9]+)'')
* `master-branch` - a string name of the master branch, if '' then no master (default: 'master')
* `master-text` - a string text to display for master branch (defaults to capitalized `master-branch`)

## Usage

