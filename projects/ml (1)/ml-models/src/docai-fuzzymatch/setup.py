# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

from setuptools import setup, find_namespace_packages


setup(
    name="docai-fuzzymatch",
    version="2.1.0",
    description="Package for standard fuzzymatching",
    long_description="",
    author="Quantiphi Inc.",
    author_email="support@quantiphi.com",
    license="Apache Software License",
    packages=find_namespace_packages(include=["docai.*"]),
    zip_safe=False,
    package_data = {"": ["*.json"]},
    namespace_packages=["docai"],
    install_requires=["fuzzywuzzy >= 0.18.0"],
)
