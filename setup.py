from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in purchase_request_workflow/__init__.py
from purchase_request_workflow import __version__ as version

setup(
	name="purchase_request_workflow",
	version=version,
	description="Purchase Request workflow System",
	author="Aarya",
	author_email="ak2003@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
