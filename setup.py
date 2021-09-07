# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in european_banking_integration/__init__.py
from european_banking_integration import __version__ as version

setup(
	name='european_banking_integration',
	version=version,
	description='Banking Integration For Eupopean Banks in ERPNext',
	author='Grynn GMBH',
	author_email='paideepak@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
