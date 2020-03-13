import os
import re
import shutil
from git import Repo
from jinja2 import Template
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

class VersionsMenuPlugin(BasePlugin):
    config_scheme = (
        ('exclude-regexes', config_options.Type(list, default=list())),
        ('include-regex', config_options.Type(str, default='([0-9]+)\\.([0-9]+)')),
        ('master-branch', config_options.Type(str, default='master')),
        ('master-text', config_options.Type(str, default=None)),
    )

    def on_pre_build(self, config):
        assert config['theme'].name == 'material'

    def on_post_build(self, config):
        repo = Repo()
        assert not repo.bare

        master = self.config['master-branch'] if len(self.config['master-branch']) > 0 else None
        branch = str(repo.active_branch)
        exclude = re.compile('|'.join(self.config['exclude-regexes']))
        include = re.compile(f'^origin/({self.config["include-regex"]})$')
        valid_master = False

        # Stamp the active branch's version as a JS module
        with open(f'{config["site_dir"]}/javascript/branch.mjs', 'w') as f:
            f.write(f'export const branch = "{ branch }";\n')

        # Collect versions
        versions = []
        for r in [str(x) for x in repo.remote().refs]:
            if master and r == f'origin/{master}':
                valid_master = True
            else:
                m = include.search(r)
                if m and not exclude.search(m[1]):
                    versions.append((int(m[2]), int(m[3]), m[1]))
        versions.sort(reverse=True)
        latest = versions[0][2]
        if master:
            assert valid_master

        # Generate versions JS module
        with open(f'{config["site_dir"]}/javascript/versions.mjs', 'w') as f:
            f.write(f'export const latest = "{ latest }";\n')
            f.write('export const versions = [\n')
            if master:
                txt = self.config['master-text'] if self.config['master-text'] else master.capitalize()
                f.write(f'  {{ branch: "{master}", path: "{master}", text: "{txt}" }},\n')
            for (mj, mn, br) in versions:
                f.write(f'  {{ branch: "{br}", path: "{mj}.{mn}", text: "v{br}" }},\n')
            f.write('];\n')

        if branch == latest:
            shutil.copytree(config["site_dir"], f'{config["site_dir"]}/{branch}')
        else:
            files = os.listdir(config["site_dir"])
            os.mkdir(os.path.join(config["site_dir"], branch))
            for f in files:
                shutil.move(os.path.join(config["site_dir"], f), f'{config["site_dir"]}/{branch}/{f}')
