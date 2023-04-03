"""Setup for air-quality-spark package.
"""

from setuptools import setup

setup(
    name="air-quality-spark",
    # ideally this should be handled automatically with gitversion
    # but for simplicity we will do it manually.
    version="0.0.1",
    install_requires=["pyspark==3.1.3", "delta-spark==1.0.1"],
    packages=["air_quality_spark"],
    package_dir={"air_quality_spark": "src/air_quality_spark"},
)
