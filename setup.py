from setuptools import setup, find_packages


setup(
    name='mkdocs-versions-menu',
    version='0.1.2',
    description='A MkDocs plugin for generating versions menu',
    long_description='',
    keywords='mkdocs',
    url='',
    author='RedisLabs',
    author_email='oss@redislabs.com',
    license='MIT',
    python_requires='>=2.7',
    install_requires=[
        'mkdocs>=1.0.4',
        'GitPython>=3.1.0',
        'beautifulsoup4>=4.8.2'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
        'Programming Language :: Python :: 3.8'
    ],
    packages=find_packages(),
    package_data={
        '': ['theme/*.*'],
    },
    entry_points={
        'mkdocs.plugins': [
            'versions-menu = mkdocs_versions_menu.plugin:VersionsMenuPlugin'
        ]
    }
)
