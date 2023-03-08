# Copyright 2022 Google LLC. This software is provided as-is, without warranty
# or representation for any use or purpose. Your use of it is subject to your
# agreement with Google.

from setuptools import setup, find_namespace_packages

setup(
    name="docai-models-stayconnected",
    version="1.0.10",
    description="Docai Model Library for Stay Connected Form",
    long_description="",
    author="Quantiphi Inc.",
    author_email="support@quantiphi.com",
    license="Apache Software License",
    packages=find_namespace_packages(include=["docai.*"]),
    zip_safe=False,
    namespace_packages=["docai"],
    install_requires=[
        "numpy>=1.20.0",
        "python-Levenshtein==0.12.2",
        "fuzzywuzzy==0.18.0",
        "Unidecode>=1.3.3",
        "unicodedata2>=13.0.0.post2",
        "opencv-python-headless>=4.5.5.62",
        "google-cloud-aiplatform>=1.12.0",
        "google-cloud>=0.34.0",
        "Pillow>=9.0.0",
    ],
)

