"""Setup for air-quality-lakehouse package.
"""

from setuptools import setup

setup(
    name="air-quality-lakehouse",
    # ideally this should be handled automatically with gitversion
    # but for simplicity we will do it manually.
    version="0.0.7",
    install_requires=["pyspark==3.1.3", "delta-spark==1.0.1"],
    packages=["air_quality_lakehouse"],
    package_dir={"air_quality_lakehouse": "src/air_quality_lakehouse"},
)
