"""Setup for air-quality-orchestration package.
"""
from setuptools import setup

with open("requirements.txt", encoding="utf-8") as requirements:
    install_requires = requirements.read().strip().split("\n")

setup(
    name="air-quality-orchestration",
    # ideally this should be handled automatically with gitversion
    # but for simplicity we will do it manually.
    version="0.0.5",
    install_requires=install_requires,
    packages=["air_quality_orchestration"],
    package_dir={"air_quality_orchestration": "src/air_quality_orchestration"},
)
