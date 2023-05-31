from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in propertymgt_dxb/__init__.py
from propertymgt_dxb import __version__ as version

setup(
	name="propertymgt_dxb",
	version=version,
	description="Application to manage property rentals in UAE",
	author="HyperCloud",
	author_email="fadilsiddique@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
