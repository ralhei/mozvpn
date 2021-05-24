#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'requests', 'PyQt6']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', 'flake8']

setup(
    author="Ralph Heinkel",
    author_email='rh@ralph-heinkel.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Tools and GUI for MozillaVPN.",
    entry_points={
        'console_scripts': [
            'mozvpn=mozvpn.cli:main',
            'xmozvpn=mozvpn.cli:xmozvpn',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='mozvpn',
    name='mozvpn',
    packages=find_packages(include=['mozvpn', 'mozvpn.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ralhei/mozvpn',
    version='0.2.0',
    zip_safe=False,
)
