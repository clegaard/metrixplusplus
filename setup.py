from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Metrixpp",
    version="0.0.1",
    author='',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/metrixplusplus/metrixplusplus',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    project_urls={
        'Bug Tracker': 'https://github.com/metrixplusplus/metrixplusplus/issues',
        'Documentation': 'https://metrixplusplus.github.io/home.html#download_section',
        'Source Code': 'https://github.com/metrixplusplus/metrixplusplus'
    },

    python_requires='>=3',

    entry_points={'console_scripts': ['metrixpp=mpp.metrixpp_cli:start']}
)
