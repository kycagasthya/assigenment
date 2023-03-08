import setuptools

setuptools.setup(
    name="takeoff-dl-ingest",
    install_requires=[],
    packages=setuptools.find_packages(),
    package_data={
        '': ['*/*.json']
    }
)
