from setuptools import setup, find_packages

version = "0.0.1"

setup(
	name="phd_management",
	version=version,
	description="PhD Lifecycle Management System",
	author="DevOps Group",
	author_email="devops@example.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=[]
)
