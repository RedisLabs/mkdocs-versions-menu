import os
import pkg_resources
import re
import shutil
from git import Repo
from jinja2 import Template
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from bs4 import BeautifulSoup as bs

class VersionsMenuPlugin(BasePlugin):
    config_scheme = (
        ('exclude-regexes', config_options.Type(list, default=['(?!.*)'])),
        ('include-regex', config_options.Type(str, default='([0-9]+)\\.([0-9]+)')),
        ('master-branch', config_options.Type(str, default='master')),
        ('master-text', config_options.Type(str, default=None)),
    )

    @staticmethod
    def _copy_to_site(src, dst):
        s = pkg_resources.resource_filename(__name__, src)
        shutil.copy(s, dst)

    def on_pre_build(self, config):
        assert config['theme'].name == 'material'

    def on_post_page(self, output, page, config):
        soup = bs(output, 'html.parser')
        soup.head.append(soup.new_tag('link', href='css/versions-menu.css', rel='stylesheet'))
        soup.head.append(soup.new_tag('script', src='javascript/versions-menu.js', type='module'))
        return soup.prettify()

    @staticmethod
    def _customize_js(path, latest):
        with open(path, 'r') as f:
            js_template = Template(f.read())
        with open(path, 'w') as f:
            f.write(js_template.render(latest=latest))

    def on_post_build(self, config):
        repo = Repo()
        assert not repo.bare

        master = self.config['master-branch'] if len(self.config['master-branch']) > 0 else None
        branch = str(repo.active_branch)
        exclude = re.compile('|'.join(self.config['exclude-regexes']))
        include = re.compile(f'^origin/({self.config["include-regex"]})$')
        valid_master = False

        # Stamp the active branch's version
        os.makedirs(f'{config["site_dir"]}/javascript', exist_ok=True)
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

        # Inject payload script and style
        os.makedirs(f'{config["site_dir"]}/css', exist_ok=True)
        payload = [
            'css/versions-menu.css',
            'javascript/versions-menu.js',
        ]
        for p in payload:
            self._copy_to_site(f'theme/{p}', f'{config["site_dir"]}/{p}')

        # Make directory structure
        if branch == latest:
            # Latest is copied
            shutil.copytree(config["site_dir"], f'{config["site_dir"]}/{branch}')
            self._customize_js(f'{config["site_dir"]}/javascript/versions-menu.js', True)
        else:
            # Others are moved
            files = os.listdir(config["site_dir"])
            os.mkdir(os.path.join(config["site_dir"], branch))
            for f in files:
                shutil.move(os.path.join(config["site_dir"], f), f'{config["site_dir"]}/{branch}/{f}')
        self._customize_js(f'{config["site_dir"]}/{branch}/javascript/versions-menu.js', False)