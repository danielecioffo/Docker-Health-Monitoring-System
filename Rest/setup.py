# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "swagger_server"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="Docker Health Monitoring System",
    author_email="",
    url="",
    keywords=["Swagger", "Docker Health Monitoring System"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['swagger_server=swagger_server.__main__:main']},
    long_description="""\
    This are the REST API for communicating with the Docker Health Monitoring System. The system monitors the wellbeing of the containers running on the hosts bt sending periodic probes. The REST API gives to the user the possiblity to retrieve some information about the containers
    """
)

