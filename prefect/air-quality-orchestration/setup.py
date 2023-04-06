"""Setup for air-quality-orchestration package.
"""
from setuptools import setup

setup(
    name="air-quality-orchestration",
    # ideally this should be handled automatically with gitversion
    # but for simplicity we will do it manually.
    version="0.0.2",
    install_requires=["prefect-gcp[cloud_storage]==0.4.0"],
    packages=["air_quality_orchestration"],
    package_dir={"air_quality_orchestration": "src/air_quality_orchestration"},
)
