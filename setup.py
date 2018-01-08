#!/usr/bin/env python34
from distutils.core import setup
from setuptools import setup,find_packages
import wheel as wl

setup (
    # Distribution meta-data
    name = "sfmodel_d",
    version = "1.0",
    description = "used for word segment,test version",
    scripts=[''],
    packages = find_packages('sf-address-dl'),
    install_requires=['tensorflow>=1.0.0','pandas>=0.18.1','numpy>=1.11.1'],
    entry_points={'console_scripts':['sfmode_d=sf-address-dl:main']}
)
