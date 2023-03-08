# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

from setuptools import setup, find_namespace_packages


setup(
    name="docai-processor",
    version="1.0.17",
    description="Package for online prediction from docai custom processor",
    long_description="",
    author="Quantiphi Inc.",
    author_email="support@quantiphi.com",
    license="Apache Software License",
    packages=find_namespace_packages(include=["docai.*"]),
    zip_safe=False,
    namespace_packages=["docai"],
    install_requires=["google-cloud-documentai==1.3.0"],
)
