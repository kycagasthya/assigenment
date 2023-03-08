# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

from setuptools import setup, find_namespace_packages


setup(
    name="docai-preproc",
    version="1.0.5",
    description="Package for standard image preprocessing in docai",
    long_description="",
    author="Quantiphi Inc.",
    author_email="support@quantiphi.com",
    license="Apache Software License",
    packages=find_namespace_packages(include=["docai.*"]),
    zip_safe=False,
    namespace_packages=["docai"],
    install_requires=[
        "deskew>=0.10.40",
        "opencv-python-headless>=4.5.5.62",
        "Pillow>=9.0.0",
    ],
)
